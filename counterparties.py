"""
Top Counterparties Analyzer Module (Tab 6).

Analyzes wallet transaction history to identify, rank, and classify top counterparties
by USD Volume or Transaction Count. Supports multi-timeframe filtering (1h, 24h, 1w, 1m, all),
directional flow filtering (all, in, out), token breakdowns, entity tagging, and instant
client-side re-aggregation.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

from web3 import Web3

import relay_core as rc
import flow_trace as ft

TIME_RANGE_SECONDS = {
    "1h": 3600,
    "24h": 86400,
    "1w": 7 * 86400,       # 604,800s
    "1m": 30 * 86400,      # 2,592,000s
    "all": None,
}

SUPPORTED_CHAINS = ["solana", "base", "ethereum", "arbitrum", "optimism", "polygon", "bsc"]


def _clean_address(addr: str) -> str:
    return str(addr or "").strip()


def _is_solana(addr: str) -> bool:
    return bool(rc.SOLANA_ADDR_RE.match(_clean_address(addr)))


def _is_evm(addr: str) -> bool:
    clean = _clean_address(addr)
    return bool(clean.startswith("0x") and Web3.is_address(clean))


def fetch_evm_all_transfers(chain: str, checksum_addr: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Fetches both native transactions and ERC-20 token transfers for an EVM address.
    Unlike flow_trace (which restricts to TARGET_TOKENS), this preserves all legitimate
    ERC-20 transfers (filtered against scam phishing tokens via rc.is_valid_token_tx).
    """
    cinfo = rc.get_chain_info(chain)
    chain_name = cinfo.get("displayName") or cinfo.get("name") or chain
    native_symbol = cinfo.get("nativeCurrency", {}).get("symbol", "ETH")
    now_ts = int(time.time())

    if ft.etherscan_supports(chain):
        f_native = rc._POOL.submit(ft._etherscan_list, chain, "txlist", checksum_addr)
        f_token = rc._POOL.submit(ft._etherscan_list, chain, "tokentx", checksum_addr)
        source = "Etherscan v2"
    else:
        api = cinfo.get("blockscoutApi")
        if not api:
            return [], {"ok": False, "source": "none", "raw_count": 0}
        def fetch(action):
            for attempt in range(3):
                rows = rc._blockscout_list(api, action, checksum_addr, 300, "desc")
                if rows is not None:
                    return rows
                time.sleep(0.8 * (attempt + 1))
            return None
        f_native = rc._POOL.submit(fetch, "txlist")
        f_token = rc._POOL.submit(fetch, "tokentx")
        source = "Blockscout"

    native_rows = f_native.result() or []
    token_rows = f_token.result() or []
    ok = bool(native_rows or token_rows)

    transfers: List[Dict[str, Any]] = []

    # Process native transactions
    for tx in native_rows:
        if str(tx.get("isError", "0")) == "1":
            continue
        val = int(tx.get("value", 0) or 0)
        from_addr = rc.to_checksum(tx.get("from") or "")
        to_addr = rc.to_checksum(tx.get("to") or "")
        amt = val / 1e18
        if amt > 0 and from_addr and to_addr:
            transfers.append({
                "from": from_addr,
                "to": to_addr,
                "token": native_symbol,
                "mint": "",
                "decimals": 18,
                "amount": amt,
                "ts": int(tx.get("timeStamp") or now_ts),
                "tx": tx.get("hash", ""),
                "chain": chain,
                "chain_name": chain_name,
            })

    # Process token transfers
    for ttx in token_rows:
        if not rc.is_valid_token_tx(ttx):
            continue
        sym = str(ttx.get("tokenSymbol") or ttx.get("symbol") or "TOKEN").strip().upper()
        dec = ttx.get("tokenDecimal", 18)
        amt = rc.parse_token_amount(ttx.get("value", "0"), dec, sym)
        from_addr = rc.to_checksum(ttx.get("from") or "")
        to_addr = rc.to_checksum(ttx.get("to") or "")
        contract = (ttx.get("contractAddress") or "").lower()
        if amt > 0 and from_addr and to_addr:
            transfers.append({
                "from": from_addr,
                "to": to_addr,
                "token": sym,
                "mint": contract,
                "decimals": int(dec) if str(dec).isdigit() else 18,
                "amount": amt,
                "ts": int(ttx.get("timeStamp") or now_ts),
                "tx": ttx.get("hash", ""),
                "chain": chain,
                "chain_name": chain_name,
            })

    return transfers, {"ok": ok, "source": source, "raw_count": len(native_rows) + len(token_rows)}


