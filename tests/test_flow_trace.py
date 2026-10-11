"""Unit tests for flow_trace: BFS limits, filters, and detectors on a synthetic graph (no network)."""
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import flow_trace as ft  # noqa: E402

BINANCE = "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9"  # labelled CEX hot wallet in relay_core


def addr(tag: str) -> str:
    """A syntactically valid Solana (base58) address made from a readable tag."""
    tag = tag.translate(str.maketrans({"l": "L", "I": "J", "O": "Q", "0": "Z"}))
    return (tag + "x" * 44)[:40]


SEED_A, SEED_B = addr("SeedA"), addr("SeedB")
P1, P2, P3 = addr("Peel1"), addr("Peel2"), addr("Peel3")
DEP = addr("Deposit")
SPLIT_X, SPLIT_Y, SPLIT_Z = addr("SplitX"), addr("SplitY"), addr("SplitZ")
DUST = addr("Dust")
USDC_DST = addr("UsdcDst")


def tr(src, dst, amount, token="SOL", tx=None):
    return {"from": src, "to": dst, "token": token, "amount": amount, "ts": 1_700_000_000,
            "tx": tx or f"tx-{src[:6]}-{dst[:6]}-{token}-{amount}"}


SCENARIO = [
    tr(SEED_A, P1, 10),
    tr(SEED_A, DUST, 0.01),                 # dust: must not create a branch
    tr(SEED_A, USDC_DST, 50, token="USDC"),  # excluded when tokens=["SOL"]
    tr(P1, P2, 9), tr(P1, SPLIT_X, 1),
    tr(P2, P3, 8), tr(P2, SPLIT_Y, 1),
    tr(P3, DEP, 7), tr(P3, SPLIT_Z, 0.8),
    tr(SEED_B, DEP, 5),
    tr(DEP, BINANCE, 12),
]


def NO_ACCOUNTS(chain, addresses):
    """Offline stand-in for the RPC account-type lookup."""
    return {}


class StubFetcher:
    def __init__(self, transfers, delay=0.0):
        self.transfers = transfers
        self.delay = delay
        self.calls = []

    def __call__(self, chain, address):
        self.calls.append(address)
        if self.delay:
            time.sleep(self.delay)
        rows = [t for t in self.transfers if address in (t["from"], t["to"])]
        return rows, {"ok": True, "raw_count": len(rows), "spoofed": 0, "limit_hit": False, "source": "stub"}


@pytest.fixture(autouse=True)
def fixed_prices(monkeypatch):
    monkeypatch.setattr(ft, "token_price", lambda chain, sym: 1.0 if sym in ft.STABLES else 100.0)


def run(seeds, transfers=SCENARIO, **kw):
    fetcher = kw.pop("fetcher", None) or StubFetcher(transfers)
    params = dict(chain="solana", depth=4, fanout=4, min_native=0.1, tokens=["SOL", "USDC"], fetcher=fetcher,
                  account_detector=kw.pop("account_detector", NO_ACCOUNTS))
    params.update(kw)
    return ft.trace_flow(seeds, **params), fetcher


def finding(res, ftype):
    return [f for f in res["findings"] if f["type"] == ftype]


def test_basic_graph_and_edges():
    res, _ = run([SEED_A, SEED_B])
    assert res["success"]
    ids = {n["id"] for n in res["nodes"]}
    assert {SEED_A, SEED_B, P1, P2, P3, DEP, BINANCE} <= ids
    e = next(e for e in res["edges"] if e["from"] == SEED_A and e["to"] == P1)
    assert e["amount"] == 10 and e["usd"] == 1000


def test_dust_never_branches():
    res, _ = run([SEED_A])
    assert DUST not in {n["id"] for n in res["nodes"]}
    assert res["stats"]["dust_filtered"] >= 1


def test_token_filter():
    res, _ = run([SEED_A], tokens=["SOL"])
    assert USDC_DST not in {n["id"] for n in res["nodes"]}
    res2, _ = run([SEED_A], tokens=["SOL", "USDC"])
    assert USDC_DST in {n["id"] for n in res2["nodes"]}


def test_stable_minimum_is_in_usd():
    res, _ = run([SEED_A], min_stable_usd=100)  # the 50 USDC transfer is below $100
    assert USDC_DST not in {n["id"] for n in res["nodes"]}


def test_cex_deposit_detected_and_cex_not_expanded():
    res, fetcher = run([SEED_A, SEED_B])
    dep = next(n for n in res["nodes"] if n["id"] == DEP)
    assert "cex_deposit" in dep["roles"]
    assert "Binance" in dep["cex"]
    assert BINANCE not in fetcher.calls  # traversal stops at the exchange
    assert finding(res, "cex_deposit")


