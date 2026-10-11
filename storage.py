"""
Local persistence for Tab 5: saved traces (re-runnable) and marked addresses.

Everything lives in ./data (gitignored) as small JSON files, written atomically so a crash
mid-write never corrupts them. This is a single-user desktop app, so a process-wide lock is
enough for concurrency.
"""
import json
import os
import re
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TRACES_FILE = "saved_traces.json"
MARKS_FILE = "marked_addresses.json"

MAX_TRACES = 200
MAX_SNAPSHOT_BYTES = 3_000_000
MAX_MARKS = 5000
MARK_COLORS = ("red", "amber", "lime", "cyan", "purple")

_LOCK = threading.Lock()


def _path(name: str) -> str:
    return os.path.join(DATA_DIR, name)


def _read(name: str, default: Any) -> Any:
    try:
        with open(_path(name), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def _write(name: str, value: Any) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = _path(name) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(value, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, _path(name))


def _clean_text(value: Any, limit: int) -> str:
    return re.sub(r"[\x00-\x1f]", " ", str(value or "")).strip()[:limit]


# ==================== SAVED TRACES ====================

def _summary(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    stats = snapshot.get("stats") or {}
    return {
        "nodes": len(snapshot.get("nodes") or []),
        "edges": len(snapshot.get("edges") or []),
        "findings": len(snapshot.get("findings") or []),
        "clusters": len(snapshot.get("clusters") or []),
        "eoa": stats.get("eoa", 0),
        "contracts": stats.get("contracts", 0),
    }


def list_traces() -> List[Dict[str, Any]]:
    """All saved traces, newest first, without their (large) snapshots."""
    with _LOCK:
        traces = _read(TRACES_FILE, [])
    items = [{k: v for k, v in t.items() if k != "snapshot"} for t in traces]
    return sorted(items, key=lambda t: t.get("updated", 0), reverse=True)


def get_trace(trace_id: str) -> Optional[Dict[str, Any]]:
    with _LOCK:
        return next((t for t in _read(TRACES_FILE, []) if t.get("id") == trace_id), None)


def save_trace(name: str, params: Dict[str, Any], snapshot: Dict[str, Any],
               trace_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a saved trace, or replace the snapshot of an existing one (`trace_id`).
    The previous snapshot's node ids are kept so the next re-trace can show what is new."""
    blob = json.dumps(snapshot, ensure_ascii=False)
    if len(blob.encode("utf-8")) > MAX_SNAPSHOT_BYTES:
        raise ValueError("snapshot too large")
    seeds = [str(s)[:100] for s in (snapshot.get("seeds") or params.get("seeds") or [])][:10]
    clean_params = {k: params.get(k) for k in ("chain", "direction", "depth", "fanout", "min_native",
                                                "min_stable_usd", "tokens") if k in params}
    clean_params["seeds"] = seeds
    now = int(time.time())
    with _LOCK:
        traces = _read(TRACES_FILE, [])
        existing = next((t for t in traces if t.get("id") == trace_id), None) if trace_id else None
        if existing:
            existing["history"] = (existing.get("history") or [])[-9:] + [
                {"at": existing["updated"], **existing["summary"]}]
            existing.update(snapshot=snapshot, summary=_summary(snapshot), updated=now,
                            params=clean_params or existing["params"],
                            name=_clean_text(name, 80) or existing["name"])
            record = existing
        else:
            if len(traces) >= MAX_TRACES:
                traces.sort(key=lambda t: t.get("updated", 0))
                traces.pop(0)
            record = {
                "id": uuid.uuid4().hex[:12],
                "name": _clean_text(name, 80) or f"Trace {time.strftime('%Y-%m-%d %H:%M')}",
                "chain": str(clean_params.get("chain") or snapshot.get("chain") or ""),
                "params": clean_params,
                "created": now,
                "updated": now,
                "summary": _summary(snapshot),
                "history": [],
                "snapshot": snapshot,
            }
            traces.append(record)
        _write(TRACES_FILE, traces)
    return {k: v for k, v in record.items() if k != "snapshot"}


def delete_trace(trace_id: str) -> bool:
    with _LOCK:
        traces = _read(TRACES_FILE, [])
        kept = [t for t in traces if t.get("id") != trace_id]
        if len(kept) == len(traces):
            return False
        _write(TRACES_FILE, kept)
    return True


# ==================== MARKED ADDRESSES ====================

def _mark_key(chain: str, address: str) -> str:
    # EVM addresses are case-insensitive, Solana base58 is not
    address = address.strip()
    return f"{chain}:{address.lower() if address.startswith('0x') else address}"


def list_marks() -> Dict[str, Dict[str, Any]]:
    with _LOCK:
        return _read(MARKS_FILE, {})


def set_mark(chain: str, address: str, label: str, color: str = "amber", note: str = "") -> Dict[str, Any]:
    chain = _clean_text(chain, 20).lower()
    address = _clean_text(address, 100)
    if not chain or not address:
        raise ValueError("chain and address are required")
    mark = {
        "chain": chain,
        "address": address,
        "label": _clean_text(label, 40) or "Marked",
        "color": color if color in MARK_COLORS else "amber",
        "note": _clean_text(note, 300),
        "updated": int(time.time()),
    }
    with _LOCK:
        marks = _read(MARKS_FILE, {})
        if len(marks) >= MAX_MARKS and _mark_key(chain, address) not in marks:
            raise ValueError("too many marked addresses")
        marks[_mark_key(chain, address)] = mark
        _write(MARKS_FILE, marks)
    return mark


def delete_mark(chain: str, address: str) -> bool:
    with _LOCK:
        marks = _read(MARKS_FILE, {})
        if marks.pop(_mark_key(chain.lower(), address), None) is None:
            return False
        _write(MARKS_FILE, marks)
    return True
