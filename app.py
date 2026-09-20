import os
from flask import Flask, render_template, request, jsonify
import relay_core

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/track", methods=["POST"])
def track():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"success": False, "error": "Query tidak boleh kosong / Query cannot be empty."}), 400
    
    result = relay_core.track_cross_chain(query)
    return jsonify(result)

@app.route("/api/inspect", methods=["POST"])
def inspect():
    data = request.get_json(silent=True) or {}
    address = data.get("address", "").strip()
    chain = data.get("chain", "ethereum").strip()
    if not address:
        return jsonify({"success": False, "error": "Alamat tidak boleh kosong / Address cannot be empty."}), 400
    
    result = relay_core.inspect_address_details(address, chain)
    return jsonify({"success": True, "data": result})

@app.route("/api/wallet/genealogy", methods=["GET", "POST"])
def wallet_genealogy():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        address = data.get("address", "").strip()
        chain = data.get("chain", "base").strip()
    else:
        address = request.args.get("address", "").strip()
        chain = request.args.get("chain", "base").strip()
        
    if not address:
        return jsonify({"success": False, "error": "Alamat dompet tidak boleh kosong / Wallet address cannot be empty."}), 400
        
    result = relay_core.analyze_wallet_genealogy(address, chain)
    return jsonify(result)

@app.route("/api/wallet/batch-sybil", methods=["POST"])
def batch_sybil():
    data = request.get_json(silent=True) or {}
    addresses = data.get("addresses", [])
    chain = data.get("chain", "base").strip()
    if not addresses:
        return jsonify({"success": False, "error": "Daftar alamat tidak boleh kosong / Addresses cannot be empty."}), 400
    res = relay_core.analyze_batch_sybil(addresses, chain)
    return jsonify(res)

@app.route("/api/deposit/trace", methods=["POST"])
def deposit_trace():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "address").strip()
    target_input = data.get("address", "") if mode == "address" else data.get("raw_data", "")
    chain = data.get("chain", "auto").strip()
    
    try:
        min_threshold_usd = float(data.get("min_threshold_usd", 50.0))
    except (ValueError, TypeError):
        min_threshold_usd = 50.0

    try:
        dust_threshold_usd = float(data.get("dust_threshold_usd", 5.0))
    except (ValueError, TypeError):
        dust_threshold_usd = 5.0

    exclude_dust = bool(data.get("exclude_dust", True))
    filter_phishing = bool(data.get("filter_phishing", True))

    if not target_input.strip():
        return jsonify({"success": False, "error": "Input tidak boleh kosong / Input cannot be empty."}), 400

    res = relay_core.trace_deposit_inflow(
        target_input=target_input,
        mode=mode,
        chain=chain,
        min_threshold_usd=min_threshold_usd,
        dust_threshold_usd=dust_threshold_usd,
        exclude_dust=exclude_dust,
        filter_phishing=filter_phishing
    )
    return jsonify(res)

@app.route("/api/chains", methods=["GET"])
def chains():
    chains_dict = relay_core.get_all_chains()
    simplified = [
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "displayName": c.get("displayName"),
            "iconUrl": c.get("iconUrl"),
            "explorerUrl": c.get("explorerUrl")
        }
        for c in chains_dict.values()
    ]
    priority_ids = [4663, 792703809, 1, 8453, 42161, 10, 56, 137]
    def sort_key(item):
        cid = item.get("id")
        return (priority_ids.index(cid) if cid in priority_ids else 9999, str(item.get("displayName")))
    
    simplified.sort(key=sort_key)
    return jsonify({"success": True, "chains": simplified})

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
    import threading, time
    def kill_server():
        time.sleep(0.4)
        os._exit(0)
    threading.Thread(target=kill_server, daemon=True).start()
    return jsonify({"success": True, "message": "Server shutting down..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] OmniRoute running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