def test_shared_deposit_cluster_links_both_seeds():
    res, _ = run([SEED_A, SEED_B])
    assert len(res["clusters"]) == 1
    c = res["clusters"][0]
    assert c["depositAddress"] == DEP
    members = {m["address"]: m for m in c["members"]}
    assert members[SEED_B]["relation"] == "direct" and members[SEED_B]["confidence"] == 90
    assert members[SEED_A]["relation"] == "upstream"
    assert c["multiSeed"] is True and set(c["seedsInCluster"]) == {SEED_A, SEED_B}
    assert finding(res, "shared_deposit")[0]["severity"] == "high"


def test_peeling_chain_detected():
    res, _ = run([SEED_A, SEED_B])
    peel = finding(res, "peeling_chain")
    # SeedA itself peels (10 SOL on, 50 USDC split off), so the chain starts at the seed
    assert peel and peel[0]["nodes"] == [SEED_A, P1, P2, P3, DEP] and peel[0]["count"] == 4


def test_consolidation_detected():
    c1, c2, c3, hub = addr("Cons1"), addr("Cons2"), addr("Cons3"), addr("Collector")
    transfers = [tr(SEED_A, c1, 2), tr(SEED_A, c2, 2), tr(SEED_A, c3, 2),
                 tr(c1, hub, 2), tr(c2, hub, 2), tr(c3, hub, 2)]
    res, _ = run([SEED_A], transfers=transfers, depth=2)
    cons = finding(res, "consolidation")
    assert cons and cons[0]["nodes"][0] == hub and cons[0]["count"] == 3


def test_cex_star_two_deposits():
    d1, d2 = addr("DepOne"), addr("DepTwo")
    transfers = [tr(SEED_A, d1, 3), tr(SEED_A, d2, 3), tr(d1, BINANCE, 3), tr(d2, BINANCE, 3)]
    res, _ = run([SEED_A], transfers=transfers, depth=2)
    star = finding(res, "cex_star")
    assert star and star[0]["count"] == 2


def test_fanout_cap():
    outs = [tr(SEED_A, addr(f"Fan{c}"), 1 + i) for i, c in enumerate("ABCDEF")]
    res, _ = run([SEED_A], transfers=outs, depth=1, fanout=2)
    assert len(res["nodes"]) == 3  # seed + top-2 by value
    assert {n["id"] for n in res["nodes"]} >= {addr("FanF"), addr("FanE")}


def test_depth_cap():
    res, fetcher = run([SEED_A], depth=1)
    assert P2 not in {n["id"] for n in res["nodes"]}
    assert fetcher.calls == [SEED_A]


def test_node_budget_truncates():
    res, _ = run([SEED_A, SEED_B], max_nodes=3)
    assert res["stats"]["truncated"] and res["stats"]["truncate_reason"] == "node_budget"
    assert len(res["nodes"]) == 3


def test_time_budget_truncates():
    slow = StubFetcher(SCENARIO, delay=0.3)
    res, _ = run([SEED_A], fetcher=slow, time_budget=0.35)
    assert res["success"] and res["stats"]["truncated"]


def test_edge_not_double_counted_from_both_ends():
    res, _ = run([SEED_B], direction="both", depth=2)
    e = next(e for e in res["edges"] if e["from"] == SEED_B and e["to"] == DEP)
    assert e["amount"] == 5 and e["count"] == 1


def test_backward_direction_follows_senders():
    res, fetcher = run([DEP], direction="backward", depth=2)
    ids = {n["id"] for n in res["nodes"]}
    assert {P3, SEED_B, P2} <= ids
    # the sweep into the exchange is still recorded (deposit detection) but never traversed
    assert BINANCE in ids and BINANCE not in fetcher.calls
    assert "cex_deposit" in next(n for n in res["nodes"] if n["id"] == DEP)["roles"]


def test_hub_is_not_traversed():
    hub = addr("BusyHub")
    transfers = [tr(SEED_A, hub, 5)] + [tr(hub, addr(f"Cust{i:02d}".replace("0", "Q")), 1) for i in range(20)]

    class LimitHit(StubFetcher):
        def __call__(self, chain, address):
            rows, meta = super().__call__(chain, address)
            meta["limit_hit"] = address == hub
            return rows, meta

    fetcher = LimitHit(transfers)
    res, _ = run([SEED_A], transfers=transfers, fetcher=fetcher, depth=3)
    hub_node = next(n for n in res["nodes"] if n["id"] == hub)
    assert hub_node["hub"] and "hub" in hub_node["roles"]
    assert len(fetcher.calls) == 2  # seed + hub, never the hub's customers


def test_invalid_input():
    assert not ft.trace_flow(["not-an-address"], chain="solana", fetcher=StubFetcher([]))["success"]
    assert not ft.trace_flow([SEED_A], chain="dogechain", fetcher=StubFetcher([]))["success"]


