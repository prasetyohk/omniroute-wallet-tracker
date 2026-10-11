"""
Multi-hop fund-flow tracing (Tab 5).

Builds a transfer graph outward from one or more seed wallets (BFS), keeping only real value
in the chain's target tokens, then runs detectors over the graph:
  * CEX deposit addresses  (a wallet that sweeps most of its outflow into a CEX / busy hub)
  * shared-deposit clusters (wallets that fund the same deposit address -> likely one owner)
  * peeling chains, consolidation points and CEX "star" hubs

Data providers (each optional key lives in the gitignored .env):
  Solana : Helius enhanced transactions (HELIUS_API_KEY)  -> fallback: public RPC (slow, capped)
  EVM    : Etherscan API v2 (ETHERSCAN_API_KEY)           -> fallback: Blockscout v1
"""
import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional, Tuple

from web3 import Web3

import relay_core as rc

HELIUS_API_KEY = rc.load_env_value("HELIUS_API_KEY")
ETHERSCAN_API_KEY = rc.load_env_value("ETHERSCAN_API_KEY")

SOL_MINT = "So11111111111111111111111111111111111111112"

# Target tokens per chain, matched by contract / mint (never by name: fake "USDT" tokens exist).
# Every contract below was checked on-chain for symbol + decimals.
TARGET_TOKENS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "solana": {
        "SOL": {"native": True, "decimals": 9},
        "USDC": {"address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "decimals": 6},
        "USDT": {"address": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", "decimals": 6},
        "USDG": {"address": "2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH", "decimals": 6},
    },
    "ethereum": {
        "ETH": {"native": True, "decimals": 18},
        "USDC": {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "decimals": 6},
        "USDT": {"address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "decimals": 6},
        "USDG": {"address": "0xe343167631d89B6Ffc58B88d6b7fB0228795491D", "decimals": 6},
    },
    "base": {
        "ETH": {"native": True, "decimals": 18},
        "USDC": {"address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "decimals": 6},
        "USDT": {"address": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2", "decimals": 6},
    },
    "arbitrum": {
        "ETH": {"native": True, "decimals": 18},
        "USDC": {"address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", "decimals": 6},
        "USDT": {"address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9", "decimals": 6},
    },
    "optimism": {
        "ETH": {"native": True, "decimals": 18},
        "USDC": {"address": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85", "decimals": 6},
        "USDT": {"address": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58", "decimals": 6},
    },
    "polygon": {
        "POL": {"native": True, "decimals": 18},
        "USDC": {"address": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359", "decimals": 6},
        "USDT": {"address": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F", "decimals": 6},
    },
    "bsc": {
        "BNB": {"native": True, "decimals": 18},
        "USDC": {"address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d", "decimals": 18},
        "USDT": {"address": "0x55d398326f99059fF775485246999027B3197955", "decimals": 18},
    },
}
SUPPORTED_CHAINS = list(TARGET_TOKENS)
ETHERSCAN_CHAIN_IDS = {"ethereum": 1, "base": 8453, "arbitrum": 42161, "optimism": 10, "polygon": 137, "bsc": 56}
STABLES = {"USDC", "USDT", "USDG"}

DEFAULT_MIN_NATIVE = {"SOL": 0.1, "ETH": 0.005, "BNB": 0.02, "POL": 20.0}
DEFAULT_MIN_STABLE_USD = 10.0

MAX_DEPTH = 4
MAX_FANOUT = 8
MAX_SEEDS = 10
MAX_NODES = 80
TIME_BUDGET_S = 75.0
HUB_COUNTERPARTIES = 40       # a wallet with this many distinct counterparties is a service/hub
DEPOSIT_SWEEP_SHARE = 0.7     # >=70% of outflow into a CEX/hub -> deposit address
PEEL_MAIN_SHARE = 0.75        # peel hop: one output carries >=75% of value, the rest splits off

TERMINAL_TYPES = {"cex", "bridge", "contract", "mixer", "hub"}


# ==================== PROVIDERS ====================
# A provider returns (transfers, meta). A transfer:
#   {"from", "to", "token", "amount", "ts", "tx"}  -- already restricted to TARGET_TOKENS
# meta: {"raw_count": int, "spoofed": int, "source": str, "limit_hit": bool}

_FETCH_CACHE: Dict[Tuple[str, str], Tuple[float, Any]] = {}
_FETCH_LOCK = threading.Lock()
FETCH_TTL = 300


def _cached(key: Tuple[str, str], fn: Callable[[], Any]) -> Any:
    now = time.time()
    with _FETCH_LOCK:
        hit = _FETCH_CACHE.get(key)
        if hit and now - hit[0] < FETCH_TTL:
            return hit[1]
    value = fn()
    if value[1].get("ok", True):
        with _FETCH_LOCK:
            if len(_FETCH_CACHE) > 2000:
                _FETCH_CACHE.pop(min(_FETCH_CACHE, key=lambda k: _FETCH_CACHE[k][0]))
            _FETCH_CACHE[key] = (now, value)
    return value


_ETHERSCAN_SUPPORT: Dict[str, bool] = {}
_ETHERSCAN_PROBE_ADDR = "0x0000000000000000000000000000000000000001"


def etherscan_supports(chain: str) -> bool:
    """Whether the configured Etherscan key may query this chain. The free tier excludes some
    chains (e.g. Base, Optimism, BNB Chain); the answer is probed once and cached."""
    if not ETHERSCAN_API_KEY or chain not in ETHERSCAN_CHAIN_IDS:
        return False
    if chain not in _ETHERSCAN_SUPPORT:
        data = rc._get_json(f"https://api.etherscan.io/v2/api?chainid={ETHERSCAN_CHAIN_IDS[chain]}&module=account"
                            f"&action=balance&address={_ETHERSCAN_PROBE_ADDR}&apikey={ETHERSCAN_API_KEY}", timeout=8)
        if data is None:
            return True  # network hiccup: try Etherscan, fetch falls back if it refuses
        _ETHERSCAN_SUPPORT[chain] = "not supported" not in str(data.get("result", "")).lower()
    return _ETHERSCAN_SUPPORT[chain]


def provider_info(chain: str) -> Dict[str, Any]:
    """Which data source will be used, and the safe limits that follow from it."""
    if chain == "solana":
        if HELIUS_API_KEY:
            return {"source": "Helius", "keyed": True, "workers": 4, "max_depth": MAX_DEPTH, "max_fanout": MAX_FANOUT}
        return {"source": "Solana public RPC", "keyed": False, "workers": 1, "max_depth": 2, "max_fanout": 3}
    if etherscan_supports(chain):
        return {"source": "Etherscan v2", "keyed": True, "workers": 4, "max_depth": MAX_DEPTH, "max_fanout": MAX_FANOUT}
    if not rc.get_chain_info(chain).get("blockscoutApi"):
        return {"source": "none", "keyed": False, "workers": 1, "max_depth": 0, "max_fanout": 0,
                "plan_required": bool(ETHERSCAN_API_KEY)}
    return {"source": "Blockscout", "keyed": False, "workers": 3, "max_depth": MAX_DEPTH, "max_fanout": MAX_FANOUT}


def _evm_token_index(chain: str) -> Tuple[Dict[str, Tuple[str, int]], str, set]:
    tokens = TARGET_TOKENS[chain]
    by_contract = {v["address"].lower(): (sym, v["decimals"]) for sym, v in tokens.items() if not v.get("native")}
    native = next(sym for sym, v in tokens.items() if v.get("native"))
    return by_contract, native, {sym for sym in tokens if sym in STABLES}


def _normalize_evm_rows(chain: str, native_rows: List[Dict[str, Any]], token_rows: List[Dict[str, Any]]):
    by_contract, native, stable_syms = _evm_token_index(chain)
    transfers, spoofed = [], 0
    for tx in native_rows:
        val = int(tx.get("value") or 0)
        if val <= 0 or str(tx.get("isError", "0")) == "1":
            continue
        transfers.append({"from": rc.to_checksum(tx.get("from", "")), "to": rc.to_checksum(tx.get("to") or ""),
                          "token": native, "amount": val / 1e18,
                          "ts": int(tx.get("timeStamp") or 0), "tx": tx.get("hash", "")})
    for ttx in token_rows:
        contract = (ttx.get("contractAddress") or "").lower()
        hit = by_contract.get(contract)
        if not hit:
            if str(ttx.get("tokenSymbol") or "").upper() in stable_syms:
                spoofed += 1  # same name as a target stablecoin, wrong contract
            continue
        sym, dec = hit
        try:
            amt = int(ttx.get("value") or 0) / (10 ** dec)
        except (TypeError, ValueError):
            continue
        if amt <= 0:
            continue
        transfers.append({"from": rc.to_checksum(ttx.get("from", "")), "to": rc.to_checksum(ttx.get("to") or ""),
                          "token": sym, "amount": amt,
                          "ts": int(ttx.get("timeStamp") or 0), "tx": ttx.get("hash", "")})
    return transfers, spoofed


EVM_PAGE = 200


def _etherscan_list(chain: str, action: str, address: str) -> Optional[List[Dict[str, Any]]]:
    url = (f"https://api.etherscan.io/v2/api?chainid={ETHERSCAN_CHAIN_IDS[chain]}&module=account&action={action}"
           f"&address={address}&page=1&offset={EVM_PAGE}&sort=desc&apikey={ETHERSCAN_API_KEY}")
    for attempt in range(3):
        data = rc._get_json(url, timeout=10)
        if isinstance(data, dict):
            if isinstance(data.get("result"), list):
                return data["result"]
            if "not supported" in str(data.get("result", "")).lower():
                _ETHERSCAN_SUPPORT[chain] = False
                return None
            if "rate limit" in str(data.get("result", "")).lower():
                time.sleep(0.6 * (attempt + 1))
                continue
        return None
    return None


def fetch_evm_transfers(chain: str, address: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    address = rc.to_checksum(address)

    def run():
        if etherscan_supports(chain):
            fetch, source = (lambda action: _etherscan_list(chain, action, address)), "Etherscan v2"
        else:
            api = rc.get_chain_info(chain).get("blockscoutApi")
            if not api:
                return [], {"ok": False, "source": "none", "raw_count": 0, "spoofed": 0, "limit_hit": False}
            def fetch(action):
                # public Blockscout throttles bursts (HTTP 429): back off briefly before giving up
                for attempt in range(3):
                    rows = rc._blockscout_list(api, action, address, EVM_PAGE, "desc")
                    if rows is not None:
                        return rows
                    time.sleep(1.2 * (attempt + 1))
                return None
            source = "Blockscout"
        f_native = rc._POOL.submit(fetch, "txlist")
        f_token = rc._POOL.submit(fetch, "tokentx")
        native_rows, token_rows = f_native.result(), f_token.result()
        ok = native_rows is not None or token_rows is not None
        transfers, spoofed = _normalize_evm_rows(chain, native_rows or [], token_rows or [])
        limit_hit = len(native_rows or []) >= EVM_PAGE or len(token_rows or []) >= EVM_PAGE
        return transfers, {"ok": ok, "source": source, "raw_count": len(native_rows or []) + len(token_rows or []),
                           "spoofed": spoofed, "limit_hit": limit_hit}

    return _cached((chain, address.lower()), run)


def _solana_mint_index() -> Dict[str, Tuple[str, int]]:
    return {v["address"]: (sym, v["decimals"]) for sym, v in TARGET_TOKENS["solana"].items() if not v.get("native")}


def parse_helius_transactions(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Helius enhanced-transaction JSON -> normalized transfers (target tokens only)."""
    mints = _solana_mint_index()
    out = []
    for tx in items or []:
        sig, ts = tx.get("signature", ""), int(tx.get("timestamp") or 0)
        if tx.get("transactionError"):
            continue
        for nt in tx.get("nativeTransfers") or []:
            amt = int(nt.get("amount") or 0) / 1e9
            if amt > 0 and nt.get("fromUserAccount") and nt.get("toUserAccount"):
                out.append({"from": nt["fromUserAccount"], "to": nt["toUserAccount"], "token": "SOL",
                            "amount": amt, "ts": ts, "tx": sig})
        for tt in tx.get("tokenTransfers") or []:
            mint = tt.get("mint")
            if mint == SOL_MINT:
                sym = "SOL"
            elif mint in mints:
                sym = mints[mint][0]
            else:
                continue
            amt = float(tt.get("tokenAmount") or 0)
            if amt > 0 and tt.get("fromUserAccount") and tt.get("toUserAccount"):
                out.append({"from": tt["fromUserAccount"], "to": tt["toUserAccount"], "token": sym,
                            "amount": amt, "ts": ts, "tx": sig})
    return out


def parse_solana_rpc_transaction(tx: Dict[str, Any], sig: str, ts: int) -> List[Dict[str, Any]]:
    """jsonParsed getTransaction -> normalized transfers. SPL token accounts are mapped to
    their owner wallets through pre/postTokenBalances."""
    mints = _solana_mint_index()
    meta = tx.get("meta") or {}
    if meta.get("err"):
        return []
    keys = rc._solana_account_keys(tx)
    owner_of, mint_of = {}, {}
    for bal in (meta.get("preTokenBalances") or []) + (meta.get("postTokenBalances") or []):
        idx = bal.get("accountIndex")
        if isinstance(idx, int) and idx < len(keys):
            if bal.get("owner"):
                owner_of[keys[idx]] = bal["owner"]
            if bal.get("mint"):
                mint_of[keys[idx]] = bal["mint"]

    instructions = list(tx.get("transaction", {}).get("message", {}).get("instructions", []))
    for inner in meta.get("innerInstructions") or []:
        instructions.extend(inner.get("instructions", []))

    out = []
    for ix in instructions:
        parsed = ix.get("parsed") if isinstance(ix, dict) else None
        if not isinstance(parsed, dict):
            continue
        info, kind = parsed.get("info", {}), parsed.get("type", "")
        if kind == "transfer" and "lamports" in info:
            amt = int(info.get("lamports") or 0) / 1e9
            if amt > 0:
                out.append({"from": info.get("source", ""), "to": info.get("destination", ""), "token": "SOL",
                            "amount": amt, "ts": ts, "tx": sig})
        elif kind in ("transfer", "transferChecked") and ix.get("program") == "spl-token":
            src, dst = info.get("source", ""), info.get("destination", "")
            mint = info.get("mint") or mint_of.get(src) or mint_of.get(dst)
            if mint == SOL_MINT:
                sym, dec = "SOL", 9
            elif mint in mints:
                sym, dec = mints[mint]
            else:
                continue
            ta = info.get("tokenAmount") or {}
            try:
                amt = float(ta["uiAmount"]) if ta.get("uiAmount") is not None else int(info.get("amount") or 0) / (10 ** dec)
            except (TypeError, ValueError):
                continue
            sender = info.get("authority") or owner_of.get(src, src)
            if amt > 0:
                out.append({"from": sender, "to": owner_of.get(dst, dst), "token": sym,
                            "amount": amt, "ts": ts, "tx": sig})
    return out


SOLANA_PUBLIC_TX_LIMIT = 15
HELIUS_PAGE = 100


def fetch_solana_transfers(chain: str, address: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    def run():
        if HELIUS_API_KEY:
            url = f"https://api-mainnet.helius-rpc.com/v0/addresses/{address}/transactions?api-key={HELIUS_API_KEY}&limit={HELIUS_PAGE}"
            items = rc._get_json(url, timeout=15)
            if not isinstance(items, list):
                return [], {"ok": False, "source": "Helius", "raw_count": 0, "spoofed": 0, "limit_hit": False}
            return parse_helius_transactions(items), {"ok": True, "source": "Helius", "raw_count": len(items),
                                                      "spoofed": 0, "limit_hit": len(items) >= HELIUS_PAGE}
        sigs = rc._rpc(rc.SOLANA_RPC, "getSignaturesForAddress", [address, {"limit": SOLANA_PUBLIC_TX_LIMIT}], 8)
        if sigs is None:
            return [], {"ok": False, "source": "Solana public RPC", "raw_count": 0, "spoofed": 0, "limit_hit": False}
        sigs = [s for s in sigs if not s.get("err")]
        txs = rc._solana_get_transactions([s["signature"] for s in sigs])
        transfers = []
        for s, tx in zip(sigs, txs):
            if tx:
                transfers.extend(parse_solana_rpc_transaction(tx, s["signature"], int(s.get("blockTime") or 0)))
        return transfers, {"ok": True, "source": "Solana public RPC", "raw_count": len(sigs), "spoofed": 0,
                           "limit_hit": len(sigs) >= SOLANA_PUBLIC_TX_LIMIT}

    return _cached((chain, address), run)


def default_fetcher(chain: str, address: str):
    return fetch_solana_transfers(chain, address) if chain == "solana" else fetch_evm_transfers(chain, address)


# ==================== GRAPH BUILD (BFS) ====================

def token_price(chain: str, sym: str) -> float:
    if sym in STABLES:
        return 1.0
    return rc.get_token_usd_price(sym)


def node_type(address: str) -> Tuple[str, Optional[str]]:
    cls = rc.classify_entity(address)
    cat = cls["category"]
    mapping = {"cex_hot_wallet": "cex", "public_faucet": "contract", "paymaster": "contract",
               "bridge_router": "bridge", "dex_router": "contract", "mixer": "mixer"}
    return mapping.get(cat, "wallet"), cls.get("name")


# ==================== ACCOUNT TYPE (EOA vs SMART CONTRACT) ====================
# EVM   : eth_getCode -> "eoa" | "smart_account" (EIP-7702 delegated EOA) | "contract"
# Solana: getMultipleAccounts owner/executable -> "eoa" (System-owned wallet) | "program" | "pda"
#         (account owned by a program: vault, pool, token/escrow account)
SOLANA_SYSTEM_PROGRAM = "11111111111111111111111111111111"
ACCOUNT_KINDS_CODE = {"contract", "program", "pda"}   # not user wallets -> not auto-traversed
_ACCOUNT_CACHE: Dict[Tuple[str, str], str] = {}


def classify_solana_account(value: Optional[Dict[str, Any]]) -> str:
    if not value:
        return "eoa"  # no account data: an unfunded/closed plain address
    if value.get("executable"):
        return "program"
    return "eoa" if value.get("owner") == SOLANA_SYSTEM_PROGRAM else "pda"


def detect_account_kinds(chain: str, addresses: List[str]) -> Dict[str, str]:
    """Batch account-type lookup (cached). Unknown/failed lookups are simply left out."""
    out: Dict[str, str] = {}
    todo = []
    for a in addresses:
        hit = _ACCOUNT_CACHE.get((chain, a))
        if hit:
            out[a] = hit
        elif a not in todo:
            todo.append(a)
    if chain == "solana":
        for i in range(0, len(todo), 100):
            chunk = todo[i:i + 100]
            res = rc.rpc_batch("solana", "getMultipleAccounts",
                               [[chunk, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}]])
            values = ((res or [None])[0] or {}).get("value")
            if isinstance(values, list) and len(values) == len(chunk):
                for a, v in zip(chunk, values):
                    out[a] = classify_solana_account(v)
    else:
        for i in range(0, len(todo), 50):
            chunk = todo[i:i + 50]
            res = rc.rpc_batch(chain, "eth_getCode", [[a, "latest"] for a in chunk])
            for a, code in zip(chunk, res or []):
                if isinstance(code, str):
                    out[a] = rc.classify_evm_code(code)
    for a in todo:
        if a in out:
            _ACCOUNT_CACHE[(chain, a)] = out[a]
    return out


def account_counts(nodes) -> Dict[str, int]:
    counts = {"eoa": 0, "contracts": 0, "smart_accounts": 0}
    for n in nodes:
        kind = n.get("account")
        if kind == "eoa":
            counts["eoa"] += 1
        elif kind == "smart_account":
            counts["smart_accounts"] += 1
        elif kind in ACCOUNT_KINDS_CODE:
            counts["contracts"] += 1
    return counts


def apply_account_kinds(nodes: Dict[str, Dict[str, Any]], kinds: Dict[str, str]) -> None:
    for addr, kind in kinds.items():
        n = nodes.get(addr)
        if not n:
            continue
        n["account"] = kind
        # An unlabelled contract / program / PDA is infrastructure: shown, but not walked through
        # automatically (DEX pools and routers would explode the graph). Seeds are always traced.
        if kind in ACCOUNT_KINDS_CODE and n["type"] == "wallet" and not n["isSeed"]:
            n["type"] = "contract"


def normalize_address(chain: str, address: str) -> Optional[str]:
    address = (address or "").strip()
    if chain == "solana":
        return address if rc.SOLANA_ADDR_RE.match(address) else None
    return Web3.to_checksum_address(address) if Web3.is_address(address) else None


def trace_flow(
    seeds: List[str],
    chain: str = "solana",
    direction: str = "forward",
    depth: int = 2,
    fanout: int = 4,
    min_native: Optional[float] = None,
    min_stable_usd: float = DEFAULT_MIN_STABLE_USD,
    tokens: Optional[List[str]] = None,
    fetcher: Callable[[str, str], Any] = default_fetcher,
    max_nodes: int = MAX_NODES,
    time_budget: float = TIME_BUDGET_S,
    workers: Optional[int] = None,
    account_detector: Optional[Callable[[str, List[str]], Dict[str, str]]] = None,
) -> Dict[str, Any]:
    started = time.time()
    detect = account_detector or detect_account_kinds
    chain = (chain or "").lower().strip()
    if chain not in TARGET_TOKENS:
        return {"success": False, "error": f"Chain '{chain}' belum didukung untuk graph tracing. / Chain not supported: {', '.join(SUPPORTED_CHAINS)}."}
    if direction not in ("forward", "backward", "both"):
        direction = "forward"

    pinfo = provider_info(chain) if fetcher is default_fetcher else {"source": "custom", "keyed": True, "workers": workers or 4,
                                                                      "max_depth": MAX_DEPTH, "max_fanout": MAX_FANOUT}
    if pinfo["max_depth"] == 0:
        return {"success": False, "error": "Chain ini butuh ETHERSCAN_API_KEY di .env (tidak ada Blockscout publik). / This chain needs ETHERSCAN_API_KEY."}
    notices = []
    depth = max(1, min(int(depth), MAX_DEPTH))
    fanout = max(1, min(int(fanout), MAX_FANOUT))
    if depth > pinfo["max_depth"] or fanout > pinfo["max_fanout"]:
        depth, fanout = min(depth, pinfo["max_depth"]), min(fanout, pinfo["max_fanout"])
        notices.append(f"limited_by_provider:{pinfo['source']}")

    clean_seeds = []
    for s in seeds[:MAX_SEEDS]:
        a = normalize_address(chain, s)
        if a and a not in clean_seeds:
            clean_seeds.append(a)
    if not clean_seeds:
        return {"success": False, "error": "Tidak ada alamat seed yang valid untuk chain ini. / No valid seed address for this chain."}

    allowed = [t for t in (tokens or list(TARGET_TOKENS[chain])) if t in TARGET_TOKENS[chain]] or list(TARGET_TOKENS[chain])
    native_sym = next(sym for sym, v in TARGET_TOKENS[chain].items() if v.get("native"))
    if min_native is None:
        min_native = DEFAULT_MIN_NATIVE.get(native_sym, 0.0)
    prices = {sym: token_price(chain, sym) for sym in allowed}

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    stats = {"fetched": 0, "fetch_failed": 0, "dust_filtered": 0, "token_filtered": 0, "spoofed": 0,
             "raw_tx": 0, "truncated": False, "truncate_reason": ""}

    def add_node(addr: str, d: int, seed: bool = False) -> bool:
        if addr in nodes:
            nodes[addr]["depth"] = min(nodes[addr]["depth"], d)
            nodes[addr]["isSeed"] = nodes[addr]["isSeed"] or seed
            return True
        if len(nodes) >= max_nodes:
            stats["truncated"], stats["truncate_reason"] = True, "node_budget"
            return False
        ntype, label = node_type(addr)
        nodes[addr] = {"id": addr, "address": addr, "type": ntype, "label": label, "depth": d, "isSeed": seed,
                       "expanded": False, "hub": False, "roles": [], "inUsd": 0.0, "outUsd": 0.0, "cex": None,
                       "account": "unknown",
                       "explorerUrl": rc.build_explorer_addr_url(rc.get_chain_info(chain).get("id"), addr)}
        return True

    for s in clean_seeds:
        add_node(s, 0, seed=True)

    def passes(t: Dict[str, Any]) -> bool:
        if t["token"] not in allowed:
            stats["token_filtered"] += 1
            return False
        if t["token"] == native_sym:
            ok = t["amount"] >= min_native
        else:
            ok = t["amount"] * prices.get(t["token"], 1.0) >= min_stable_usd
        if not ok:
            stats["dust_filtered"] += 1
        return ok

    frontier = list(clean_seeds)
    n_workers = max(1, workers or pinfo["workers"])
    for level in range(depth):
        try:
            apply_account_kinds(nodes, detect(chain, [a for a in frontier if nodes[a]["account"] == "unknown"]))
        except Exception:
            pass  # account typing is best-effort; tracing continues without it
        to_expand = [a for a in frontier if nodes[a]["type"] not in TERMINAL_TYPES and not nodes[a]["hub"]
                     and not nodes[a]["expanded"]]
        if not to_expand:
            break
        remaining = time_budget - (time.time() - started)
        if remaining <= 0:
            stats["truncated"], stats["truncate_reason"] = True, "time_budget"
            break

        results: Dict[str, Any] = {}
        with ThreadPoolExecutor(max_workers=n_workers) as ex:
            futs = {ex.submit(fetcher, chain, a): a for a in to_expand}
            try:
                for fut in as_completed(futs, timeout=remaining):
                    try:
                        results[futs[fut]] = fut.result()
                    except Exception:
                        results[futs[fut]] = ([], {"ok": False})
            except Exception:
                stats["truncated"], stats["truncate_reason"] = True, "time_budget"
                for f in futs:
                    f.cancel()

        next_frontier: List[str] = []
        for addr in to_expand:
            if addr not in results:
                continue
            transfers, meta = results[addr]
            node = nodes[addr]
            node["expanded"] = True
            stats["fetched"] += 1
            stats["raw_tx"] += meta.get("raw_count", 0)
            stats["spoofed"] += meta.get("spoofed", 0)
            if not meta.get("ok", True):
                stats["fetch_failed"] += 1
                node["roles"].append("fetch_failed")
                continue

            # aggregate per (direction, counterparty, token)
            agg: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
            counterparties = set()
            for t in transfers:
                if t["from"] == addr and t["to"] and t["to"] != addr:
                    key = ("out", t["to"], t["token"])
                elif t["to"] == addr and t["from"] and t["from"] != addr:
                    key = ("in", t["from"], t["token"])
                else:
                    continue
                counterparties.add(key[1])
                if not passes(t):
                    continue
                agg.setdefault(key, []).append(t)

            # A busy wallet (exchange / service / pool) is recorded but never traversed through.
            # Threshold scales with the page size (public Solana RPC only returns 15 txs per wallet).
            hub_threshold = min(HUB_COUNTERPARTIES, max(8, int(meta.get("raw_count", 0) * 0.6)))
            if not node["isSeed"] and meta.get("limit_hit") and len(counterparties) >= hub_threshold:
                node["hub"] = True
                node["roles"].append("hub")
                continue  # a hub is a dead end: its customers are unrelated to the seed

            # Record EVERY qualifying edge (needed for deposit detection), but only follow top-N.
            per_dir: Dict[str, List[Tuple[float, str]]] = {"out": [], "in": []}
            cp_value: Dict[Tuple[str, str], float] = {}
            for (d, cp, tok), items in agg.items():
                usd = sum(t["amount"] for t in items) * prices.get(tok, 0.0)
                cp_value[(d, cp)] = cp_value.get((d, cp), 0.0) + usd
            for (d, cp), usd in cp_value.items():
                per_dir[d].append((usd, cp))

            follow_dirs = {"forward": ["out"], "backward": ["in"], "both": ["out", "in"]}[direction]
            for d in ("out", "in"):
                ranked = sorted(per_dir[d], reverse=True)
                keep = [cp for _, cp in ranked[:fanout]] if d in follow_dirs else []
                if d == "out":
                    # Always record sweeps into a labelled CEX: needed to spot deposit addresses.
                    keep += [cp for _, cp in ranked if cp not in keep and node_type(cp)[0] == "cex"]
                for cp in keep:
                    if not add_node(cp, level + 1):
                        continue
                    for tok in allowed:
                        for t in agg.get((d, cp, tok), []):
                            src, dst = (addr, cp) if d == "out" else (cp, addr)
                            e = edges.setdefault((src, dst, tok), {"from": src, "to": dst, "token": tok, "amount": 0.0,
                                                                  "usd": 0.0, "count": 0, "tx": t["tx"], "ts": t["ts"],
                                                                  "_seen": set()})
                            # the same transfer is seen again when its other endpoint is expanded
                            tkey = (t["tx"], round(t["amount"], 9))
                            if tkey in e["_seen"]:
                                continue
                            e["_seen"].add(tkey)
                            e["amount"] += t["amount"]
                            e["usd"] += t["amount"] * prices.get(tok, 0.0)
                            e["count"] += 1
                            if t["ts"] and (not e["ts"] or t["ts"] < e["ts"]):
                                e["ts"], e["tx"] = t["ts"], t["tx"]
                    if cp not in next_frontier and not nodes[cp]["expanded"]:
                        next_frontier.append(cp)
        frontier = next_frontier

    try:
        apply_account_kinds(nodes, detect(chain, [a for a, n in nodes.items() if n["account"] == "unknown"]))
    except Exception:
        pass

    # volumes
    for e in edges.values():
        if e["from"] in nodes:
            nodes[e["from"]]["outUsd"] += e["usd"]
        if e["to"] in nodes:
            nodes[e["to"]]["inUsd"] += e["usd"]

    findings, clusters = run_detectors(nodes, edges, clean_seeds)

    explorer_tx = lambda h: rc.build_explorer_tx_url(rc.get_chain_info(chain).get("id"), h)  # noqa: E731
    edge_list = []
    for e in edges.values():
        e.pop("_seen", None)
        edge_list.append({**e, "amount": round(e["amount"], 6), "usd": round(e["usd"], 2), "txUrl": explorer_tx(e["tx"])})
    edge_list.sort(key=lambda x: -x["usd"])
    for n in nodes.values():
        n["inUsd"], n["outUsd"] = round(n["inUsd"], 2), round(n["outUsd"], 2)

    return {
        "success": True,
        "chain": chain,
        "chainName": rc.get_chain_info(chain).get("displayName", chain),
        "direction": direction,
        "depth": depth,
        "fanout": fanout,
        "seeds": clean_seeds,
        "tokens": allowed,
        "minNative": min_native,
        "nativeSymbol": native_sym,
        "minStableUsd": min_stable_usd,
        "provider": pinfo["source"],
        "providerKeyed": pinfo["keyed"],
        "notices": notices,
        "nodes": list(nodes.values()),
        "edges": edge_list,
        "findings": findings,
        "clusters": clusters,
        "stats": {**stats, "nodes": len(nodes), "edges": len(edge_list), **account_counts(nodes.values()),
                  "elapsed_ms": int((time.time() - started) * 1000)},
    }


DETECTOR_ROLES = {"cex_deposit", "consolidation", "peel"}
MAX_GRAPH_NODES = 300


def expand_graph(graph: Dict[str, Any], address: str, fetcher: Callable[[str, str], Any] = default_fetcher,
                 account_detector: Optional[Callable[[str, List[str]], Dict[str, str]]] = None,
                 **params: Any) -> Dict[str, Any]:
    """Trace one more hop from `address` and merge it into an existing graph, then re-run every
    detector on the merged graph (a cluster can span the old and the new part)."""
    chain = (params.get("chain") or graph.get("chain") or "").lower()
    params = {**params, "chain": chain, "depth": 1}
    detect = account_detector or detect_account_kinds
    sub = trace_flow([address], fetcher=fetcher, account_detector=detect, **params)
    if not sub.get("success"):
        return sub

    seeds = [s for s in graph.get("seeds") or [] if normalize_address(chain, s)]
    nodes: Dict[str, Dict[str, Any]] = {}
    for n in (graph.get("nodes") or [])[:MAX_GRAPH_NODES]:
        addr = normalize_address(chain, n.get("id", ""))
        if not addr:
            continue
        ntype, label = node_type(addr)  # never trust labels echoed back by the client
        nodes[addr] = {"id": addr, "address": addr, "type": ntype, "label": label,
                       "depth": int(n.get("depth") or 0), "isSeed": addr in seeds,
                       "expanded": bool(n.get("expanded")), "hub": bool(n.get("hub")),
                       "roles": [r for r in n.get("roles") or [] if r in ("hub", "fetch_failed")],
                       "inUsd": 0.0, "outUsd": 0.0, "cex": None, "account": "unknown",
                       "explorerUrl": rc.build_explorer_addr_url(rc.get_chain_info(chain).get("id"), addr)}
    base_depth = nodes.get(sub["seeds"][0], {}).get("depth", 0)

    for n in sub["nodes"]:
        if n["id"] in nodes:
            old = nodes[n["id"]]
            old["expanded"] = old["expanded"] or n["expanded"]
            old["hub"] = old["hub"] or n["hub"]
            old["roles"] = sorted(set(old["roles"]) | ({"hub", "fetch_failed"} & set(n["roles"])))
        elif len(nodes) < MAX_GRAPH_NODES:
            nodes[n["id"]] = {**n, "depth": base_depth + n["depth"], "isSeed": False, "cex": None,
                              "roles": [r for r in n["roles"] if r not in DETECTOR_ROLES], "clusters": []}

    edges: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for e in list(graph.get("edges") or []) + sub["edges"]:
        src, dst = normalize_address(chain, e.get("from", "")), normalize_address(chain, e.get("to", ""))
        tok = str(e.get("token", ""))
        if not src or not dst or src not in nodes or dst not in nodes or tok not in TARGET_TOKENS[chain]:
            continue
        key = (src, dst, tok)
        if key not in edges:  # an edge already in the graph keeps its original totals
            edges[key] = {"from": src, "to": dst, "token": tok, "amount": float(e.get("amount") or 0),
                          "usd": float(e.get("usd") or 0), "count": int(e.get("count") or 0),
                          "tx": str(e.get("tx") or ""), "ts": int(e.get("ts") or 0), "txUrl": e.get("txUrl", "")}

    try:  # cached lookups: only nodes never seen before cost an RPC call
        apply_account_kinds(nodes, detect(chain, [a for a, n in nodes.items() if n.get("account", "unknown") == "unknown"]))
    except Exception:
        pass
    for n in nodes.values():
        n["roles"] = [r for r in n["roles"] if r not in DETECTOR_ROLES]
        n["clusters"], n["cex"], n["inUsd"], n["outUsd"] = [], None, 0.0, 0.0
    for e in edges.values():
        nodes[e["from"]]["outUsd"] += e["usd"]
        nodes[e["to"]]["inUsd"] += e["usd"]
    findings, clusters = run_detectors(nodes, edges, seeds)
    for n in nodes.values():
        n["inUsd"], n["outUsd"] = round(n["inUsd"], 2), round(n["outUsd"], 2)

    edge_list = sorted(edges.values(), key=lambda x: -x["usd"])
    return {**sub, "seeds": seeds or sub["seeds"], "expandedAddress": sub["seeds"][0],
            "nodes": list(nodes.values()), "edges": edge_list, "findings": findings, "clusters": clusters,
            "stats": {**sub["stats"], "nodes": len(nodes), "edges": len(edge_list), **account_counts(nodes.values()),
                      "addedNodes": len(nodes) - len(graph.get("nodes") or [])}}


# ==================== DETECTORS ====================

def run_detectors(nodes: Dict[str, Dict[str, Any]], edges: Dict[Tuple[str, str, str], Dict[str, Any]],
                  seeds: List[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    out_edges: Dict[str, List[Dict[str, Any]]] = {}
    in_edges: Dict[str, List[Dict[str, Any]]] = {}
    for e in edges.values():
        out_edges.setdefault(e["from"], []).append(e)
        in_edges.setdefault(e["to"], []).append(e)

    def sink_name(addr: str) -> Optional[str]:
        n = nodes.get(addr)
        if not n:
            return None
        if n["type"] == "cex":
            return n["label"] or "CEX"
        if n["hub"]:
            return "Service / likely CEX hot wallet"
        return None

    findings: List[Dict[str, Any]] = []

    # 1) CEX deposit addresses
    deposits: Dict[str, Dict[str, Any]] = {}
    for addr, n in nodes.items():
        if n["type"] != "wallet" or n["hub"]:
            continue
        outs = out_edges.get(addr, [])
        total = sum(e["usd"] for e in outs)
        if total <= 0:
            continue
        by_sink: Dict[str, float] = {}
        for e in outs:
            name = sink_name(e["to"])
            if name:
                by_sink[e["to"]] = by_sink.get(e["to"], 0.0) + e["usd"]
        if not by_sink:
            continue
        sink, sink_usd = max(by_sink.items(), key=lambda kv: kv[1])
        if sink_usd / total >= DEPOSIT_SWEEP_SHARE:
            n["roles"].append("cex_deposit")
            n["cex"] = sink_name(sink)
            deposits[addr] = {"address": addr, "cex": n["cex"], "cexAddress": sink,
                              "share": round(sink_usd / total * 100, 1), "sweptUsd": round(sink_usd, 2)}
            findings.append({"type": "cex_deposit", "severity": "info", "nodes": [addr, sink],
                             "cex": n["cex"], "share": deposits[addr]["share"], "usd": round(sink_usd, 2)})

    # 2) Shared-deposit clusters: wallets upstream of the same deposit address
    clusters = []
    for dep, info in deposits.items():
        direct = sorted({e["from"] for e in in_edges.get(dep, []) if nodes.get(e["from"], {}).get("type") == "wallet"
                         and not nodes[e["from"]]["hub"]})
        upstream = set(direct)
        frontier = list(direct)
        for _ in range(3):  # up to 3 hops above the deposit address
            nxt = []
            for a in frontier:
                for e in in_edges.get(a, []):
                    src = e["from"]
                    sn = nodes.get(src)
                    if sn and sn["type"] == "wallet" and not sn["hub"] and src not in upstream and src != dep:
                        upstream.add(src)
                        nxt.append(src)
            frontier = nxt
        members = [{"address": a, "relation": "direct" if a in direct else "upstream",
                    "confidence": 90 if a in direct else 60, "isSeed": a in seeds} for a in sorted(upstream)]
        seed_members = [m["address"] for m in members if m["isSeed"]]
        # A cluster needs >=2 wallets depositing into the same address (or >=2 seeds converging on it).
        # One depositor plus its own funders is just that depositor's funding tree.
        if len(direct) < 2 and len(seed_members) < 2:
            continue
        cluster = {"id": f"C{len(clusters) + 1}", "depositAddress": dep, "cex": info["cex"],
                   "cexAddress": info["cexAddress"], "members": members,
                   "seedsInCluster": seed_members, "multiSeed": len(seed_members) >= 2}
        clusters.append(cluster)
        for m in members:
            nodes[m["address"]].setdefault("clusters", []).append(cluster["id"])
        nodes[dep].setdefault("clusters", []).append(cluster["id"])
        findings.append({"type": "shared_deposit", "severity": "high", "nodes": [dep] + [m["address"] for m in members],
                         "cluster": cluster["id"], "cex": info["cex"], "count": len(members),
                         "multiSeed": cluster["multiSeed"]})

    # 3) CEX star: one CEX/hub fed by >=2 deposit addresses
    by_cex: Dict[str, List[str]] = {}
    for dep, info in deposits.items():
        by_cex.setdefault(info["cexAddress"], []).append(dep)
    for cex_addr, deps in by_cex.items():
        if len(deps) >= 2:
            findings.append({"type": "cex_star", "severity": "medium", "nodes": [cex_addr] + deps,
                             "cex": sink_name(cex_addr), "count": len(deps)})

    # 4) Consolidation: >=3 traced wallets paying into one wallet
    for addr, n in nodes.items():
        if n["type"] != "wallet" or n["hub"]:
            continue
        srcs = {e["from"] for e in in_edges.get(addr, []) if nodes.get(e["from"], {}).get("type") == "wallet"}
        if len(srcs) >= 3:
            n["roles"].append("consolidation")
            findings.append({"type": "consolidation", "severity": "medium", "nodes": [addr] + sorted(srcs),
                             "count": len(srcs), "usd": round(sum(e["usd"] for e in in_edges.get(addr, [])), 2)})

    # 5) Peeling chains: >=3 consecutive hops where one output carries most value and a smaller one splits off
    def peel_next(addr: str) -> Optional[str]:
        outs = out_edges.get(addr, [])
        if len(outs) < 2:
            return None
        by_dst: Dict[str, float] = {}
        for e in outs:
            by_dst[e["to"]] = by_dst.get(e["to"], 0.0) + e["usd"]
        if len(by_dst) < 2:
            return None
        total = sum(by_dst.values())
        dst, usd = max(by_dst.items(), key=lambda kv: kv[1])
        if total > 0 and usd / total >= PEEL_MAIN_SHARE and nodes.get(dst, {}).get("type") == "wallet":
            return dst
        return None

    reported: set = set()
    for start in nodes:
        if start in reported or nodes[start]["type"] != "wallet":
            continue
        path, cur = [start], start
        while True:
            nxt = peel_next(cur)
            if not nxt or nxt in path:
                break
            path.append(nxt)
            cur = nxt
        hops = len(path) - 1
        if hops >= 3 and not any(p in reported for p in path):
            reported.update(path)
            for p in path[:-1]:
                if "peel" not in nodes[p]["roles"]:
                    nodes[p]["roles"].append("peel")
            findings.append({"type": "peeling_chain", "severity": "medium", "nodes": path, "count": hops})

    order = {"high": 0, "medium": 1, "info": 2}
    findings.sort(key=lambda f: order.get(f["severity"], 3))
    return findings, clusters


def edge_log_width(usd: float) -> float:
    """Helper mirrored in the UI: edge thickness grows with log10(USD)."""
    return 1 + 2 * math.log10(max(usd, 1))