def fetch_solana_all_transfers(address: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Fetches all native SOL and SPL transfers for a Solana address.
    """
    res, meta = ft.fetch_solana_transfers("solana", address)
    out: List[Dict[str, Any]] = []
    for t in res or []:
        out.append({
            "from": t["from"],
            "to": t["to"],
            "token": t["token"],
            "mint": rc.KNOWN_SOL_MINTS.get(t.get("token"), {}).get("mint", ""),
            "decimals": 9 if t["token"] == "SOL" else 6,
            "amount": float(t["amount"]),
            "ts": int(t.get("ts") or time.time()),
            "tx": t.get("tx", ""),
            "chain": "solana",
            "chain_name": "Solana",
        })
    return out, meta


def get_token_price_map(transfers: List[Dict[str, Any]], chain: str = "ethereum") -> Dict[Tuple[str, str], float]:
    """
    Prices all distinct tokens in the transfers list.
    Returns {(symbol, mint): price_usd}.
    """
    unique_tokens = {(t["token"].upper(), t.get("mint", "").lower(), t.get("chain", chain)) for t in transfers}
    futures = {
        (sym, mint): rc._POOL.submit(rc.get_token_usd_price, sym, mint, ch)
        for sym, mint, ch in unique_tokens
    }
    price_map: Dict[Tuple[str, str], float] = {}
    for key, fut in futures.items():
        try:
            price_map[key] = float(fut.result(timeout=5) or 0.0)
        except Exception:
            price_map[key] = 1.0 if key[0] in rc.STABLECOIN_SYMBOLS else 0.0
    return price_map


def aggregate_counterparties_data(
    transfers: List[Dict[str, Any]],
    target_address: str,
    time_range: str = "all",
    direction: str = "all",
    sort_by: str = "usd"
) -> Dict[str, Any]:
    """
    Filters and aggregates transfers into ranked counterparties + summary metrics.
    """
    now_ts = int(time.time())
    max_age_s = TIME_RANGE_SECONDS.get(time_range)
    target_lower = target_address.lower()

    # Price tokens
    price_map = get_token_price_map(transfers)

    # Attach computed USD values and determine counterparty
    counterparties_map: Dict[str, Dict[str, Any]] = {}
    normalized_transfers: List[Dict[str, Any]] = []

    for t in transfers:
        amt = float(t.get("amount", 0.0) or 0.0)
        sym = t.get("token", "").upper()
        mint = t.get("mint", "").lower()
        price = price_map.get((sym, mint), 0.0)
        usd_val = amt * price

        ts = int(t.get("ts") or now_ts)
        from_addr = t.get("from", "")
        to_addr = t.get("to", "")
        from_lower = from_addr.lower()
        to_lower = to_addr.lower()

        # Determine direction relative to target
        if from_lower == target_lower:
            flow_dir = "out"
            cp_addr = to_addr
        elif to_lower == target_lower:
            flow_dir = "in"
            cp_addr = from_addr
        else:
            continue

        if not cp_addr or cp_addr.lower() == target_lower:
            # Skip self-transfers or empty addresses
            continue

        enriched_tx = {
            "from": from_addr,
            "to": to_addr,
            "counterparty": cp_addr,
            "dir": flow_dir,
            "token": sym,
            "amount": round(amt, 6),
            "price_usd": round(price, 4),
            "usd": round(usd_val, 2),
            "ts": ts,
            "tx": t.get("tx", ""),
            "chain": t.get("chain", ""),
            "chain_name": t.get("chain_name", t.get("chain", "")),
        }
        normalized_transfers.append(enriched_tx)

        # Check time range filter
        if max_age_s is not None and (now_ts - ts) > max_age_s:
            continue

        # Check direction filter
        if direction == "in" and flow_dir != "in":
            continue
        if direction == "out" and flow_dir != "out":
            continue

        # Accumulate counterparty
        rec = counterparties_map.get(cp_addr)
        if not rec:
            rec = {
                "address": cp_addr,
                "total_volume_usd": 0.0,
                "in_volume_usd": 0.0,
                "out_volume_usd": 0.0,
                "net_volume_usd": 0.0,
                "total_tx_count": 0,
                "in_tx_count": 0,
                "out_tx_count": 0,
                "first_seen_ts": ts,
                "last_seen_ts": ts,
                "latest_tx_hash": t.get("tx", ""),
                "chain": t.get("chain", ""),
                "chain_name": t.get("chain_name", ""),
                "tokens": {},
            }
            counterparties_map[cp_addr] = rec

        rec["total_volume_usd"] += usd_val
        rec["total_tx_count"] += 1
        if flow_dir == "in":
            rec["in_volume_usd"] += usd_val
            rec["in_tx_count"] += 1
        else:
            rec["out_volume_usd"] += usd_val
            rec["out_tx_count"] += 1

        rec["first_seen_ts"] = min(rec["first_seen_ts"], ts)
        rec["last_seen_ts"] = max(rec["last_seen_ts"], ts)
        if ts >= rec["last_seen_ts"]:
            rec["latest_tx_hash"] = t.get("tx", "")

        # Token breakdown
        tok = rec["tokens"].get(sym)
        if not tok:
            tok = {"symbol": sym, "amount": 0.0, "usd": 0.0}
            rec["tokens"][sym] = tok
        tok["amount"] += amt
        tok["usd"] += usd_val

    # Post-process counterparties list
    cp_list: List[Dict[str, Any]] = []
    for cp_addr, rec in counterparties_map.items():
        cls_info = rc.classify_entity(cp_addr)
        in_c = rec["in_tx_count"]
        out_c = rec["out_tx_count"]
        flow_type = "both" if (in_c > 0 and out_c > 0) else ("in" if in_c > 0 else "out")

        # Convert tokens dict to sorted list
        token_list = sorted(rec["tokens"].values(), key=lambda x: x["usd"], reverse=True)
        for tok_item in token_list:
            tok_item["amount"] = round(tok_item["amount"], 4)
            tok_item["usd"] = round(tok_item["usd"], 2)

        is_contract = cls_info["category"] in ("bridge_router", "dex_router", "paymaster", "public_faucet") or bool(
            cls_info.get("name") and any(w in cls_info["name"] for w in ("Router", "Pool", "Proxy", "Contract", "Bridge"))
        )

        cp_list.append({
            "address": cp_addr,
            "label": cls_info.get("name") or "",
            "category": cls_info.get("category", "private_eoa"),
            "is_noisy": cls_info.get("is_noisy", False),
            "is_contract": is_contract,
            "is_cex": cls_info.get("category") == "cex_hot_wallet",
            "total_volume_usd": round(rec["total_volume_usd"], 2),
            "in_volume_usd": round(rec["in_volume_usd"], 2),
            "out_volume_usd": round(rec["out_volume_usd"], 2),
            "net_volume_usd": round(rec["in_volume_usd"] - rec["out_volume_usd"], 2),
            "total_tx_count": rec["total_tx_count"],
            "in_tx_count": in_c,
            "out_tx_count": out_c,
            "flow_type": flow_type,
            "tokens": token_list,
            "first_seen_ts": rec["first_seen_ts"],
            "last_seen_ts": rec["last_seen_ts"],
            "first_seen_days_ago": max(0, (now_ts - rec["first_seen_ts"]) // 86400),
            "last_seen_days_ago": max(0, (now_ts - rec["last_seen_ts"]) // 86400),
            "latest_tx_hash": rec["latest_tx_hash"],
            "chain": rec["chain"],
            "chain_name": rec["chain_name"],
            "explorer_url": rc._sender_explorer_url(cp_addr, rec["chain"]),
        })

    # Sort counterparties
    if sort_by == "tx":
        cp_list.sort(key=lambda x: (-x["total_tx_count"], -x["total_volume_usd"]))
    else:  # default 'usd'
        cp_list.sort(key=lambda x: (-x["total_volume_usd"], -x["total_tx_count"]))

    # Assign 1-indexed ranks
    for idx, cp in enumerate(cp_list):
        cp["rank"] = idx + 1

    # Summary metrics
    total_vol = sum(c["total_volume_usd"] for c in cp_list)
    total_in = sum(c["in_volume_usd"] for c in cp_list)
    total_out = sum(c["out_volume_usd"] for c in cp_list)
    total_tx = sum(c["total_tx_count"] for c in cp_list)
    total_in_tx = sum(c["in_tx_count"] for c in cp_list)
    total_out_tx = sum(c["out_tx_count"] for c in cp_list)
    top_cp = cp_list[0] if cp_list else None
    dom_pct = round(top_cp["total_volume_usd"] / total_vol * 100, 1) if (total_vol > 0 and top_cp) else 0.0

    summary = {
        "total_counterparties": len(cp_list),
        "total_volume_usd": round(total_vol, 2),
        "total_inflow_usd": round(total_in, 2),
        "total_outflow_usd": round(total_out, 2),
        "inflow_share_pct": round(total_in / total_vol * 100, 1) if total_vol > 0 else 0.0,
        "outflow_share_pct": round(total_out / total_vol * 100, 1) if total_vol > 0 else 0.0,
        "total_tx_count": total_tx,
        "total_inflow_tx": total_in_tx,
        "total_outflow_tx": total_out_tx,
        "top_counterparty": {
            "address": top_cp["address"],
            "label": top_cp["label"],
            "total_volume_usd": top_cp["total_volume_usd"],
            "total_tx_count": top_cp["total_tx_count"],
            "flow_type": top_cp["flow_type"],
            "dominance_pct": dom_pct,
        } if top_cp else None,
        "time_range": time_range,
        "direction": direction,
        "sort_by": sort_by,
    }

    return {
        "summary": summary,
        "counterparties": cp_list,
        "all_transfers": normalized_transfers,
    }


def analyze_top_counterparties(
    target_address: str,
    chain: str = "auto",
    time_range: str = "all",
    direction: str = "all",
    sort_by: str = "usd"
) -> Dict[str, Any]:
    """
    Main entry point for Tab 6: Top Counterparties Analyzer.
    """
    started = time.time()
    clean_addr = _clean_address(target_address)
    if not clean_addr:
        return {"success": False, "error": "Alamat wallet tidak boleh kosong / Wallet address cannot be empty."}

    is_sol = _is_solana(clean_addr)
    is_e = _is_evm(clean_addr)
    if not is_sol and not is_e:
        return {"success": False, "error": "Alamat tidak valid (bukan EVM 0x… atau Solana Base58). / Invalid address format."}

    target_chk = clean_addr if is_sol else rc.to_checksum(clean_addr)
    resolved_chain = "solana" if is_sol else chain.lower().strip()

    raw_transfers: List[Dict[str, Any]] = []
    meta_info: Dict[str, Any] = {}

    if is_sol or resolved_chain == "solana":
        resolved_chain = "solana"
        raw_transfers, meta_info = fetch_solana_all_transfers(target_chk)
    elif resolved_chain == "auto":
        futures = {
            c: rc._POOL.submit(fetch_evm_all_transfers, c, target_chk)
            for c in rc.AUTO_SCAN_EVM_CHAINS
        }
        active_chains = []
        for c, fut in futures.items():
            try:
                c_txs, c_meta = fut.result(timeout=20)
                if c_txs:
                    raw_transfers.extend(c_txs)
                    active_chains.append(rc.get_chain_info(c).get("displayName", c.capitalize()))
            except Exception:
                pass
        resolved_chain = f"Multi-Chain EVM ({', '.join(sorted(active_chains) or ['Base, Ethereum, Arbitrum'])})"
    else:
        raw_transfers, meta_info = fetch_evm_all_transfers(resolved_chain, target_chk)

    # Classify the analyzed target entity
    target_cls = rc.classify_entity(target_chk)
    is_target_contract = target_cls["category"] in ("bridge_router", "dex_router", "cex_hot_wallet", "mixer", "paymaster")
    target_account = "contract" if is_target_contract else ("eoa" if not is_sol else "wallet")

    # Aggregate
    agg = aggregate_counterparties_data(
        raw_transfers,
        target_chk,
        time_range=time_range,
        direction=direction,
        sort_by=sort_by
    )

    elapsed_ms = int((time.time() - started) * 1000)

    return {
        "success": True,
        "target_address": target_chk,
        "is_solana": is_sol,
        "chain": resolved_chain,
        "time_range": time_range,
        "direction": direction,
        "sort_by": sort_by,
        "elapsed_ms": elapsed_ms,
        "target_entity": {
            "label": target_cls.get("name") or "",
            "category": target_cls.get("category", "private_eoa"),
            "account_kind": target_account,
            "is_contract": is_target_contract,
        },
        "summary": agg["summary"],
        "counterparties": agg["counterparties"],
        "all_transfers": agg["all_transfers"],
    }