# ---- parsers ----

def test_evm_parser_rejects_spoofed_stablecoin():
    real = ft.TARGET_TOKENS["ethereum"]["USDT"]["address"]
    rows = [
        {"from": "0x" + "1" * 40, "to": "0x" + "2" * 40, "contractAddress": real, "value": "5000000",
         "tokenSymbol": "USDT", "timeStamp": "1", "hash": "0xa"},
        {"from": "0x" + "1" * 40, "to": "0x" + "2" * 40, "contractAddress": "0x" + "9" * 40, "value": "9" * 20,
         "tokenSymbol": "USDT", "timeStamp": "1", "hash": "0xb"},
    ]
    transfers, spoofed = ft._normalize_evm_rows("ethereum", [], rows)
    assert len(transfers) == 1 and transfers[0]["amount"] == 5.0 and spoofed == 1


def test_evm_parser_bsc_18_decimals_and_native():
    usdt = ft.TARGET_TOKENS["bsc"]["USDT"]["address"]
    native = [{"from": "0x" + "1" * 40, "to": "0x" + "2" * 40, "value": str(2 * 10 ** 18), "isError": "0",
               "timeStamp": "1", "hash": "0xn"}]
    tokens = [{"from": "0x" + "1" * 40, "to": "0x" + "2" * 40, "contractAddress": usdt, "value": str(7 * 10 ** 18),
               "tokenSymbol": "USDT", "timeStamp": "1", "hash": "0xt"}]
    transfers, _ = ft._normalize_evm_rows("bsc", native, tokens)
    by_tok = {t["token"]: t["amount"] for t in transfers}
    assert by_tok == {"BNB": 2.0, "USDT": 7.0}


def test_helius_parser():
    items = [{"signature": "sig1", "timestamp": 5, "nativeTransfers": [
                {"fromUserAccount": SEED_A, "toUserAccount": P1, "amount": 2_500_000_000}],
              "tokenTransfers": [
                {"fromUserAccount": SEED_A, "toUserAccount": P2, "mint": ft.TARGET_TOKENS["solana"]["USDG"]["address"], "tokenAmount": 12.5},
                {"fromUserAccount": SEED_A, "toUserAccount": P3, "mint": "SomeScamMint11111111111111111111111", "tokenAmount": 9e9}]},
             {"signature": "sig2", "timestamp": 6, "transactionError": {"x": 1},
              "nativeTransfers": [{"fromUserAccount": SEED_A, "toUserAccount": P1, "amount": 10 ** 9}]}]
    out = ft.parse_helius_transactions(items)
    assert [(t["token"], t["amount"], t["to"]) for t in out] == [("SOL", 2.5, P1), ("USDG", 12.5, P2)]


def test_solana_rpc_parser_maps_token_accounts_to_owners():
    usdc = ft.TARGET_TOKENS["solana"]["USDC"]["address"]
    src_ata, dst_ata = addr("SrcAta"), addr("DstAta")
    tx = {"meta": {"err": None,
                   "preTokenBalances": [{"accountIndex": 1, "owner": SEED_A, "mint": usdc},
                                        {"accountIndex": 2, "owner": P1, "mint": usdc}],
                   "postTokenBalances": [], "innerInstructions": []},
          "transaction": {"message": {"accountKeys": [{"pubkey": SEED_A}, {"pubkey": src_ata}, {"pubkey": dst_ata}],
                                      "instructions": [
                                          {"program": "spl-token", "parsed": {"type": "transfer", "info": {
                                              "source": src_ata, "destination": dst_ata, "amount": "25000000"}}},
                                          {"program": "system", "parsed": {"type": "transfer", "info": {
                                              "source": SEED_A, "destination": P2, "lamports": 300_000_000}}}]}}}
    out = ft.parse_solana_rpc_transaction(tx, "sigX", 1)
    assert {(t["from"], t["to"], t["token"], t["amount"]) for t in out} == {
        (SEED_A, P1, "USDC", 25.0), (SEED_A, P2, "SOL", 0.3)}


def test_expand_merges_and_reruns_detectors():
    # Start from SeedB only at depth 1: DEP is seen but not expanded -> no deposit detected yet
    fetcher = StubFetcher(SCENARIO)
    res, _ = run([SEED_B], fetcher=fetcher, depth=1)
    assert not res["clusters"]
    merged = ft.expand_graph(res, DEP, fetcher=fetcher, account_detector=NO_ACCOUNTS, chain="solana", direction="both", min_native=0.1, tokens=["SOL", "USDC"])
    assert merged["success"] and merged["expandedAddress"] == DEP
    ids = {n["id"] for n in merged["nodes"]}
    assert BINANCE in ids and SEED_B in ids
    dep = next(n for n in merged["nodes"] if n["id"] == DEP)
    assert "cex_deposit" in dep["roles"] and dep["expanded"]
    # the SEED_B -> DEP edge already existed: it must not be double counted after the merge
    e = next(e for e in merged["edges"] if e["from"] == SEED_B and e["to"] == DEP)
    assert e["amount"] == 5
    assert merged["clusters"] and merged["clusters"][0]["depositAddress"] == DEP
    assert merged["stats"]["addedNodes"] >= 1


