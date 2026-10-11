import os
import threading
import time
from flask import Flask, render_template, request, jsonify
import relay_core
import flow_trace
import storage

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_SORT_KEYS"] = False

MAX_QUERY_LEN = 300
MAX_BATCH = 20
MAX_CSV_LEN = 500_000

# ==================== SHORT-LIVED RESPONSE CACHE ====================
# Re-running the same lookup (language switch, back/forward, double click) is served instantly.
_RESP_CACHE: dict = {}
_RESP_LOCK = threading.Lock()
RESP_TTL = 60


def cached_call(key: tuple, fn):
    now = time.time()
    with _RESP_LOCK:
        hit = _RESP_CACHE.get(key)
        if hit and now - hit[0] < RESP_TTL:
            return hit[1]
    result = fn()
    if result.get("success"):
        with _RESP_LOCK:
            if len(_RESP_CACHE) > 200:
                _RESP_CACHE.pop(min(_RESP_CACHE, key=lambda k: _RESP_CACHE[k][0]))
            _RESP_CACHE[key] = (now, result)
    return result


def bad_request(msg: str):
    return jsonify({"success": False, "error": msg}), 400


def _payload() -> dict:
    return request.get_json(silent=True) or {}


def _str(data: dict, key: str, default: str = "") -> str:
    return str(data.get(key) or default).strip()


def _clamp_float(value, default: float, lo: float, hi: float) -> float:
    try:
        return max(lo, min(hi, float(value)))
    except (TypeError, ValueError):
        return default


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/track", methods=["POST"])
def track():
    query = _str(_payload(), "query")
    if not query:
        return bad_request("Query tidak boleh kosong / Query cannot be empty.")
    if len(query) > MAX_QUERY_LEN:
        return bad_request("Query terlalu panjang / Query too long.")
    return jsonify(cached_call(("track", query), lambda: relay_core.track_cross_chain(query)))


@app.route("/api/inspect", methods=["POST"])
def inspect():
    data = _payload()
    address = _str(data, "address")
    chain = _str(data, "chain", "ethereum")
    if not address:
        return bad_request("Alamat tidak boleh kosong / Address cannot be empty.")
    if len(address) > 100:
        return bad_request("Alamat tidak valid / Invalid address.")
    return jsonify({"success": True, "data": relay_core.inspect_address_details(address, chain)})


@app.route("/api/wallet/genealogy", methods=["GET", "POST"])
def wallet_genealogy():
    data = _payload() if request.method == "POST" else request.args
    address = _str(data, "address")
    chain = _str(data, "chain", "base")
    if not address:
        return bad_request("Alamat dompet tidak boleh kosong / Wallet address cannot be empty.")
    if len(address) > 100:
        return bad_request("Alamat tidak valid / Invalid address.")
    return jsonify(relay_core.analyze_wallet_genealogy(address, chain))


@app.route("/api/wallet/batch-sybil", methods=["POST"])
def batch_sybil():
    data = _payload()
    addresses = data.get("addresses") or []
    if not isinstance(addresses, list) or not addresses:
        return bad_request("Daftar alamat tidak boleh kosong / Addresses cannot be empty.")
    addresses = [str(a)[:100] for a in addresses[:MAX_BATCH]]
    return jsonify(relay_core.analyze_batch_sybil(addresses, _str(data, "chain", "base")))


@app.route("/api/deposit/trace", methods=["POST"])
def deposit_trace():
    data = _payload()
    mode = "manual" if _str(data, "mode", "address") == "manual" else "address"
    target_input = str(data.get("raw_data") if mode == "manual" else data.get("address") or "").strip()
    if not target_input:
        return bad_request("Input tidak boleh kosong / Input cannot be empty.")
    if len(target_input) > (MAX_CSV_LEN if mode == "manual" else 100):
        return bad_request("Input terlalu panjang / Input too long.")

    params = dict(
        target_input=target_input,
        mode=mode,
        chain=_str(data, "chain", "auto"),
        min_threshold_usd=_clamp_float(data.get("min_threshold_usd"), 50.0, 0, 1e9),
        dust_threshold_usd=_clamp_float(data.get("dust_threshold_usd"), 5.0, 0, 1e6),
        exclude_dust=bool(data.get("exclude_dust", True)),
        filter_phishing=bool(data.get("filter_phishing", True)),
    )
    key = ("deposit",) + tuple(sorted(params.items()))
    return jsonify(cached_call(key, lambda: relay_core.trace_deposit_inflow(**params)))


