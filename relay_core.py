import re
import time
import threading
from functools import lru_cache
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional, List
from web3 import Web3

# ==================== SHARED NETWORK LAYER ====================
# One pooled keep-alive session for every outbound HTTP call (APIs + JSON-RPC).
HTTP = requests.Session()
_adapter = HTTPAdapter(
    pool_connections=32,
    pool_maxsize=32,
    # No Retry-After sleeping: a throttled public RPC can ask for 10s+; callers pace their own retries.
    max_retries=Retry(total=1, backoff_factor=0.3, status_forcelist=[502, 503], allowed_methods=None,
                      respect_retry_after_header=False),
)
HTTP.mount("https://", _adapter)
HTTP.mount("http://", _adapter)
HTTP.headers.update({"User-Agent": "Mozilla/5.0 (OmniRoute)"})

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
SOLANA_ADDR_RE = re.compile(r"^(?!0x)[1-9A-HJ-NP-Za-km-z]{32,44}$")
SOURCE_DOWN_ERROR = ("Sumber data (Blockscout) tidak merespons — kemungkinan rate-limit. Coba lagi dalam 1 menit. "
                     "/ Data source (Blockscout) did not respond — likely rate-limited. Try again in a minute.")


def _get_json(url: str, timeout: float = 7, **kwargs) -> Optional[Any]:
    """GET returning parsed JSON on HTTP 200, else None. Never raises."""
    try:
        r = HTTP.get(url, timeout=timeout, **kwargs)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def _rpc(url: str, method: str, params: list, timeout: float = 6) -> Optional[Any]:
    """Single JSON-RPC call returning `result`, else None. Never raises."""
    try:
        r = HTTP.post(url, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=timeout)
        if r.status_code == 200:
            return r.json().get("result")
    except Exception:
        pass
    return None


@lru_cache(maxsize=64)
def get_web3(rpc_url: Optional[str]) -> Optional[Web3]:
    """Cached Web3 instance per RPC URL (reuses the pooled session)."""
    if not rpc_url:
        return None
    provider = Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 5}, session=HTTP, exception_retry_configuration=None)
    return Web3(provider)


def to_checksum(addr: str) -> str:
    return Web3.to_checksum_address(addr) if addr and Web3.is_address(addr) else addr


def _fmt_amount(raw: Any, decimals: Any) -> str:
    """Format raw integer token amount with decimals into a human string."""
    try:
        val = int(raw) / (10 ** int(decimals))
        return f"{val:,.4f}".rstrip("0").rstrip(".")
    except Exception:
        return str(raw)

# Known DEX / Bridge / CEX / Cross-Chain Routers Database
POPULAR_ROUTERS = {
    # Relay.link Depository / Routers / Solvers
    "0x4cD00E387622C35bDDB9b4c962C136462338BC31": "Relay: Solver / Depository (Robinhood Chain)",
    "0xb92fe925dc43a0ecde6c8b1a2709c170ec4fff4f": "Relay: ERC20 Router",
    "0xccc88a9d1b4ed6b0eaba998850414b24f1c315be": "Relay: Approval Proxy",
    "0xf70da97812cb96acdf810712aa562db8dfa3dbef": "Relay: Cross-Chain Solver",
    
    # Li.Fi & Jumper Exchange
    "0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE": "Li.Fi Diamond Proxy (Jumper Exchange)",
    "0x341e94069f53234fE6DabeF707aD424830525715": "Li.Fi Diamond Proxy (Arbitrum)",
    
    # Across Protocol
    "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5": "Across V2 SpokePool",
    "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64": "Across V3 SpokePool (Arbitrum)",
    "0xe0B01066d730601417079290b9855D186660591E": "Across V3 SpokePool (Base)",
    
    # Stargate / LayerZero
    "0x8731d54E9D02c286767d56ac03e8037C07e01e98": "Stargate Router (Base)",
    "0x53Bf833A5d6C4ddA888F69c22C88C9f356a41614": "Stargate Router (Arbitrum)",
    "0x45A01E4e04F14f7A4a6702c74187c5F6222033cd": "Stargate Router (Optimism)",
    "0x296F55F8Fb28E498B858d0ADDA062F55B3402095": "Stargate Router (Ethereum)",
    
    # Uniswap
    "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45": "Uniswap Universal Router / SwapRouter02",
    "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD": "Uniswap Universal Router (Latest)",
    "0xE592427A0AEce92De3Edee1F18E0157C05861564": "Uniswap V3 SwapRouter",
    
    # 1inch
    "0x1111111254EEB25477B68fb85Ed929f73A960582": "1inch Aggregation Router V5",
    "0x111111125421cA6dc452d289314280a0f8842A65": "1inch Aggregation Router V6",
    
    # 0x Project
    "0xdef1c0ded9bec7f1a1670819833240f027b25eff": "0x Exchange Proxy",
    
    # CoW Swap
    "0x9008D19f58AAbD9eD0D60971565AA8510560ab41": "CoW Protocol GPv2Settlement"
}