def test_expand_ignores_client_labels():
    res, _ = run([SEED_B], depth=1)
    for n in res["nodes"]:
        n["label"] = "<script>alert(1)</script>"
    merged = ft.expand_graph(res, DEP, fetcher=StubFetcher(SCENARIO), account_detector=NO_ACCOUNTS, chain="solana", min_native=0.1)
    assert all("<script>" not in str(n["label"]) for n in merged["nodes"])


def test_single_depositor_is_not_a_cluster():
    # one wallet (plus its funders) depositing to an address is a funding tree, not a shared deposit
    transfers = [tr(SEED_A, P1, 10), tr(P1, DEP, 9), tr(DEP, BINANCE, 9)]
    res, _ = run([SEED_A], transfers=transfers, depth=3)
    assert "cex_deposit" in next(n for n in res["nodes"] if n["id"] == DEP)["roles"]
    assert res["clusters"] == [] and not finding(res, "shared_deposit")


def test_test_addresses_are_valid_base58():
    import relay_core as rc
    for a in (SEED_A, SEED_B, P1, P2, P3, DEP, SPLIT_X, DUST, USDC_DST):
        assert rc.SOLANA_ADDR_RE.match(a), a


# ---- account type (EOA vs contract) ----

def test_contract_is_marked_and_not_traversed():
    kinds = {SEED_A: "eoa", P1: "pda", DUST: "eoa"}
    res, fetcher = run([SEED_A], account_detector=lambda c, addrs: {a: kinds.get(a, "eoa") for a in addrs})
    p1 = next(n for n in res["nodes"] if n["id"] == P1)
    assert p1["account"] == "pda" and p1["type"] == "contract"
    assert P1 not in fetcher.calls and P2 not in {n["id"] for n in res["nodes"]}
    assert res["stats"]["contracts"] == 1 and res["stats"]["eoa"] >= 1


def test_seed_contract_is_still_traced():
    res, fetcher = run([SEED_A], depth=1, account_detector=lambda c, addrs: {a: "contract" for a in addrs})
    seed = next(n for n in res["nodes"] if n["id"] == SEED_A)
    assert seed["account"] == "contract" and seed["type"] == "wallet" and SEED_A in fetcher.calls


def test_smart_account_is_traversed():
    res, fetcher = run([SEED_A], depth=2, account_detector=lambda c, addrs: {a: "smart_account" for a in addrs})
    assert P1 in fetcher.calls
    assert next(n for n in res["nodes"] if n["id"] == P1)["account"] == "smart_account"


def test_detector_failure_does_not_break_trace():
    def boom(chain, addrs):
        raise RuntimeError("rpc down")
    res, _ = run([SEED_A, SEED_B], account_detector=boom)
    assert res["success"] and len(res["nodes"]) > 3


def test_classifiers():
    import relay_core as rc
    assert rc.classify_evm_code("0x") == "eoa"
    assert rc.classify_evm_code("0xef0100" + "ab" * 20) == "smart_account"
    assert rc.classify_evm_code("0x6080604052") == "contract"
    assert ft.classify_solana_account(None) == "eoa"
    assert ft.classify_solana_account({"owner": ft.SOLANA_SYSTEM_PROGRAM, "executable": False}) == "eoa"
    assert ft.classify_solana_account({"owner": "BPFLoaderUpgradeab1e11111111111111111111111", "executable": True}) == "program"
    assert ft.classify_solana_account({"owner": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "executable": False}) == "pda"


def test_detect_account_kinds_batches_and_caches(monkeypatch):
    calls = []

    def fake_batch(chain, method, params_list, timeout=10):
        calls.append(len(params_list))
        return ["0x" if p[0].endswith("1") else "0x6080" for p in params_list]

    monkeypatch.setattr(ft.rc, "rpc_batch", fake_batch)
    ft._ACCOUNT_CACHE.clear()
    addrs = ["0x" + "0" * 39 + "1", "0x" + "0" * 39 + "2"]
    assert ft.detect_account_kinds("ethereum", addrs) == {addrs[0]: "eoa", addrs[1]: "contract"}
    assert ft.detect_account_kinds("ethereum", addrs) == {addrs[0]: "eoa", addrs[1]: "contract"}
    assert calls == [2]  # second call served from cache