# ==================== TAB 5: FUND FLOW GRAPH ====================

def _flow_params(data: dict) -> dict:
    tokens = data.get("tokens")
    min_native = data.get("min_native")
    return dict(
        chain=_str(data, "chain", "solana").lower(),
        direction=_str(data, "direction", "forward"),
        depth=int(_clamp_float(data.get("depth"), 2, 1, flow_trace.MAX_DEPTH)),
        fanout=int(_clamp_float(data.get("fanout"), 4, 1, flow_trace.MAX_FANOUT)),
        min_native=None if min_native in (None, "") else _clamp_float(min_native, 0.0, 0, 1e9),
        min_stable_usd=_clamp_float(data.get("min_stable_usd"), flow_trace.DEFAULT_MIN_STABLE_USD, 0, 1e12),
        tokens=[str(t).upper()[:10] for t in tokens][:10] if isinstance(tokens, list) else None,
    )


@app.route("/api/flow/config", methods=["GET"])
def flow_config():
    return jsonify({
        "success": True,
        "chains": {
            c: {"tokens": list(flow_trace.TARGET_TOKENS[c]),
                "native": next(s for s, v in flow_trace.TARGET_TOKENS[c].items() if v.get("native")),
                "provider": flow_trace.provider_info(c)}
            for c in flow_trace.SUPPORTED_CHAINS
        },
        "defaults": {"minNative": flow_trace.DEFAULT_MIN_NATIVE, "minStableUsd": flow_trace.DEFAULT_MIN_STABLE_USD,
                     "maxDepth": flow_trace.MAX_DEPTH, "maxFanout": flow_trace.MAX_FANOUT, "maxSeeds": flow_trace.MAX_SEEDS},
    })


@app.route("/api/flow/trace", methods=["POST"])
def flow_trace_route():
    data = _payload()
    seeds = data.get("seeds") or []
    if isinstance(seeds, str):
        seeds = seeds.split()
    seeds = [str(s).strip()[:100] for s in seeds if str(s).strip()][:flow_trace.MAX_SEEDS]
    if not seeds:
        return bad_request("Masukkan minimal 1 alamat seed / Enter at least one seed address.")
    params = _flow_params(data)
    key = ("flow", tuple(seeds)) + tuple((k, tuple(v) if isinstance(v, list) else v) for k, v in sorted(params.items()))
    return jsonify(cached_call(key, lambda: flow_trace.trace_flow(seeds, **params)))


@app.route("/api/flow/expand", methods=["POST"])
def flow_expand():
    data = _payload()
    address = _str(data, "address")[:100]
    if not address:
        return bad_request("Alamat kosong / Address is empty.")
    params = _flow_params(data)
    graph = data.get("graph") if isinstance(data.get("graph"), dict) else {}
    return jsonify(flow_trace.expand_graph(graph, address, **params))


# ---- saved traces & marked addresses (local ./data, gitignored) ----

@app.route("/api/flow/saved", methods=["GET"])
def flow_saved_list():
    return jsonify({"success": True, "traces": storage.list_traces()})


@app.route("/api/flow/saved", methods=["POST"])
def flow_saved_create():
    data = _payload()
    snapshot = data.get("snapshot")
    if not isinstance(snapshot, dict) or not snapshot.get("nodes"):
        return bad_request("Belum ada hasil trace untuk disimpan / Nothing to save yet.")
    params = data.get("params") if isinstance(data.get("params"), dict) else {}
    try:
        record = storage.save_trace(_str(data, "name"), params, snapshot, trace_id=_str(data, "id") or None)
    except ValueError as e:
        return bad_request(f"Gagal menyimpan / Cannot save: {e}")
    return jsonify({"success": True, "trace": record})