# Known Centralized Exchanges (CEX), Faucets, Bridges, Paymasters & Mixers Database
KNOWN_ENTITIES = {
    # Binance Hot Wallets
    "0x28C6c06298d514Db089934071355E5743bf21d60": {"name": "Binance Hot Wallet 14", "type": "cex_hot_wallet", "is_noisy": True},
    "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549": {"name": "Binance Hot Wallet 15", "type": "cex_hot_wallet", "is_noisy": True},
    "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d": {"name": "Binance Hot Wallet 16", "type": "cex_hot_wallet", "is_noisy": True},
    "0xF977814e90dA44bFA03b6295A0616a897441aceC": {"name": "Binance Hot Wallet 8", "type": "cex_hot_wallet", "is_noisy": True},
    "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8": {"name": "Binance Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0x8894e0a0c962cb723c1976a4421c95949be2d4e3": {"name": "Binance Hot Wallet 6", "type": "cex_hot_wallet", "is_noisy": True},
    "0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503": {"name": "Binance Hot Wallet 19", "type": "cex_hot_wallet", "is_noisy": True},
    # OKX
    "0x6cC5F688a304C3b60Ab610705E5907A6a8dBEe63": {"name": "OKX Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0x5041ed759Dd4aFfc3a72b8192C143F5295774143": {"name": "OKX Hot Wallet 2", "type": "cex_hot_wallet", "is_noisy": True},
    "0x204f9922ab4361fA8398695727B27b1407812e91": {"name": "OKX Deposit Gateway", "type": "cex_hot_wallet", "is_noisy": True},
    "0xa7efae728d2936e78bda97dc267687568dd593f3": {"name": "OKX Hot Wallet 3", "type": "cex_hot_wallet", "is_noisy": True},
    # Bybit
    "0xf89d7b9c379f64923e1B2E05d0B6bA8A3b7c7689": {"name": "Bybit Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0x1db93e1fc801a613296c0d89e7e721a938676d1e": {"name": "Bybit Deposit Address", "type": "cex_hot_wallet", "is_noisy": True},
    "0xee5b5b9230e774020a16c7cf65bc3e2cb5f69f2e": {"name": "Bybit Hot Wallet 2", "type": "cex_hot_wallet", "is_noisy": True},
    # Coinbase
    "0x503828976D22510aad0201ac7EC88293211D23Da": {"name": "Coinbase Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0xA9D1e08C7793af67e9d92fe308d5697FB81d3E43": {"name": "Coinbase Prime", "type": "cex_hot_wallet", "is_noisy": True},
    "0x71660c4005ba85c37ccec55d0c4493e66fe775d3": {"name": "Coinbase Hot Wallet 2", "type": "cex_hot_wallet", "is_noisy": True},
    "0xd61e1b12b304620023ee45155f818ecad01050e0": {"name": "Coinbase Base Bridge Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    # KuCoin, Gate.io, MEXC, Bitget
    "0xd6216fC19DB775Df9777a4CEa83F204C4d9D1314": {"name": "KuCoin Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0x0D0707963952f2fBA59dD06f2b425ace40b492Fe": {"name": "Gate.io Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0x75e89d5979e4f6fba9f97c104c2f0afb3f1dcb88": {"name": "MEXC Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    "0x0419e5967664687635952f411624c965e6bb8f01": {"name": "Bitget Hot Wallet", "type": "cex_hot_wallet", "is_noisy": True},
    # Public Faucets & Aggregator Dispensers
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": {"name": "Uniswap Governance / Faucet", "type": "public_faucet", "is_noisy": True},
    "0x4b16c5de96eb2117bbe5fd171e4d203624b014aa": {"name": "Coinbase Faucet Base", "type": "public_faucet", "is_noisy": True},
    "0xa39d2da7cbcfb9baebf5df4156637e614fe3ef4a": {"name": "Superchain Faucet", "type": "public_faucet", "is_noisy": True},
    "0xe592427a0aece92de3edee1f18e0157c05861564": {"name": "Uniswap V3 SwapRouter", "type": "dex_router", "is_noisy": True},
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45": {"name": "Uniswap Universal Router", "type": "dex_router", "is_noisy": True},
    # Base Gasless Paymasters / ERC-4337 EntryPoints
    "0x0000000000400CdFef5E2714E63d8047b8c06ac4": {"name": "Base Gasless Paymaster", "type": "paymaster", "is_noisy": True},
    "0x5ff137d4b0fdcd49dca30c7cf57e578a026d2789": {"name": "ERC-4337 EntryPoint V0.6", "type": "paymaster", "is_noisy": True},
    "0x0000000071727De22E5E9d8BAf0edAc6f37da032": {"name": "ERC-4337 EntryPoint V0.7", "type": "paymaster", "is_noisy": True},
    # Mixers (Tornado Cash - High Risk, not noisy)
    "0x722122dF12D4e14e13Ac3b6895a86e84145b6967": {"name": "Tornado.Cash: Governance", "type": "mixer", "is_noisy": False},
    "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b": {"name": "Tornado.Cash: Router", "type": "mixer", "is_noisy": False},
    "0x47CE0C6eD5B0Ce3d3A51fdb1C52DC66a7c3c2936": {"name": "Tornado.Cash: 0.1 ETH", "type": "mixer", "is_noisy": False},
    "0x910Cbd523D972eb0a6f4cAe4618aD62622b39DbF": {"name": "Tornado.Cash: 1 ETH", "type": "mixer", "is_noisy": False}
}

_BRIDGE_KEYWORDS = ("Relay", "Across", "Li.Fi", "Stargate")


def _build_entity_index() -> Dict[str, Dict[str, Any]]:
    """Lowercase address -> classification, built once for O(1) lookups."""
    idx: Dict[str, Dict[str, Any]] = {}
    for k, name in POPULAR_ROUTERS.items():
        cat = "bridge_router" if any(p in name for p in _BRIDGE_KEYWORDS) else "dex_router"
        idx[k.lower()] = {"is_noisy": True, "name": name, "category": cat}
    # KNOWN_ENTITIES wins over routers when both list an address
    for k, v in KNOWN_ENTITIES.items():
        idx[k.lower()] = {"is_noisy": v.get("is_noisy", False), "name": v.get("name"), "category": v.get("type", "unknown")}
    return idx


_ENTITY_INDEX = _build_entity_index()


def classify_entity(address: str) -> Dict[str, Any]:
    """
    Classifies address into noisy institutional infrastructure vs private EOA.
    category: cex_hot_wallet | public_faucet | paymaster | bridge_router | dex_router | mixer | private_eoa
    """
    if not address:
        return {"is_noisy": False, "name": None, "category": "unknown"}
    hit = _ENTITY_INDEX.get(address.lower())
    if hit:
        return dict(hit)
    return {"is_noisy": False, "name": None, "category": "private_eoa"}


def router_label(address: str, default: str = "") -> str:
    hit = _ENTITY_INDEX.get((address or "").lower())
    return hit["name"] if hit else default

# Static fallback chains info with public RPCs & Explorers
DEFAULT_CHAINS_INFO = {
    4663: {
        "id": 4663,
        "name": "robinhood",
        "displayName": "Robinhood Chain",
        "explorerUrl": "https://robin.etherscan.io",
        "blockscoutApi": "",
        "rpc": "https://rpc.mainnet.chain.robinhood.com",
        "nativeCurrency": {"symbol": "ETH", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/4663/light.png"
    },
    792703809: {
        "id": 792703809,
        "name": "solana",
        "displayName": "Solana",
        "explorerUrl": "https://solscan.io",
        "blockscoutApi": "",
        "rpc": "https://api.mainnet-beta.solana.com",
        "nativeCurrency": {"symbol": "SOL", "decimals": 9},
        "iconUrl": "https://assets.relay.link/icons/792703809/light.png"
    },
    1: {
        "id": 1,
        "name": "ethereum",
        "displayName": "Ethereum",
        "explorerUrl": "https://etherscan.io",
        "blockscoutApi": "https://eth.blockscout.com/api",
        "rpc": "https://ethereum-rpc.publicnode.com",
        "nativeCurrency": {"symbol": "ETH", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/1/light.png"
    },
    42161: {
        "id": 42161,
        "name": "arbitrum",
        "displayName": "Arbitrum One",
        "explorerUrl": "https://arbiscan.io",
        "blockscoutApi": "https://arbitrum.blockscout.com/api",
        "rpc": "https://arb1.arbitrum.io/rpc",
        "nativeCurrency": {"symbol": "ETH", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/42161/light.png"
    },
    8453: {
        "id": 8453,
        "name": "base",
        "displayName": "Base",
        "explorerUrl": "https://basescan.org",
        "blockscoutApi": "https://base.blockscout.com/api",
        "rpc": "https://mainnet.base.org",
        "nativeCurrency": {"symbol": "ETH", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/8453/light.png"
    },
    56: {
        "id": 56,
        "name": "bsc",
        "displayName": "BNB Chain",
        "explorerUrl": "https://bscscan.com",
        "blockscoutApi": "",
        "rpc": "https://bsc-rpc.publicnode.com",
        "nativeCurrency": {"symbol": "BNB", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/56/light.png"
    },
    10: {
        "id": 10,
        "name": "optimism",
        "displayName": "Optimism",
        "explorerUrl": "https://optimistic.etherscan.io",
        "blockscoutApi": "https://optimism.blockscout.com/api",
        "rpc": "https://mainnet.optimism.io",
        "nativeCurrency": {"symbol": "ETH", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/10/light.png"
    },
    137: {
        "id": 137,
        "name": "polygon",
        "displayName": "Polygon",
        "explorerUrl": "https://polygonscan.com",
        "blockscoutApi": "https://polygon.blockscout.com/api",
        "rpc": "https://polygon-bor-rpc.publicnode.com",
        "nativeCurrency": {"symbol": "POL", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/137/light.png"
    },
    43114: {
        "id": 43114,
        "name": "avalanche",
        "displayName": "Avalanche",
        "explorerUrl": "https://snowtrace.io",
        "blockscoutApi": "",
        "rpc": "https://api.avax.network/ext/bc/C/rpc",
        "nativeCurrency": {"symbol": "AVAX", "decimals": 18},
        "iconUrl": "https://assets.relay.link/icons/43114/light.png"
    }
}

_CHAINS_TTL = 3600
_chains_lock = threading.Lock()
_chains_state: Dict[str, Any] = {"ts": 0.0, "by_id": {}, "by_name": {}}


def get_all_chains() -> Dict[int, Dict[str, Any]]:
    """Static defaults merged with Relay's live chain list (cached 1h, thread-safe)."""
    if _chains_state["by_id"] and time.time() - _chains_state["ts"] < _CHAINS_TTL:
        return _chains_state["by_id"]
    with _chains_lock:
        if _chains_state["by_id"] and time.time() - _chains_state["ts"] < _CHAINS_TTL:
            return _chains_state["by_id"]
        merged = {cid: dict(info) for cid, info in DEFAULT_CHAINS_INFO.items()}
        data = _get_json("https://api.relay.link/chains", timeout=4) or {}
        for c in data.get("chains", []):
            cid = c.get("id")
            if not cid:
                continue
            base = merged.get(cid, {})
            currency = c.get("currency") or {}
            merged[cid] = {
                "id": cid,
                "name": c.get("name") or base.get("name", ""),
                "displayName": c.get("displayName") or c.get("name") or base.get("displayName", str(cid)),
                "explorerUrl": c.get("explorerUrl") or base.get("explorerUrl", ""),
                # keep our known-good public RPC when we have one
                "rpc": base.get("rpc") or c.get("httpRpcUrl", ""),
                "iconUrl": c.get("iconUrl") or base.get("iconUrl", ""),
                "nativeCurrency": base.get("nativeCurrency") or {"symbol": currency.get("symbol", "ETH"), "decimals": currency.get("decimals", 18)},
                "blockscoutApi": base.get("blockscoutApi", ""),
            }
        by_name: Dict[str, Dict[str, Any]] = {}
        for info in merged.values():
            for key in (info.get("displayName", ""), info.get("name", "")):
                if key:
                    by_name[key.lower()] = info
        _chains_state.update(ts=time.time() if data else time.time() - _CHAINS_TTL + 60, by_id=merged, by_name=by_name)
        return merged


def get_chain_info(chain_id_or_name: Any) -> Dict[str, Any]:
    chains = get_all_chains()
    try:
        cid = int(chain_id_or_name)
        if cid in chains:
            return chains[cid]
    except (ValueError, TypeError):
        pass

    hit = _chains_state["by_name"].get(str(chain_id_or_name).lower().strip())
    if hit:
        return hit

    return {
        "id": chain_id_or_name,
        "name": str(chain_id_or_name),
        "displayName": str(chain_id_or_name).capitalize(),
        "explorerUrl": "",
        "rpc": "",
        "iconUrl": "",
        "blockscoutApi": ""
    }

def clean_input(raw_input: str) -> Dict[str, Any]:
    s = raw_input.strip()

    tx_url_match = re.search(r'/tx/(0x[a-fA-F0-9]{64}|[1-9A-HJ-NP-Za-km-z]{64,88})', s)
    if tx_url_match:
        return {"type": "tx_hash", "value": tx_url_match.group(1), "original_url": s}

    addr_url_match = re.search(r'/address/(0x[a-fA-F0-9]{40}|[1-9A-HJ-NP-Za-km-z]{32,44})', s)
    if addr_url_match:
        return {"type": "address", "value": addr_url_match.group(1), "original_url": s}

    if re.match(r'^0x[a-fA-F0-9]{64}$', s):
        return {"type": "tx_hash", "value": s, "original_url": ""}

    if re.match(r'^[1-9A-HJ-NP-Za-km-z]{80,90}$', s):
        return {"type": "tx_hash", "value": s, "original_url": ""}

    if re.match(r'^0x[a-fA-F0-9]{40}$', s):
        return {"type": "address", "value": s, "original_url": ""}

    if re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', s):
        return {"type": "address", "value": s, "original_url": ""}

    return {"type": "raw", "value": s, "original_url": ""}

def build_explorer_tx_url(chain_id: Any, tx_hash: str) -> str:
    cinfo = get_chain_info(chain_id)
    base = cinfo.get("explorerUrl", "")
    if not base:
        return ""
    base = base.rstrip("/")
    return f"{base}/tx/{tx_hash}"

def build_explorer_addr_url(chain_id: Any, address: str) -> str:
    cinfo = get_chain_info(chain_id)
    base = cinfo.get("explorerUrl", "")
    if not base:
        return ""
    base = base.rstrip("/")
    if str(chain_id) == "792703809" or str(chain_id).lower() == "solana" or "solscan" in base:
        return f"{base}/account/{address}"
    return f"{base}/address/{address}"

def get_entity_label(address: str) -> Optional[str]:
    """Identify CEX, Bridge, DEX, or Mixer label for an address."""
    return router_label(address) or None

# ==================== PROTOCOL RESOLVERS ====================

def _chain_side(chain_id: Any, info: Dict[str, Any], tx_hash: str, fallback_name: str = "") -> Dict[str, Any]:
    """Common origin/destination block shared by every resolver."""
    if info.get("displayName"):
        display = info["displayName"]
    elif fallback_name:
        display = fallback_name.capitalize()
    else:
        display = f"Chain {chain_id}" if chain_id else "Pending"
    return {
        "id": chain_id,
        "name": info.get("name") or fallback_name or "Unknown",
        "display_name": display,
        "icon": info.get("iconUrl", ""),
        "tx_hash": tx_hash,
        "tx_explorer_url": build_explorer_tx_url(chain_id, tx_hash) if chain_id and tx_hash else "",
    }


def _asset(symbol: str, name: str, amount: str, usd: Any = None, raw: Any = "") -> Dict[str, Any]:
    return {"symbol": symbol, "name": name, "amount": amount, "amount_usd": usd, "raw_amount": raw}


def _parse_relay_request(req: Dict[str, Any], tx_hash: str = "") -> Dict[str, Any]:
    """Convert one Relay `requests/v2` item into the unified route schema (no network)."""
    protocol = req.get("protocol", {})
    deposit = protocol.get("deposit", {})
    origin = deposit.get("origin", {})
    relay_deposit = deposit.get("relay", {})
    destination = protocol.get("settlement", {}).get("destination", {})

    from_wallet = req.get("user") or origin.get("depositor") or ""
    to_wallet = req.get("recipient") or ""
    depository = origin.get("depository") or ""

    origin_chain_id = origin.get("chainId")
    origin_tx = origin.get("transactionId") or tx_hash
    origin_info = get_chain_info(origin_chain_id)

    req_data = req.get("data", {})
    metadata = req_data.get("metadata", {})
    curr_in = metadata.get("currencyIn", {})
    curr_out = metadata.get("currencyOut", {})

    dest_chain_id, dest_tx = None, ""
    fills = destination.get("fills", [])
    out_txs = req_data.get("outTxs", [])
    if fills:
        dest_chain_id, dest_tx = fills[0].get("chainId"), fills[0].get("transactionId") or ""
    elif out_txs:
        dest_chain_id, dest_tx = out_txs[0].get("chainId"), out_txs[0].get("hash") or ""
    if not dest_chain_id and curr_out:
        dest_chain_id = curr_out.get("currency", {}).get("chainId")
    dest_info = get_chain_info(dest_chain_id) if dest_chain_id else {}

    # Sent asset
    in_tok = curr_in.get("currency", {})
    in_meta = relay_deposit.get("tokenMetadata", {})
    in_decimals = in_tok.get("decimals") or in_meta.get("decimals", 6)
    in_symbol = in_tok.get("symbol") or in_meta.get("symbol", "TOKEN")
    in_name = in_tok.get("name") or in_meta.get("name", "Token")
    raw_in = origin.get("amount") or relay_deposit.get("amount") or curr_in.get("amount") or "0"
    sent_amount = curr_in.get("amountFormatted") or _fmt_amount(raw_in, in_decimals)

    # Received asset
    out_tok = curr_out.get("currency", {})
    out_symbol, out_name, out_decimals = out_tok.get("symbol"), out_tok.get("name"), out_tok.get("decimals")
    if not out_symbol:
        if str(dest_chain_id) in ("792703809", "solana"):
            out_symbol, out_name, out_decimals = "SOL", "Solana", 9
        else:
            out_symbol, out_name, out_decimals = in_symbol, in_name, in_decimals
    raw_out = curr_out.get("amount") or "0"
    rec_amount = curr_out.get("amountFormatted")
    if rec_amount:
        try:
            rec_amount = f"{float(rec_amount):,.4f}".rstrip("0").rstrip(".")
        except ValueError:
            pass
    elif raw_out != "0":
        rec_amount = _fmt_amount(raw_out, out_decimals or 18)
    else:
        rec_amount = sent_amount

    origin_side = _chain_side(origin_chain_id, origin_info, origin_tx)
    origin_side.update(
        sender_explorer_url=build_explorer_addr_url(origin_chain_id, from_wallet),
        depository_explorer_url=build_explorer_addr_url(origin_chain_id, depository),
    )
    dest_side = _chain_side(dest_chain_id, dest_info, dest_tx)
    dest_side["recipient_explorer_url"] = build_explorer_addr_url(dest_chain_id, to_wallet) if dest_chain_id and to_wallet else ""

    sent = _asset(in_symbol, in_name, sent_amount, curr_in.get("amountUsd"), raw_in)
    return {
        "protocol": "Relay.link",
        "protocol_badge": "Relay Protocol",
        "status": req.get("status", "unknown"),
        "created_at": req.get("createdAt", ""),
        "from_wallet": from_wallet,
        "depository_contract": depository,
        "depository_label": router_label(depository, "Relay Depository / Solver"),
        "to_wallet_tujuan": to_wallet,
        "origin_chain": origin_side,
        "destination_chain": dest_side,
        "sent_asset": sent,
        "recipient_asset": _asset(out_symbol, out_name, rec_amount, curr_out.get("amountUsd"), raw_out),
        "asset": dict(sent),
    }


def resolve_relay_tx(tx_hash: str) -> Optional[Dict[str, Any]]:
    """Resolve transaction using Relay.link API."""
    data = _get_json(f"https://api.relay.link/requests/v2?hash={tx_hash}") or {}
    reqs = data.get("requests") or []
    if not reqs:
        return None
    try:
        return _parse_relay_request(reqs[0], tx_hash)
    except Exception:
        return None


def resolve_lifi_jumper_tx(tx_hash: str) -> Optional[Dict[str, Any]]:
    """Resolve transaction using Li.Fi & Jumper Exchange API."""
    data = _get_json(f"https://li.quest/v1/status?txHash={tx_hash}")
    if not data:
        return None
    status = data.get("status", "")
    if status not in ("DONE", "PENDING", "COMPLETED", "FAILED") and not data.get("sending"):
        return None
    try:
        tool_name = str(data.get("tool") or "Li.Fi / Jumper").capitalize()
        sending = data.get("sending", {})
        receiving = data.get("receiving", {})
        from_wallet = data.get("fromAddress") or ""
        to_wallet = data.get("toAddress") or from_wallet

        src_token = sending.get("token", {})
        src_chain_id = src_token.get("chainId") or sending.get("chainId")
        src_tx = sending.get("txHash") or tx_hash
        src_raw = sending.get("amount") or sending.get("value") or "0"

        dst_token = receiving.get("token", {})
        dst_chain_id = dst_token.get("chainId") or receiving.get("chainId") or src_chain_id
        dst_tx = receiving.get("txHash") or ""
        dst_raw = receiving.get("amount") or receiving.get("value") or "0"

        router = "0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE"
        origin = _chain_side(src_chain_id, get_chain_info(src_chain_id), src_tx)
        origin.update(
            tx_explorer_url=sending.get("txLink") or origin["tx_explorer_url"],
            sender_explorer_url=build_explorer_addr_url(src_chain_id, from_wallet),
            depository_explorer_url=build_explorer_addr_url(src_chain_id, router),
        )
        dest = _chain_side(dst_chain_id, get_chain_info(dst_chain_id), dst_tx)
        dest.update(
            tx_explorer_url=receiving.get("txLink") or dest["tx_explorer_url"],
            recipient_explorer_url=build_explorer_addr_url(dst_chain_id, to_wallet),
        )
        src_sym, src_name = src_token.get("symbol", "TOKEN"), src_token.get("name", "Token")
        sent = _asset(src_sym, src_name, _fmt_amount(src_raw, src_token.get("decimals", 18)), sending.get("amountUSD"), src_raw)
        return {
            "protocol": f"Li.Fi / Jumper ({tool_name})",
            "protocol_badge": "Li.Fi / Jumper Exchange",
            "status": "SUCCESS" if status in ("DONE", "COMPLETED") else status,
            "created_at": "",
            "from_wallet": from_wallet,
            "depository_contract": router,
            "depository_label": f"Li.Fi Diamond Proxy ({tool_name})",
            "to_wallet_tujuan": to_wallet,
            "origin_chain": origin,
            "destination_chain": dest,
            "sent_asset": sent,
            "recipient_asset": _asset(
                dst_token.get("symbol", src_sym), dst_token.get("name", src_name),
                _fmt_amount(dst_raw, dst_token.get("decimals", 18)), receiving.get("amountUSD"), dst_raw),
            "asset": dict(sent),
        }
    except Exception:
        return None


def resolve_across_tx(tx_hash: str) -> Optional[Dict[str, Any]]:
    """Resolve transaction using Across Protocol API."""
    data = _get_json(f"https://app.across.to/api/deposit/status?depositTxHash={tx_hash}")
    if not data or not data.get("deposit"):
        return None
    try:
        deposit = data["deposit"]
        status = data.get("status", "filled")
        from_wallet = deposit.get("depositor") or ""
        to_wallet = deposit.get("recipient") or from_wallet
        src_id, dst_id = deposit.get("originChainId"), deposit.get("destinationChainId")
        fill_txs = data.get("fillTxs") or []
        dst_tx = fill_txs[0].get("hash", "") if fill_txs else ""
        spoke = deposit.get("spokePoolAddress") or "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5"

        origin = _chain_side(src_id, get_chain_info(src_id), tx_hash)
        origin.update(
            sender_explorer_url=build_explorer_addr_url(src_id, from_wallet),
            depository_explorer_url=build_explorer_addr_url(src_id, spoke),
        )
        dest = _chain_side(dst_id, get_chain_info(dst_id), dst_tx)
        dest["recipient_explorer_url"] = build_explorer_addr_url(dst_id, to_wallet)
        amt = str(deposit.get("amount", "0"))
        sent = _asset("ASSET", "Bridged Token", amt, None, amt)
        return {
            "protocol": "Across Protocol",
            "protocol_badge": "Across Bridge",
            "status": "SUCCESS" if status in ("filled", "completed") else status,
            "created_at": "",
            "from_wallet": from_wallet,
            "depository_contract": spoke,
            "depository_label": "Across SpokePool Bridge",
            "to_wallet_tujuan": to_wallet,
            "origin_chain": origin,
            "destination_chain": dest,
            "sent_asset": sent,
            "recipient_asset": dict(sent),
            "asset": dict(sent),
        }
    except Exception:
        return None


def resolve_layerzero_tx(tx_hash: str) -> Optional[Dict[str, Any]]:
    """Resolve transaction using LayerZero Scan API."""
    data = _get_json(f"https://scan.layerzero-api.com/v1/messages/tx/{tx_hash}") or {}
    messages = data.get("data") or []
    if not messages:
        return None
    try:
        msg = messages[0]
        pathway = msg.get("pathway", {})
        src_sender = pathway.get("sender", {})
        dst_receiver = pathway.get("receiver", {})
        from_wallet = src_sender.get("address") or ""
        to_wallet = dst_receiver.get("address") or from_wallet
        src_name = src_sender.get("chain", "Origin")
        dst_name = dst_receiver.get("chain", "Destination")
        src_info, dst_info = get_chain_info(src_name), get_chain_info(dst_name)
        status = msg.get("status", {}).get("name", "DELIVERED")
        dst_tx = msg.get("destination", {}).get("tx", {}).get("txHash", "")

        origin = _chain_side(src_info.get("id"), src_info, tx_hash, src_name)
        origin.update(sender_explorer_url=build_explorer_addr_url(src_info.get("id"), from_wallet), depository_explorer_url="")
        dest = _chain_side(dst_info.get("id"), dst_info, dst_tx, dst_name)
        dest["recipient_explorer_url"] = build_explorer_addr_url(dst_info.get("id"), to_wallet)
        sent = _asset("TOKEN", "LayerZero OFT / Asset", "Cross-Chain Message")
        return {
            "protocol": "LayerZero / Stargate",
            "protocol_badge": "LayerZero Protocol",
            "status": "SUCCESS" if status in ("DELIVERED", "CONFIRMED") else status,
            "created_at": "",
            "from_wallet": from_wallet,
            "depository_contract": from_wallet,
            "depository_label": f"LayerZero Endpoint ({src_sender.get('name', 'OApp')})",
            "to_wallet_tujuan": to_wallet,
            "origin_chain": origin,
            "destination_chain": dest,
            "sent_asset": sent,
            "recipient_asset": dict(sent),
            "asset": dict(sent),
        }
    except Exception:
        return None


ERC20_TRANSFER_TOPIC = "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ONCHAIN_CANDIDATES = ["arbitrum", "base", "ethereum", "bsc", "robinhood", "optimism", "polygon"]
_EXPLORER_HINTS = [
    ("robin.etherscan", "robinhood"), ("optimistic.etherscan", "optimism"), ("arbiscan", "arbitrum"),
    ("basescan", "base"), ("bscscan", "bsc"), ("polygonscan", "polygon"), ("etherscan.io", "ethereum"),
]


def _hex(b: Any) -> str:
    h = b.hex() if hasattr(b, "hex") else str(b)
    return h[2:] if h.startswith("0x") else h


def _onchain_lookup(chain: str, tx_hash: str) -> Optional[Dict[str, Any]]:
    cinfo = get_chain_info(chain)
    w3 = get_web3(cinfo.get("rpc"))
    if not w3:
        return None
    try:
        tx = w3.eth.get_transaction(tx_hash)
    except Exception:
        return None
    if not tx:
        return None
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
    except Exception:
        receipt = {}

    from_wallet = tx.get("from", "")
    interacted_to = tx.get("to") or ""
    status = "SUCCESS" if receipt.get("status") == 1 else ("FAILED" if receipt else "PENDING")
    to_wallet = interacted_to
    for log in receipt.get("logs", []):
        topics = log.get("topics", [])
        if len(topics) >= 3 and _hex(topics[0]) == ERC20_TRANSFER_TOPIC:
            recipient = "0x" + _hex(topics[2])[-40:]
            if recipient.lower() != from_wallet.lower():
                to_wallet = Web3.to_checksum_address(recipient)
                break

    cid = cinfo.get("id")
    symbol = cinfo.get("nativeCurrency", {}).get("symbol", "ETH")
    value = tx.get("value", 0)
    amount = f"{Web3.from_wei(value, 'ether'):.4f}" if value > 0 else "Transferred"
    side = _chain_side(cid, cinfo, tx_hash)
    origin = dict(side, sender_explorer_url=build_explorer_addr_url(cid, from_wallet),
                  depository_explorer_url=build_explorer_addr_url(cid, interacted_to))
    dest = dict(side, recipient_explorer_url=build_explorer_addr_url(cid, to_wallet))
    asset = _asset(symbol, "Native / ERC20 Asset", amount, None, str(value))
    return {
        "protocol": "On-Chain EVM / Direct Router",
        "protocol_badge": "On-Chain Route",
        "status": status,
        "created_at": "",
        "from_wallet": from_wallet,
        "depository_contract": interacted_to,
        "depository_label": router_label(interacted_to, "Smart Contract / Gateway"),
        "to_wallet_tujuan": to_wallet,
        "origin_chain": origin,
        "destination_chain": dest,
        "sent_asset": asset,
        "recipient_asset": dict(asset),
        "asset": dict(asset),
    }


# Shared worker pool for all fan-out network calls.
_POOL = ThreadPoolExecutor(max_workers=16, thread_name_prefix="omniroute")


def _first_in_priority(fns: List[Any], timeout: float = 15) -> Optional[Dict[str, Any]]:
    """Run callables in parallel; return the highest-priority non-empty result,
    without waiting for lower-priority ones once a higher one has answered."""
    futures = [_POOL.submit(fn) for fn in fns]
    deadline = time.time() + timeout
    for fut in futures:
        try:
            res = fut.result(timeout=max(0.1, deadline - time.time()))
        except Exception:
            res = None
        if res:
            return res
    return None


def resolve_universal_onchain_tx(tx_hash: str, original_url: str = "") -> Optional[Dict[str, Any]]:
    """Universal on-chain fallback: query all public EVM RPCs in parallel, first hit wins."""
    if not tx_hash.startswith("0x"):
        return None
    chains = list(ONCHAIN_CANDIDATES)
    for hint, ch in _EXPLORER_HINTS:
        if hint in original_url:
            # Explorer URL tells us the chain: ask it alone first.
            hit = _onchain_lookup(ch, tx_hash)
            if hit:
                return hit
            chains.remove(ch)
            break
    futures = [_POOL.submit(_onchain_lookup, ch, tx_hash) for ch in chains]
    try:
        for fut in as_completed(futures, timeout=12):
            res = fut.result()
            if res:
                return res
    except Exception:
        pass
    return None


# ==================== MAIN RESOLVER DISPATCHER ====================

def track_cross_chain(query: str) -> Dict[str, Any]:
    """Universal multi-protocol tracker supporting Relay, Li.Fi/Jumper, Across, LayerZero, and On-Chain."""
    cleaned = clean_input(query)
    q_type, val = cleaned["type"], cleaned["value"]
    original_url = cleaned.get("original_url", "")

    if not val:
        return {"success": False, "error": "Query tidak boleh kosong / Query cannot be empty."}

    started = time.time()

    if q_type == "tx_hash":
        # All protocol APIs fire at once; priority order decides the winner.
        res = _first_in_priority([
            lambda: resolve_relay_tx(val),
            lambda: resolve_lifi_jumper_tx(val),
            lambda: resolve_across_tx(val),
            lambda: resolve_layerzero_tx(val),
        ]) or resolve_universal_onchain_tx(val, original_url)
        if res:
            return {"success": True, "query_type": "transaction", "elapsed_ms": int((time.time() - started) * 1000), "data": res}
        return {
            "success": False,
            "error": f"Transaksi {val[:12]}... belum terindeks di Relay, Li.Fi/Jumper, Across, LayerZero, maupun RPC publik. / Not found on any supported protocol or public RPC."
        }

    if q_type == "address":
        data = _get_json(f"https://api.relay.link/requests/v2?user={val}&limit=10") or {}
        items = []
        for req in data.get("requests") or []:
            try:
                items.append(_parse_relay_request(req))
            except Exception:
                continue
        if items:
            return {"success": True, "query_type": "wallet_history", "address": val, "count": len(items),
                    "elapsed_ms": int((time.time() - started) * 1000), "data": items}

        return {
            "success": True,
            "query_type": "address_inspection",
            "address": val,
            "message": "Tidak ditemukan riwayat bridge untuk alamat ini — berikut hasil inspeksi alamat. / No bridge history found — showing address inspection instead.",
            "data": inspect_address_details(val)
        }

    return {"success": False, "error": "Format tidak dikenali. Masukkan Tx Hash, link explorer, atau alamat dompet. / Unrecognized input: paste a TX hash, explorer URL or wallet address."}


def inspect_address_details(address: str, chain_id_or_name: str = "ethereum") -> Dict[str, Any]:
    """Inspects target address: Checksum, EOA vs Contract, known routers, and native balance."""
    addr = address.strip()

    if SOLANA_ADDR_RE.match(addr):
        return {
            "is_valid": True,
            "format": "Solana (SVM)",
            "address": addr,
            "chain": "Solana",
            "type": "Solana Wallet / Program",
            "is_contract": False,
            "note": "Alamat Solana Base58 valid.",
            "explorer_url": f"https://solscan.io/account/{addr}"
        }

    if not Web3.is_address(addr):
        return {
            "is_valid": False,
            "address": addr,
            "error": "Alamat tidak valid (bukan format EVM atau Solana). / Invalid address (not EVM or Solana)."
        }

    checksum_addr = Web3.to_checksum_address(addr)
    chain_info = get_chain_info(chain_id_or_name)
    entity = classify_entity(checksum_addr)
    result = {
        "is_valid": True,
        "format": "EVM",
        "checksum_address": checksum_addr,
        "chain": chain_info.get("displayName", "Ethereum"),
        "chain_id": chain_info.get("id"),
        "known_protocol": entity["name"],
        "entity_category": entity["category"],
        "explorer_url": build_explorer_addr_url(chain_info.get("id"), checksum_addr)
    }

    w3 = get_web3(chain_info.get("rpc"))
    if not w3:
        result["rpc_status"] = "RPC tidak tersedia untuk chain ini / No RPC for this chain"
        return result

    # bytecode + balance in parallel
    f_code = _POOL.submit(w3.eth.get_code, checksum_addr)
    f_bal = _POOL.submit(w3.eth.get_balance, checksum_addr)
    try:
        is_contract = len(f_code.result(timeout=8)) > 0
        result["is_contract"] = is_contract
        result["target_type"] = "SMART CONTRACT (Router / Pool / Gateway)" if is_contract else "EOA (Dompet Biasa / User Wallet)"
    except Exception as e:
        result["rpc_error"] = str(e)[:200]
    try:
        symbol = chain_info.get("nativeCurrency", {}).get("symbol", "ETH")
        result["native_balance"] = f"{Web3.from_wei(f_bal.result(timeout=8), 'ether'):.4f} {symbol}"
    except Exception:
        result["native_balance"] = "N/A"
    return result


# ==================== WALLET GENEALOGY, FLOW & SYBIL ANALYZER ====================

SPAM_PATTERNS = re.compile(
    r'(https?://|www\.|\.io|\.so|\.org|\.com|\.xyz|\.vip|\.top|\.cc|\.net|\.app|\.me|\.link|\.site|\.live|'
    r'claim|visit|t\.ly|airdrop|bonus|t\.me|shib|pump|free|gift|reward|voucher|drop|freetoken)',
    re.IGNORECASE
)

# Verified Token Decimals Map (Protection against token decimal spoofing)
VERIFIED_TOKEN_DECIMALS = {
    # 6 decimals
    "USDC": 6, "USDT": 6, "USDBC": 6, "USDD": 6, "FDUSD": 6, "PYUSD": 6,
    # 8 decimals
    "WBTC": 8, "TBTC": 8, "CBTC": 8,
    # 9 decimals
    "SOL": 9,
    # 18 decimals
    "ETH": 18, "WETH": 18, "DAI": 18, "POL": 18, "MATIC": 18, "BNB": 18,
    "WBNB": 18, "AVAX": 18, "FTM": 18, "ARB": 18, "OP": 18, "LINK": 18,
    "UNI": 18, "AERO": 18, "BRETT": 18, "DEGEN": 18, "TOSHI": 18
}

VERIFIED_TOKENS = set(VERIFIED_TOKEN_DECIMALS.keys())

# ==================== IN-MEMORY TTL CACHE (BATCH & RE-RUN ACCELERATOR) ====================
_GENEALOGY_CACHE: Dict[str, Dict[str, Any]] = {}
_GENEALOGY_LOCK = threading.Lock()
CACHE_TTL_SECONDS = 300  # 5 minutes cache


def get_cached_genealogy(cache_key: str) -> Optional[Dict[str, Any]]:
    with _GENEALOGY_LOCK:
        entry = _GENEALOGY_CACHE.get(cache_key)
        if not entry:
            return None
        if time.time() - entry["timestamp"] >= CACHE_TTL_SECONDS:
            del _GENEALOGY_CACHE[cache_key]
            return None
        res = dict(entry["data"])
    res["fromCache"] = True
    return res


def set_cached_genealogy(cache_key: str, data: Dict[str, Any]):
    with _GENEALOGY_LOCK:
        if len(_GENEALOGY_CACHE) > 500:
            oldest_key = min(_GENEALOGY_CACHE, key=lambda k: _GENEALOGY_CACHE[k]["timestamp"])
            del _GENEALOGY_CACHE[oldest_key]
        _GENEALOGY_CACHE[cache_key] = {"timestamp": time.time(), "data": data}


def is_spam_symbol(sym: str) -> bool:
    sym = str(sym or "").strip()
    return bool(SPAM_PATTERNS.search(sym)) or any(c in sym for c in "./\\") or len(sym) > 10


def is_valid_token_tx(tx: Dict[str, Any]) -> bool:
    """Filters out scam airdrop tokens and phishing URLs."""
    name = str(tx.get("tokenName") or "").strip()
    sym = str(tx.get("tokenSymbol") or tx.get("symbol") or "").strip()
    val_raw = str(tx.get("value") or "0").strip()
    if not sym or not val_raw or val_raw == "0":
        return False
    return not (SPAM_PATTERNS.search(name) or is_spam_symbol(sym))


def parse_token_amount(val_str: Any, raw_dec: Any, symbol: str = "") -> float:
    """
    Normalizes token decimal accurately with anti-spoof protection.
    Prevents artificially inflated scam balances by enforcing verified decimal registries
    and bounds checking dynamic decimals (0 <= dec <= 18).
    """
    try:
        val = int(str(val_str).strip())
        if val <= 0:
            return 0.0
        sym_upper = str(symbol or "").strip().upper()
        if sym_upper in VERIFIED_TOKEN_DECIMALS:
            dec = VERIFIED_TOKEN_DECIMALS[sym_upper]
        else:
            try:
                dec = int(raw_dec)
                if not 0 <= dec <= 18:
                    dec = 18  # Safe default if spoofed (e.g. 255 or negative)
            except (ValueError, TypeError):
                dec = 18
        real_amt = val / (10 ** dec)
        # Reject astronomically inflated scam amounts (> 1 quadrillion tokens)
        return 0.0 if real_amt > 1e15 else real_amt
    except Exception:
        return 0.0


def _blockscout_list(api: str, action: str, address: str, offset: int = 500, sort: str = "asc") -> Optional[List[Dict[str, Any]]]:
    """Account tx list from Blockscout v1. Returns [] for a genuinely empty history and
    None when the source failed (timeout, rate limit, Cloudflare challenge)."""
    data = _get_json(f"{api}?module=account&action={action}&address={address}&page=1&offset={offset}&sort={sort}", timeout=8)
    if isinstance(data, dict) and isinstance(data.get("result"), list):
        return data["result"]
    return None


_RISK_BY_CATEGORY = {
    "public_faucet": "Public Faucet / Gas Dispenser",
    "bridge_router": "Bridge Settlement Funder",
    "mixer": "Mixer Interaction (Tornado Cash)",
}


def _aggregate_flows(native_txs, token_txs, addr_lower: str, direction: str, native_symbol: str):
    """Sum native + clean token flows per counterparty. direction: 'in' or 'out'."""
    me, other = ("to", "from") if direction == "in" else ("from", "to")
    flows: Dict[str, Dict[str, Any]] = {}
    total = 0.0
    for tx in native_txs:
        if (tx.get(me) or "").lower() != addr_lower:
            continue
        cp = tx.get(other) or ""
        amt = int(tx.get("value", 0) or 0) / 1e18
        if cp and amt > 0.0001:
            rec = flows.setdefault(cp, {"amount": 0.0, "count": 0, "symbol": native_symbol})
            rec["amount"] += amt
            rec["count"] += 1
            total += amt
    for ttx in token_txs:
        if (ttx.get(me) or "").lower() != addr_lower:
            continue
        cp = ttx.get(other) or ""
        sym = ttx.get("tokenSymbol", "TOKEN")
        amt = parse_token_amount(ttx.get("value", "0"), ttx.get("tokenDecimal"), sym)
        if cp and amt > 0.001:
            rec = flows.setdefault(cp, {"amount": 0.0, "count": 0, "symbol": sym})
            rec["amount"] += amt
            rec["count"] += 1
            total += amt
    return sorted(flows.items(), key=lambda x: x[1]["amount"], reverse=True), total


def analyze_wallet_genealogy(target_address: str, chain: str = "base") -> Dict[str, Any]:
    """
    Analyzes all-time Genesis funder (initial gas provider), capital providers,
    clean outflow targets (CEX / DEX), and prepares linked wallets for GMGN export.
    Works for both EVM and Solana addresses. Includes in-memory TTL caching.
    """
    addr = target_address.strip()
    if SOLANA_ADDR_RE.match(addr):
        return analyze_solana_genealogy(addr)

    if not Web3.is_address(addr):
        return {"success": False, "error": "Alamat bukan format EVM atau Solana yang valid. / Not a valid EVM or Solana address."}

    checksum_addr = Web3.to_checksum_address(addr)
    addr_lower = checksum_addr.lower()
    chain_key = chain.lower().strip()
    cache_key = f"{chain_key}:{addr_lower}"

    cached = get_cached_genealogy(cache_key)
    if cached:
        return cached

    cinfo = get_chain_info(chain)
    native_symbol = cinfo.get("nativeCurrency", {}).get("symbol", "ETH")
    blockscout_api = cinfo.get("blockscoutApi")
    if not blockscout_api:
        return {"success": False, "error": f"Chain {cinfo.get('displayName', chain)} belum didukung untuk analisis silsilah (butuh Blockscout). / This chain is not supported for genealogy yet."}

    # Native + token history fetched in parallel
    f_native = _POOL.submit(_blockscout_list, blockscout_api, "txlist", checksum_addr)
    f_token = _POOL.submit(_blockscout_list, blockscout_api, "tokentx", checksum_addr)
    all_txs, raw_token_txs = f_native.result(), f_token.result()
    if all_txs is None and raw_token_txs is None:
        # Don't report (or cache) "no history" when the data source simply didn't answer.
        return {"success": False, "error": SOURCE_DOWN_ERROR}
    partial = all_txs is None or raw_token_txs is None
    all_txs = all_txs or []
    clean_token_txs = [t for t in (raw_token_txs or []) if is_valid_token_tx(t)]

    now_ts = int(time.time())
    genesis_funder = None
    risk_flags: List[str] = []

    # Genesis Funder: first native deposit, else first meaningful clean token deposit
    for tx in all_txs:
        val = int(tx.get("value", 0) or 0)
        if (tx.get("to") or "").lower() == addr_lower and val > 0:
            funder = to_checksum(tx.get("from", ""))
            cls_info = classify_entity(funder)
            tx_ts = int(tx.get("timeStamp", now_ts))
            genesis_funder = {
                "address": funder,
                "label": cls_info["name"],
                "is_noisy": cls_info["is_noisy"],
                "category": cls_info["category"],
                "amount": f"{val / 1e18:.4f}",
                "tokenSymbol": native_symbol,
                "txHash": tx.get("hash", ""),
                "timestamp": tx_ts,
                "days_ago": max(0, (now_ts - tx_ts) // 86400)
            }
            if cls_info["category"] == "cex_hot_wallet":
                risk_flags.append(f"Public CEX Funder: {cls_info['name']}")
            elif cls_info["category"] in _RISK_BY_CATEGORY:
                risk_flags.append(_RISK_BY_CATEGORY[cls_info["category"]])
            if genesis_funder["days_ago"] < 2:
                risk_flags.append("Fresh Wallet (<48h)")
            break

    if not genesis_funder:
        for ttx in clean_token_txs:
            if (ttx.get("to") or "").lower() != addr_lower:
                continue
            amt = parse_token_amount(ttx.get("value", "0"), ttx.get("tokenDecimal"), ttx.get("tokenSymbol", ""))
            if amt <= 0.001:
                continue
            funder = to_checksum(ttx.get("from", ""))
            cls_info = classify_entity(funder)
            tx_ts = int(ttx.get("timeStamp", now_ts))
            genesis_funder = {
                "address": funder,
                "label": cls_info["name"] or "Token Capital Funder",
                "is_noisy": cls_info["is_noisy"],
                "category": cls_info["category"],
                "amount": f"{amt:,.2f}",
                "tokenSymbol": ttx.get("tokenSymbol", "TOKEN"),
                "txHash": ttx.get("hash", ""),
                "timestamp": tx_ts,
                "days_ago": max(0, (now_ts - tx_ts) // 86400)
            }
            break

    if genesis_funder:
        genesis_funder["txUrl"] = build_explorer_tx_url(cinfo.get("id"), genesis_funder["txHash"])

    # Top inflow providers
    sorted_inflows, _ = _aggregate_flows(all_txs, clean_token_txs, addr_lower, "in", native_symbol)
    top_inflows = []
    for s_addr, s_data in sorted_inflows[:5]:
        s_chk = to_checksum(s_addr)
        s_cls = classify_entity(s_chk)
        top_inflows.append({
            "sender": s_chk,
            "label": s_cls["name"],
            "is_noisy": s_cls["is_noisy"],
            "category": s_cls["category"],
            "totalAmount": round(s_data["amount"], 4),
            "tokenSymbol": s_data["symbol"],
            "txCount": s_data["count"]
        })

    # Top outflow targets (exit / cash out)
    sorted_outflows, total_outflow_vol = _aggregate_flows(all_txs, clean_token_txs, addr_lower, "out", native_symbol)
    top_outflows = []
    cex_cashout_detected = False
    for r_addr, r_data in sorted_outflows[:6]:
        r_chk = to_checksum(r_addr)
        r_cls = classify_entity(r_chk)
        label = r_cls["name"]
        is_contract = r_cls["category"] in ("bridge_router", "dex_router", "paymaster") or bool(
            label and any(w in label for w in ("Router", "Pool", "Proxy", "Contract")))
        if r_cls["category"] == "cex_hot_wallet":
            cex_cashout_detected = True
        top_outflows.append({
            "recipient": r_chk,
            "label": label,
            "is_noisy": r_cls["is_noisy"],
            "category": r_cls["category"],
            "totalAmount": round(r_data["amount"], 4),
            "percentage": round(r_data["amount"] / total_outflow_vol * 100, 1) if total_outflow_vol > 0 else 0,
            "tokenSymbol": r_data["symbol"],
            "txCount": r_data["count"],
            "isContract": is_contract
        })

    if cex_cashout_detected:
        risk_flags.append("CEX Off-Ramp / Cash Out Target")
    if any(o["category"] == "mixer" for o in top_outflows):
        risk_flags.append("Mixer Cash Out (Tornado Cash)")

    if cex_cashout_detected:
        exit_pattern = "CEX Off-Ramp / Hot Wallet"
    elif any(o["isContract"] for o in top_outflows):
        exit_pattern = "DEX Trading & Liquidity"
    else:
        exit_pattern = "Private Transfers / In-Transit"

    # Linked wallets for GMGN watchlist & clustering
    linked_wallets = [{"address": checksum_addr, "role": "Target_Main", "confidence": 100, "chain": chain_key, "label": "Analyzed Target Wallet"}]
    seen = {addr_lower}

    def _link(address: str, role: str, conf: int, label: str):
        if address and address.lower() not in seen:
            seen.add(address.lower())
            linked_wallets.append({"address": address, "role": role, "confidence": conf, "chain": chain_key, "label": label})

    if genesis_funder and genesis_funder.get("address"):
        cat = genesis_funder.get("category")
        role = "Public_CEX_Funder" if cat == "cex_hot_wallet" else ("Public_Faucet" if cat == "public_faucet" else "Genesis_Funder")
        _link(genesis_funder["address"], role, 20 if genesis_funder.get("is_noisy") else 95,
              genesis_funder.get("label") or "Initial Gas Provider")
    for item in top_inflows:
        _link(item["sender"], "CEX_Inflow" if item["category"] == "cex_hot_wallet" else "Capital_Provider",
              25 if item["is_noisy"] else 85,
              item["label"] or f"Inflow (+{item['totalAmount']} {item['tokenSymbol']})")
    for item in top_outflows:
        if item["category"] == "cex_hot_wallet":
            role, conf = "CEX_Deposit", 20
        elif item["isContract"]:
            role, conf = "Router_Contract", 40
        else:
            role, conf = "Consolidation_EOA", 90
        _link(item["recipient"], role, conf, item["label"] or f"Exit Destination ({item['percentage']}%)")

    result = {
        "success": True,
        "targetAddress": checksum_addr,
        "chain": cinfo.get("displayName", chain.capitalize()),
        "chainKey": chain_key,
        "genesisFunder": genesis_funder,
        "topInflows": top_inflows,
        "topOutflows": top_outflows,
        "linkedWallets": linked_wallets,
        "totalTransactions": len(all_txs) + len(clean_token_txs),
        "exitPattern": exit_pattern,
        "riskFlags": risk_flags + (["Data parsial: sebagian riwayat gagal dimuat / Partial data: part of the history failed to load"] if partial else [])
    }
    if not partial:
        set_cached_genealogy(cache_key, result)
    return result


def _split_shared(groups: Dict[str, List[str]], key: str, list_key: str, private_label: str, infra_default: str):
    """Split addresses shared by >1 wallet into private-EOA overlaps vs public infrastructure."""
    private, infra = [], []
    for addr, wallets in groups.items():
        if len(wallets) < 2:
            continue
        cls_info = classify_entity(addr)
        if cls_info["is_noisy"]:
            infra.append({key: addr, "label": cls_info["name"] or infra_default, "category": cls_info["category"], list_key: wallets})
        else:
            private.append({key: addr, "label": private_label, "category": "private_eoa", list_key: wallets})
    return private, infra


def analyze_batch_sybil(addresses: List[str], chain: str = "base") -> Dict[str, Any]:
    """
    Analyzes a batch of 2-20 wallets to discover genuine Sybil clusters
    while eliminating false positives from noisy infrastructure (CEX hot wallets, faucets, bridge solvers).
    Wallets are analyzed in parallel (bounded) and reuse the genealogy cache.
    """
    seen_inputs = set()
    clean_addrs = []
    for a in addresses:
        a = str(a).strip()
        if a and a.lower() not in seen_inputs:
            seen_inputs.add(a.lower())
            clean_addrs.append(a)
    clean_addrs = clean_addrs[:20]
    if len(clean_addrs) < 2:
        return {"success": False, "error": "Harap masukkan minimal 2 alamat wallet berbeda / Please provide at least 2 distinct wallet addresses."}

    chain_key = chain.lower().strip()

    # 4 concurrent wallets (= up to 8 Blockscout calls) keeps us under public rate limits.
    with ThreadPoolExecutor(max_workers=4) as ex:
        genealogies = list(ex.map(lambda a: analyze_wallet_genealogy(a, chain), clean_addrs))

    results = []
    funders_map: Dict[str, List[str]] = {}
    exits_map: Dict[str, List[str]] = {}
    all_linked: List[Dict[str, Any]] = []
    linked_seen = set()
    failed = []

    for addr, genealogy in zip(clean_addrs, genealogies):
        if not genealogy.get("success"):
            failed.append({"address": addr, "error": genealogy.get("error", "")})
            continue
        results.append(genealogy)
        gf = genealogy.get("genesisFunder")
        if gf and gf.get("address"):
            funders_map.setdefault(gf["address"], []).append(addr)
        for out in genealogy.get("topOutflows", []):
            if out.get("recipient"):
                exits_map.setdefault(out["recipient"], []).append(addr)
        for lw in genealogy.get("linkedWallets", []):
            if lw["address"].lower() not in linked_seen:
                linked_seen.add(lw["address"].lower())
                all_linked.append(lw)

    private_shared_funders, infra_shared_funders = _split_shared(
        funders_map, "funder", "fundedWallets", "Private EOA Funder", "Public Infrastructure Funder")
    private_shared_exits, infra_shared_exits = _split_shared(
        exits_map, "exitTarget", "sendingWallets", "Private Consolidation EOA", "Public CEX / Router Hub")

    # Sybil is ONLY true on private shared overlap (not common Binance/OKX hot wallets)
    sybil_detected = bool(private_shared_funders or private_shared_exits)

    if private_shared_funders and private_shared_exits:
        confidence_score, risk_level = 96, "CRITICAL"
        risk_desc = {
            "id": "Tingkat Keyakinan Sangat Tinggi: Dompet berbagi Funder EOA pribadi yang sama DAN Hub Konsolidasi EOA yang sama.",
            "en": "High Confidence Linkage: Wallets share the same private Genesis Funder EOA AND the same Consolidation Hub EOA."
        }
    elif private_shared_funders:
        max_overlap = max(len(x["fundedWallets"]) for x in private_shared_funders)
        confidence_score, risk_level = (92 if max_overlap >= 3 else 85), "HIGH"
        risk_desc = {
            "id": f"Sinyal Relasi Kuat: {len(private_shared_funders)} alamat EOA pribadi mendanai beberapa dompet.",
            "en": f"Strong Relationship Signal: {len(private_shared_funders)} private EOA address(es) funded multiple wallets."
        }
    elif private_shared_exits:
        max_overlap = max(len(x["sendingWallets"]) for x in private_shared_exits)
        confidence_score, risk_level = (88 if max_overlap >= 3 else 80), "HIGH"
        risk_desc = {
            "id": f"Sinyal Relasi Kuat: {len(private_shared_exits)} hub konsolidasi EOA pribadi menerima dana dari beberapa dompet.",
            "en": f"Strong Relationship Signal: {len(private_shared_exits)} private consolidation EOA hub(s) received funds from multiple wallets."
        }
    elif infra_shared_funders or infra_shared_exits:
        confidence_score, risk_level = 20, "LOW_COINCIDENTAL"
        risk_desc = {
            "id": "Infrastruktur Publik Bersama: Dompet hanya beririsan pada Hot Wallet CEX besar (Binance, OKX, dll) atau Faucet publik (Bukan klaster pribadi).",
            "en": "Shared Public Infrastructure: Wallets only overlap on major CEX Hot Wallets (Binance, OKX, etc.) or public faucets (Independent users, not a private cluster)."
        }
    else:
        confidence_score, risk_level = 0, "NONE"
        risk_desc = {
            "id": "Independen Bersih: Tidak ditemukan irisan funder maupun exit target antar-dompet.",
            "en": "Clean Independence: No shared funders or exit targets found across wallets."
        }

    sybil_flags = []
    if private_shared_funders:
        sybil_flags.append(f"Private Genesis Funder Overlap ({len(private_shared_funders)} private EOA)")
    if private_shared_exits:
        sybil_flags.append(f"Private Consolidation Hub Overlap ({len(private_shared_exits)} private EOA)")
    if infra_shared_funders or infra_shared_exits:
        sybil_flags.append(f"Shared CEX / Public Infrastructure ({len(infra_shared_funders) + len(infra_shared_exits)} public entities)")

    return {
        "success": True,
        "chain": chain,
        "chainKey": chain_key,
        "totalChecked": len(results),
        "failedWallets": failed,
        "sybilDetected": sybil_detected,
        "confidenceScore": confidence_score,
        "riskLevel": risk_level,
        "riskDescription": risk_desc,
        "sharedFunders": private_shared_funders,
        "sharedExits": private_shared_exits,
        "sharedInfrastructure": {"funders": infra_shared_funders, "exits": infra_shared_exits},
        "sybilFlags": sybil_flags,
        "linkedWallets": all_linked,
        "walletGenealogies": results
    }


def _solana_account_keys(tx: Dict[str, Any]) -> List[str]:
    keys = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
    return [k.get("pubkey") if isinstance(k, dict) else k for k in keys]


def analyze_solana_genealogy(solana_address: str) -> Dict[str, Any]:
    """
    Solana funder lookup via public RPC: finds the oldest visible signature (up to 1000 back)
    and reports who funded the wallet in that transaction. Outflow analysis is not available
    for Solana yet, which is flagged in the result.
    """
    cache_key = f"solana:{solana_address}"
    cached = get_cached_genealogy(cache_key)
    if cached:
        return cached

    sigs = _rpc(SOLANA_RPC, "getSignaturesForAddress", [solana_address, {"limit": 1000}], timeout=8) or []
    genesis_funder = None
    top_inflows: List[Dict[str, Any]] = []
    risk_flags: List[str] = []

    if sigs:
        earliest = sigs[-1]
        sig = earliest.get("signature", "")
        ts = earliest.get("blockTime") or int(time.time())
        tx = _rpc(SOLANA_RPC, "getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}], timeout=8) or {}
        funder, amount, symbol = "", 0.0, "SOL"

        # Prefer an explicit SOL/SPL transfer into the target; fall back to the fee payer.
        meta = tx.get("meta") or {}
        instructions = list(tx.get("transaction", {}).get("message", {}).get("instructions", []))
        for inner in meta.get("innerInstructions") or []:
            instructions.extend(inner.get("instructions", []))
        for ix in instructions:
            parsed = ix.get("parsed") if isinstance(ix, dict) else None
            if not isinstance(parsed, dict):
                continue
            info = parsed.get("info", {})
            if parsed.get("type") in ("transfer", "createAccount") and info.get("destination", info.get("newAccount")) == solana_address and "lamports" in info:
                funder = info.get("source", "")
                amount = int(info.get("lamports", 0)) / 1e9
                break
        if not funder:
            keys = _solana_account_keys(tx)
            if keys and keys[0] != solana_address:
                funder = keys[0]

        if funder:
            cls_info = classify_entity(funder)
            days_ago = max(0, (int(time.time()) - ts) // 86400)
            genesis_funder = {
                "address": funder,
                "label": cls_info["name"] or "Solana Funder / Fee Payer",
                "is_noisy": cls_info["is_noisy"],
                "category": cls_info["category"],
                "amount": f"{amount:.4f}" if amount else "-",
                "tokenSymbol": symbol,
                "txHash": sig,
                "txUrl": f"https://solscan.io/tx/{sig}",
                "timestamp": ts,
                "days_ago": days_ago
            }
            if days_ago < 2:
                risk_flags.append("Fresh Wallet (<48h)")
    if len(sigs) >= 1000:
        risk_flags.append("Riwayat >1000 tx: funder = tx tertua yang terlihat / History >1000 txs: oldest visible tx shown")
    risk_flags.append("Solana: analisis outflow belum tersedia / outflow analysis not available")

    linked_wallets = [{"address": solana_address, "role": "Target_Main", "confidence": 100, "chain": "solana", "label": "Solana Target Wallet"}]
    if genesis_funder:
        linked_wallets.append({
            "address": genesis_funder["address"],
            "role": "Public_Funder" if genesis_funder["is_noisy"] else "Genesis_Funder",
            "confidence": 20 if genesis_funder["is_noisy"] else 90,
            "chain": "solana",
            "label": genesis_funder["label"]
        })

    result = {
        "success": True,
        "targetAddress": solana_address,
        "chain": "Solana",
        "chainKey": "solana",
        "genesisFunder": genesis_funder,
        "topInflows": top_inflows,
        "topOutflows": [],
        "linkedWallets": linked_wallets,
        "totalTransactions": len(sigs),
        "exitPattern": "Solana On-Chain Transfers",
        "riskFlags": risk_flags
    }
    set_cached_genealogy(cache_key, result)
    return result


# ==================== TAB 4: EXCHANGE DEPOSIT INFLOW TRACER ====================

_TOKEN_PRICE_CACHE: Dict[str, Dict[str, Any]] = {}
_SOLANA_ATA_CACHE: Dict[str, str] = {}
PRICE_TTL_SECONDS = 300

STABLECOIN_SYMBOLS = {"USDC", "USDT", "USDG", "PYUSD", "DAI", "USDBC", "FDUSD", "USDD", "USDB"}

# Offline fallback prices, used only when CoinGecko is unreachable.
_FALLBACK_MAJOR_PRICES = {
    "ETH": 2600.0, "WETH": 2600.0, "SOL": 110.0, "WSOL": 110.0,
    "BTC": 80000.0, "WBTC": 80000.0, "CBTC": 80000.0, "BNB": 750.0, "WBNB": 750.0,
    "POL": 0.40, "MATIC": 0.40, "ARB": 0.55, "OP": 1.40, "AVAX": 24.0,
}
_COINGECKO_IDS = {
    "ETH": "ethereum", "WETH": "ethereum", "SOL": "solana", "WSOL": "solana",
    "BTC": "bitcoin", "WBTC": "bitcoin", "CBTC": "bitcoin", "BNB": "binancecoin", "WBNB": "binancecoin",
    "POL": "polygon-ecosystem-token", "MATIC": "polygon-ecosystem-token",
    "ARB": "arbitrum", "OP": "optimism", "AVAX": "avalanche-2",
}
_majors_state: Dict[str, Any] = {"ts": 0.0, "prices": {}}
_majors_lock = threading.Lock()


def _major_prices() -> Dict[str, float]:
    """All major spot prices from ONE CoinGecko call, cached for PRICE_TTL_SECONDS."""
    if _majors_state["prices"] and time.time() - _majors_state["ts"] < PRICE_TTL_SECONDS:
        return _majors_state["prices"]
    with _majors_lock:
        if _majors_state["prices"] and time.time() - _majors_state["ts"] < PRICE_TTL_SECONDS:
            return _majors_state["prices"]
        ids = ",".join(sorted(set(_COINGECKO_IDS.values())))
        live = _get_json(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd", timeout=4) or {}
        prices = dict(_FALLBACK_MAJOR_PRICES)
        for sym, cg_id in _COINGECKO_IDS.items():
            p = (live.get(cg_id) or {}).get("usd")
            if p:
                prices[sym] = float(p)
        # Retry sooner when the live call failed
        _majors_state.update(ts=time.time() if live else time.time() - PRICE_TTL_SECONDS + 30, prices=prices)
        return prices


def get_token_usd_price(symbol: str, mint_or_addr: Optional[str] = None, chain: str = "ethereum") -> float:
    """
    Resolves token price in USD:
    1. $1.00 for verified USD stablecoins.
    2. Major spot prices (single batched CoinGecko call, cached).
    3. DexScreener highest-liquidity pair for other tokens by contract/mint (cached).
    """
    sym_clean = str(symbol or "").strip().upper()
    if sym_clean in STABLECOIN_SYMBOLS:
        return 1.0
    majors = _major_prices()
    if sym_clean in majors:
        return majors[sym_clean]
    if not mint_or_addr or len(mint_or_addr) < 30:
        return 0.0

    cache_key = mint_or_addr.lower()
    entry = _TOKEN_PRICE_CACHE.get(cache_key)
    if entry and time.time() - entry["timestamp"] < PRICE_TTL_SECONDS:
        return entry["price"]

    price = 0.0
    data = _get_json(f"https://api.dexscreener.com/latest/dex/tokens/{mint_or_addr}", timeout=4) or {}
    pairs = data.get("pairs") or []
    if pairs:
        def _liq(p):
            try:
                return float((p.get("liquidity") or {}).get("usd") or 0)
            except (TypeError, ValueError):
                return 0.0
        best = max(pairs, key=_liq)
        try:
            price = float(best.get("priceUsd") or 0)
        except (TypeError, ValueError):
            price = 0.0
    _TOKEN_PRICE_CACHE[cache_key] = {"timestamp": time.time(), "price": price}
    return price


def resolve_solana_token_owner(ata_pubkey: str, tx_meta: Optional[Dict[str, Any]] = None) -> str:
    """
    Resolves Solana Associated Token Account (ATA) to its true wallet owner.
    1. Checks transaction pre/postTokenBalances for pre-indexed owner.
    2. Fallback to Solana RPC getAccountInfo with in-memory caching.
    """
    if not ata_pubkey:
        return ""
    if ata_pubkey in _SOLANA_ATA_CACHE:
        return _SOLANA_ATA_CACHE[ata_pubkey]

    if tx_meta:
        for bal_list in (tx_meta.get("preTokenBalances") or [], tx_meta.get("postTokenBalances") or []):
            for item in bal_list:
                owner = item.get("owner")
                if owner and owner != ata_pubkey:
                    _SOLANA_ATA_CACHE[ata_pubkey] = owner
                    return owner

    val = (_rpc(SOLANA_RPC, "getAccountInfo", [ata_pubkey, {"encoding": "jsonParsed"}], timeout=4) or {}).get("value")
    owner = ""
    if isinstance(val, dict):
        owner = val.get("data", {}).get("parsed", {}).get("info", {}).get("owner", "")
    _SOLANA_ATA_CACHE[ata_pubkey] = owner or ata_pubkey
    return owner or ata_pubkey


KNOWN_SOL_MINTS = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {"symbol": "USDC", "decimals": 6},
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {"symbol": "USDT", "decimals": 6},
    "2b1kV6ebUAKGJJrwQVBSAvxsxjqPPd5GE3GvcBXSox4V": {"symbol": "PYUSD", "decimals": 6},
    "So11111111111111111111111111111111111111112": {"symbol": "SOL", "decimals": 9},
}
SOLANA_TX_SCAN_LIMIT = 25


def _solana_get_transactions(sigs: List[str]) -> List[Optional[Dict[str, Any]]]:
    """Fetch parsed transactions within the public RPC's quota.
    mainnet-beta allows ~10 getTransaction calls per ~10s window and rejects the rest (batches
    included), so we go sequentially and, when throttled, sleep exactly until the window resets
    instead of blind backoff. 25 txs ≈ 20s with no gaps in the data."""
    params = {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
    window = 10.5
    window_start = time.time()
    out: List[Optional[Dict[str, Any]]] = []
    for sig in sigs:
        res = None
        for _ in range(3):
            res = _rpc(SOLANA_RPC, "getTransaction", [sig, params], 6)
            if res:
                break
            time.sleep(max(1.0, window - (time.time() - window_start)))
            window_start = time.time()
        out.append(res)
    return out


def fetch_solana_deposit_inflows(deposit_address: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetches native SOL and SPL token transfers into the deposit address.
    Resolves the actual sender wallet (not the ATA).
    """
    sigs = _rpc(SOLANA_RPC, "getSignaturesForAddress", [deposit_address, {"limit": min(limit, 100)}], timeout=7) or []
    sig_entries = [s for s in sigs if s.get("signature") and not s.get("err")][:SOLANA_TX_SCAN_LIMIT]
    if not sig_entries:
        return []

    txs = _solana_get_transactions([s["signature"] for s in sig_entries])
    inflows: List[Dict[str, Any]] = []
    for s_entry, tx_data in zip(sig_entries, txs):
        if not tx_data:
            continue
        sig = s_entry["signature"]
        block_time = s_entry.get("blockTime") or int(time.time())
        tx_meta = tx_data.get("meta") or {}
        instructions = list(tx_data.get("transaction", {}).get("message", {}).get("instructions", []))
        for inner in tx_meta.get("innerInstructions") or []:
            instructions.extend(inner.get("instructions", []))

        for ix in instructions:
            parsed = ix.get("parsed") if isinstance(ix, dict) else None
            if not isinstance(parsed, dict):
                continue
            ix_type = parsed.get("type", "")
            info = parsed.get("info", {})

            # Native SOL transfer
            if ix_type == "transfer" and "lamports" in info:
                if info.get("destination") != deposit_address:
                    continue
                sender = info.get("source")
                amt = int(info.get("lamports", 0)) / 1e9
                if sender and amt > 0.0001:
                    inflows.append({"sender": sender, "amount": amt, "token_symbol": "SOL",
                                    "mint": "So11111111111111111111111111111111111111112", "decimals": 9,
                                    "timestamp": block_time, "tx_hash": sig, "chain": "solana"})

            # SPL token transfer
            elif ix_type in ("transfer", "transferChecked"):
                mint = info.get("mint") or "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
                token_amount = info.get("tokenAmount") or {}
                raw_amt = info.get("amount") or token_amount.get("amount", "0")
                decimals = token_amount.get("decimals")
                if decimals is None:
                    decimals = KNOWN_SOL_MINTS.get(mint, {}).get("decimals", 6)
                try:
                    amt = int(raw_amt) / (10 ** int(decimals))
                except (TypeError, ValueError):
                    amt = 0.0
                sender = info.get("authority") or resolve_solana_token_owner(info.get("source", ""), tx_meta)
                if amt > 0.0001 and sender and sender != deposit_address:
                    inflows.append({"sender": sender, "amount": amt,
                                    "token_symbol": KNOWN_SOL_MINTS.get(mint, {}).get("symbol", "SPL_TOKEN"),
                                    "mint": mint, "decimals": decimals,
                                    "timestamp": block_time, "tx_hash": sig, "chain": "solana"})
    return inflows


def _iso_ts(ts_str: str, default: int) -> int:
    try:
        return int(datetime.fromisoformat(ts_str.replace("Z", "+00:00")).timestamp()) if ts_str else default
    except Exception:
        return default


def fetch_evm_deposit_inflows(deposit_address: str, chain: str = "base", limit: int = 100) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches native and ERC-20 inflows into the EVM deposit address via Blockscout
    (v2 REST first, v1 fallback). Native + token lists are requested in parallel.
    Returns None when every data source failed (vs [] for a genuinely empty history).
    """
    cinfo = get_chain_info(chain)
    blockscout_api = cinfo.get("blockscoutApi")
    if not blockscout_api:
        return []
    chain_name = cinfo.get("displayName") or cinfo.get("name") or chain
    native_symbol = cinfo.get("nativeCurrency", {}).get("symbol", "ETH")
    chk_addr = to_checksum(deposit_address)
    me = chk_addr.lower()
    now_ts = int(time.time())
    v2_base = blockscout_api[: -len("/api")] if blockscout_api.endswith("/api") else blockscout_api

    f_tx = _POOL.submit(_get_json, f"{v2_base}/api/v2/addresses/{chk_addr}/transactions", 6)
    f_tok = _POOL.submit(_get_json, f"{v2_base}/api/v2/addresses/{chk_addr}/token-transfers", 6)
    v2_tx, v2_tok = f_tx.result(), f_tok.result()

    inflows: List[Dict[str, Any]] = []
    if v2_tx is not None or v2_tok is not None:
        for tx in (v2_tx or {}).get("items") or []:
            if ((tx.get("to") or {}).get("hash") or "").lower() != me:
                continue
            from_addr = (tx.get("from") or {}).get("hash") or ""
            val_str = str(tx.get("value") or "0")
            amt = (int(val_str) if val_str.isdigit() else 0) / 1e18
            if from_addr and from_addr.lower() != me and amt > 0.00001:
                inflows.append({"sender": to_checksum(from_addr), "amount": amt, "token_symbol": native_symbol,
                                "mint": "", "decimals": 18, "timestamp": _iso_ts(tx.get("timestamp", ""), now_ts),
                                "tx_hash": tx.get("hash", ""), "chain": chain_name})
        for tt in (v2_tok or {}).get("items") or []:
            if ((tt.get("to") or {}).get("hash") or "").lower() != me:
                continue
            from_addr = (tt.get("from") or {}).get("hash") or ""
            token = tt.get("token") or {}
            sym = str(token.get("symbol") or "TOKEN").strip()
            dec = token.get("decimals") or 18
            amt = parse_token_amount((tt.get("total") or {}).get("value") or "0", dec, sym)
            if from_addr and from_addr.lower() != me and amt > 0.0001:
                inflows.append({"sender": to_checksum(from_addr), "amount": amt, "token_symbol": sym,
                                "mint": token.get("address_hash") or token.get("address") or "",
                                "decimals": int(dec) if str(dec).isdigit() else 18,
                                "timestamp": _iso_ts(tt.get("timestamp", ""), now_ts),
                                "tx_hash": tt.get("transaction_hash", ""), "chain": chain_name})
        return inflows

    # v1 fallback
    f_native = _POOL.submit(_blockscout_list, blockscout_api, "txlist", chk_addr, limit, "desc")
    f_token = _POOL.submit(_blockscout_list, blockscout_api, "tokentx", chk_addr, limit, "desc")
    v1_native, v1_token = f_native.result(), f_token.result()
    if v1_native is None and v1_token is None:
        return None
    for tx in v1_native or []:
        if (tx.get("to") or "").lower() != me:
            continue
        amt = int(tx.get("value", 0) or 0) / 1e18
        if tx.get("from") and amt > 0.00001:
            inflows.append({"sender": to_checksum(tx["from"]), "amount": amt, "token_symbol": native_symbol,
                            "mint": "", "decimals": 18, "timestamp": int(tx.get("timeStamp", now_ts)),
                            "tx_hash": tx.get("hash", ""), "chain": chain_name})
    for ttx in v1_token or []:
        if (ttx.get("to") or "").lower() != me or not is_valid_token_tx(ttx):
            continue
        sym = str(ttx.get("tokenSymbol") or "TOKEN").strip()
        dec = ttx.get("tokenDecimal", 18)
        amt = parse_token_amount(ttx.get("value", "0"), dec, sym)
        if ttx.get("from") and amt > 0.0001:
            inflows.append({"sender": to_checksum(ttx["from"]), "amount": amt, "token_symbol": sym,
                            "mint": ttx.get("contractAddress", ""),
                            "decimals": int(dec) if str(dec).isdigit() else 18,
                            "timestamp": int(ttx.get("timeStamp", now_ts)),
                            "tx_hash": ttx.get("hash", ""), "chain": chain_name})
    return inflows


def parse_manual_inflow_csv(csv_text: str) -> List[Dict[str, Any]]:
    """
    Parses manual transaction history from CSV / tab-separated text.
    Expected columns: from, to, amount, token_symbol, token_decimal, timestamp, tx_hash
    """
    inflows = []
    lines = [ln.strip() for ln in csv_text.strip().splitlines() if ln.strip()]
    now_ts = int(time.time())
    header_words = {"from", "sender", "from_address", "sender_address", "address", "tx_hash"}

    for idx, line in enumerate(lines):
        parts = [p.strip() for p in re.split(r'[,;\t]+', line)]
        if len(parts) < 3:
            continue
        if idx == 0 and (parts[0].lower() in header_words or (len(parts[0]) < 15 and not parts[0].startswith("0x"))):
            continue

        sender = parts[0]
        symbol = parts[3] if len(parts) > 3 else "TOKEN"
        decimals_str = parts[4] if len(parts) > 4 else "18"
        tx_hash = parts[6] if len(parts) > 6 else f"manual_tx_{idx}"
        try:
            amt = float(parts[2].replace(",", ""))
        except ValueError:
            amt = 0.0
        try:
            ts = int(parts[5]) if len(parts) > 5 else now_ts
        except ValueError:
            ts = now_ts

        if sender and amt > 0:
            inflows.append({
                "sender": sender,
                "amount": amt,
                "token_symbol": symbol.upper(),
                "mint": "",
                "decimals": int(decimals_str) if decimals_str.isdigit() else 18,
                "timestamp": ts,
                "tx_hash": tx_hash,
                "chain": "solana" if SOLANA_ADDR_RE.match(sender) else "evm"
            })
    return inflows


AUTO_SCAN_EVM_CHAINS = ["ethereum", "arbitrum", "polygon", "base", "optimism"]
_EXPLORER_ADDR_BY_CHAIN = [
    ("arbitrum", "https://arbiscan.io/address/"), ("polygon", "https://polygonscan.com/address/"),
    ("optimism", "https://optimistic.etherscan.io/address/"), ("base", "https://basescan.org/address/"),
    ("bnb", "https://bscscan.com/address/"), ("bsc", "https://bscscan.com/address/"),
]


def _sender_explorer_url(addr: str, chain_lower: str) -> str:
    if "solana" in chain_lower or SOLANA_ADDR_RE.match(addr):
        return f"https://solscan.io/account/{addr}"
    for key, base in _EXPLORER_ADDR_BY_CHAIN:
        if key in chain_lower:
            return base + addr
    return f"https://etherscan.io/address/{addr}"


def trace_deposit_inflow(
    target_input: str,
    mode: str = "address",
    chain: str = "auto",
    min_threshold_usd: float = 50.0,
    dust_threshold_usd: float = 5.0,
    exclude_dust: bool = True,
    filter_phishing: bool = True
) -> Dict[str, Any]:
    """
    Core Aggregator & Multi-Tier Spam Filter for Exchange Deposit Inflows.
    When chain='auto', scans ALL major EVM chains in parallel and merges results.
    Groups transactions by sender, converts to USD (each unique token priced once),
    applies cumulative dust & phishing filters, and outputs qualified vs filtered senders.
    """
    started = time.time()
    target_clean = str(target_input or "").strip()
    is_solana = False
    resolved_chain = chain
    is_contract_or_vault = False
    contract_label = ""

    if mode == "address":
        if not target_clean:
            return {"success": False, "error": "Alamat deposit tidak boleh kosong / Deposit address cannot be empty."}
        is_solana = bool(SOLANA_ADDR_RE.match(target_clean))
        if not is_solana and not Web3.is_address(target_clean):
            return {"success": False, "error": "Alamat tidak valid (bukan EVM 0x… atau Solana). / Invalid address (not EVM or Solana)."}

        evm_bytecode_future = None
        if not is_solana:
            check_chain = "ethereum" if chain == "auto" else chain
            w3 = get_web3(get_chain_info(check_chain).get("rpc"))
            if w3:
                evm_bytecode_future = _POOL.submit(w3.eth.get_code, Web3.to_checksum_address(target_clean))

        if is_solana or chain.lower() == "solana":
            is_solana = True
            resolved_chain = "solana"
            raw_inflows = fetch_solana_deposit_inflows(target_clean, limit=100)
        elif chain == "auto":
            futures = {c: _POOL.submit(fetch_evm_deposit_inflows, target_clean, c, 100) for c in AUTO_SCAN_EVM_CHAINS}
            raw_inflows, active, failed = [], [], 0
            for c, fut in futures.items():
                try:
                    c_inflows = fut.result(timeout=20)
                except Exception:
                    c_inflows = None
                if c_inflows is None:
                    failed += 1
                elif c_inflows:
                    raw_inflows.extend(c_inflows)
                    active.append(get_chain_info(c).get("displayName", c.capitalize()))
            if failed == len(AUTO_SCAN_EVM_CHAINS):
                return {"success": False, "error": SOURCE_DOWN_ERROR}
            resolved_chain = f"Multi-Chain EVM ({', '.join(sorted(active) or ['Ethereum, Arbitrum, Base, Polygon, Optimism'])})"
        else:
            resolved_chain = chain.lower().strip()
            if not get_chain_info(resolved_chain).get("blockscoutApi"):
                return {"success": False, "error": f"Chain {resolved_chain} belum didukung pemindai deposit (butuh Blockscout). Gunakan Deteksi Otomatis atau Mode B (CSV). / This chain is not supported by the deposit scanner; use Auto-Detect or CSV mode."}
            raw_inflows = fetch_evm_deposit_inflows(target_clean, chain=resolved_chain, limit=100)
            if raw_inflows is None:
                return {"success": False, "error": SOURCE_DOWN_ERROR}

        cls_info = classify_entity(target_clean)
        is_contract_or_vault = cls_info["category"] in ("bridge_router", "dex_router", "cex_hot_wallet", "mixer")
        contract_label = cls_info.get("name") or ""
        if evm_bytecode_future and not is_contract_or_vault:
            try:
                if len(evm_bytecode_future.result(timeout=6)) > 0:
                    is_contract_or_vault = True
                    contract_label = "Smart Contract (Bytecode Detected)"
            except Exception:
                pass
    else:
        raw_inflows = parse_manual_inflow_csv(target_clean)
        resolved_chain = "multi-chain / CSV"

    # 1. Group by sender
    senders_map: Dict[str, Dict[str, Any]] = {}
    now_ts = int(time.time())
    for item in raw_inflows:
        s_addr = item["sender"]
        sym = item["token_symbol"].upper()
        ts = item.get("timestamp", now_ts)
        item_chain = item.get("chain", resolved_chain)
        s_rec = senders_map.setdefault(s_addr, {
            "tx_count": 0, "first": ts, "last": ts, "tokens": {}, "chains": set(), "has_phishing_token": False
        })
        s_rec["tx_count"] += 1
        s_rec["first"] = min(s_rec["first"], ts)
        s_rec["last"] = max(s_rec["last"], ts)
        if item_chain:
            s_rec["chains"].add(item_chain)
        if filter_phishing and is_spam_symbol(sym):
            s_rec["has_phishing_token"] = True
        tok = s_rec["tokens"].setdefault(sym, {"amount": 0.0, "mint": item.get("mint", "")})
        tok["amount"] += item["amount"]

    # 2. Price every unique token once, in parallel
    unique_tokens = {(sym, t.get("mint") or "") for rec in senders_map.values() for sym, t in rec["tokens"].items()}
    price_futures = {k: _POOL.submit(get_token_usd_price, k[0], k[1]) for k in unique_tokens}
    prices: Dict[Any, float] = {}
    for k, fut in price_futures.items():
        try:
            prices[k] = fut.result(timeout=8)
        except Exception:
            prices[k] = 0.0

    # 3. USD valuation + multi-tier spam filter
    qualified_senders, filtered_senders = [], []
    total_usd_all = qualified_usd = 0.0
    for s_addr, data in senders_map.items():
        token_breakdowns = []
        total_usd = 0.0
        for sym, tinfo in data["tokens"].items():
            price = prices.get((sym, tinfo.get("mint") or ""), 0.0)
            usd_val = tinfo["amount"] * price
            total_usd += usd_val
            token_breakdowns.append({"symbol": sym, "amount": tinfo["amount"], "usd_value": usd_val, "unit_price": price})
        total_usd_all += total_usd

        chains_list = sorted(data["chains"]) or [resolved_chain]
        sender_obj = {
            "sender_address": s_addr,
            "total_deposit_usd": round(total_usd, 2),
            "tx_count": data["tx_count"],
            "first_deposit_timestamp": data["first"],
            "first_deposit_days_ago": max(0, (now_ts - data["first"]) // 86400),
            "last_deposit_timestamp": data["last"],
            "last_deposit_days_ago": max(0, (now_ts - data["last"]) // 86400),
            "tokens": token_breakdowns,
            "chain": ", ".join(chains_list),
            "explorer_url": _sender_explorer_url(s_addr, chains_list[0].lower())
        }

        if filter_phishing and data["has_phishing_token"]:
            filter_reason = "phishing_spam_token"
        elif exclude_dust and data["tx_count"] == 1 and total_usd < dust_threshold_usd:
            filter_reason = "single_tx_dust"
        elif total_usd < min_threshold_usd:
            filter_reason = "below_min_threshold"
        else:
            filter_reason = None

        if filter_reason:
            sender_obj["filter_reason"] = filter_reason
            filtered_senders.append(sender_obj)
        else:
            qualified_senders.append(sender_obj)
            qualified_usd += total_usd

    qualified_senders.sort(key=lambda x: x["total_deposit_usd"], reverse=True)
    filtered_senders.sort(key=lambda x: x["total_deposit_usd"], reverse=True)

    if "Multi-Chain" in resolved_chain:
        scope_note = "Multi-Chain EVM scan aggregated across Ethereum, Arbitrum, Base, Polygon, Optimism."
    elif is_solana:
        scope_note = f"Solana: scanned the {SOLANA_TX_SCAN_LIMIT} most recent transactions. USD value estimated at current market price."
    else:
        scope_note = "Showing up to 100 most recent transactions (Personal Deposit Scope). USD value estimated using current market price."

    return {
        "success": True,
        "target_address": target_clean,
        "mode": mode,
        "chain": resolved_chain,
        "elapsed_ms": int((time.time() - started) * 1000),
        "is_contract_or_vault": is_contract_or_vault,
        "contract_label": contract_label,
        "scan_scope_note": scope_note,
        "summary": {
            "total_senders": len(senders_map),
            "qualified_count": len(qualified_senders),
            "filtered_count": len(filtered_senders),
            "total_cumulative_deposit_usd": round(total_usd_all, 2),
            "qualified_cumulative_deposit_usd": round(qualified_usd, 2),
            "min_threshold_usd": min_threshold_usd,
            "dust_threshold_usd": dust_threshold_usd
        },
        "qualified_senders": qualified_senders,
        "filtered_senders": filtered_senders
    }

# Backward compatibility alias
track_relay = track_cross_chain