@app.route("/api/flow/saved/<trace_id>", methods=["GET"])
def flow_saved_get(trace_id):
    trace = storage.get_trace(trace_id)
    if not trace:
        return jsonify({"success": False, "error": "Trace tidak ditemukan / Trace not found."}), 404
    return jsonify({"success": True, "trace": trace})


@app.route("/api/flow/saved/<trace_id>", methods=["DELETE"])
def flow_saved_delete(trace_id):
    return jsonify({"success": storage.delete_trace(trace_id)})


@app.route("/api/flow/marks", methods=["GET"])
def flow_marks_list():
    return jsonify({"success": True, "marks": storage.list_marks()})


@app.route("/api/flow/marks", methods=["POST"])
def flow_marks_set():
    data = _payload()
    try:
        mark = storage.set_mark(_str(data, "chain"), _str(data, "address"), _str(data, "label"),
                                _str(data, "color", "amber"), _str(data, "note"))
    except ValueError as e:
        return bad_request(str(e))
    return jsonify({"success": True, "mark": mark})


@app.route("/api/flow/marks", methods=["DELETE"])
def flow_marks_delete():
    data = _payload()
    return jsonify({"success": storage.delete_mark(_str(data, "chain"), _str(data, "address"))})


_PRIORITY_CHAIN_IDS = [4663, 792703809, 1, 8453, 42161, 10, 56, 137]


@app.route("/api/chains", methods=["GET"])
def chains():
    def build():
        simplified = [
            {k: c.get(k) for k in ("id", "name", "displayName", "iconUrl", "explorerUrl")}
            for c in relay_core.get_all_chains().values()
        ]
        simplified.sort(key=lambda item: (
            _PRIORITY_CHAIN_IDS.index(item["id"]) if item["id"] in _PRIORITY_CHAIN_IDS else 9999,
            str(item.get("displayName")),
        ))
        return {"success": True, "chains": simplified}
    return jsonify(cached_call(("chains",), build))


@app.route("/api/samples", methods=["GET"])
def samples():
    return jsonify({
        "relay": {
            "protocol": "Relay.link",
            "url": "https://robin.etherscan.io/tx/0x2a17e404fed1a1bdc3c97bcc7249f4a5c1dd1c65be59b608dd1d32b395f91031",
            "label": "Robinhood Chain ➔ Solana Bridge (USDG 5,345.60)"
        },
        "lifi": {
            "protocol": "Li.Fi / Jumper Exchange",
            "url": "https://bscscan.com/tx/0xda166887e41e61838ae518bedc05c7735270f84d7ac89ebe290986747fb65cec",
            "label": "BSC Swap & Cross-Chain Route (1inch / Li.Fi)"
        },
        "deposit_solana": {
            "address": "2S1zLXppAyd9st2Y9BSn4ZMsTUHU3s7cB44yBXDdEJ1h",
            "chain": "solana",
            "label": "Solana Personal Deposit / Settlement Address"
        },
        "deposit_evm": {
            "address": "0x0532da9a4248daa5a48b4d7c6c1c8fe447b1320a",
            "chain": "base",
            "label": "EVM Active Deposit Address"
        }
    })


@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "app": "OmniRoute"})


@app.route("/api/shutdown", methods=["POST"])
def shutdown():
    def kill_server():
        time.sleep(0.4)
        os._exit(0)
    threading.Thread(target=kill_server, daemon=True).start()
    return jsonify({"success": True, "message": "Server shutting down..."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] OmniRoute running on http://127.0.0.1:{port}")
    # Warm the chain registry so the first lookup doesn't pay for it.
    threading.Thread(target=relay_core.get_all_chains, daemon=True).start()
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)
