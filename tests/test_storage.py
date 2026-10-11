"""Saved traces & marked addresses: storage module and Flask endpoints (isolated temp data dir)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage  # noqa: E402

SNAP = {
    "chain": "solana", "seeds": ["SeedA"], "stats": {"eoa": 2, "contracts": 1},
    "nodes": [{"id": "SeedA"}, {"id": "X"}, {"id": "Y"}],
    "edges": [{"from": "SeedA", "to": "X"}], "findings": [{"type": "cex_deposit"}], "clusters": [],
}
PARAMS = {"chain": "solana", "direction": "forward", "depth": 2, "fanout": 4, "tokens": ["SOL"], "evil": "x"}


@pytest.fixture(autouse=True)
def tmp_data(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", str(tmp_path))
    return tmp_path


def test_save_list_get_delete():
    rec = storage.save_trace("My trace", PARAMS, SNAP)
    assert rec["name"] == "My trace" and rec["summary"]["nodes"] == 3 and rec["summary"]["contracts"] == 1
    assert "snapshot" not in rec and "evil" not in rec["params"] and rec["params"]["seeds"] == ["SeedA"]
    listed = storage.list_traces()
    assert len(listed) == 1 and "snapshot" not in listed[0]
    full = storage.get_trace(rec["id"])
    assert full["snapshot"]["nodes"][1]["id"] == "X"
    assert storage.delete_trace(rec["id"]) and storage.list_traces() == []
    assert not storage.delete_trace("missing")


def test_update_keeps_history():
    rec = storage.save_trace("T", PARAMS, SNAP)
    bigger = {**SNAP, "nodes": SNAP["nodes"] + [{"id": "Z"}]}
    upd = storage.save_trace("", PARAMS, bigger, trace_id=rec["id"])
    assert upd["id"] == rec["id"] and upd["name"] == "T"
    assert upd["summary"]["nodes"] == 4 and upd["history"][-1]["nodes"] == 3
    assert len(storage.list_traces()) == 1


def test_default_name_and_text_cleaning():
    rec = storage.save_trace("  bad\x00name\nwith newline  " + "x" * 200, PARAMS, SNAP)
    assert "\x00" not in rec["name"] and "\n" not in rec["name"] and len(rec["name"]) <= 80
    assert storage.save_trace("", PARAMS, SNAP)["name"].startswith("Trace ")


def test_snapshot_size_limit(monkeypatch):
    monkeypatch.setattr(storage, "MAX_SNAPSHOT_BYTES", 100)
    with pytest.raises(ValueError):
        storage.save_trace("big", PARAMS, SNAP)


def test_trace_limit_drops_oldest(monkeypatch):
    monkeypatch.setattr(storage, "MAX_TRACES", 3)
    ids = [storage.save_trace(f"t{i}", PARAMS, SNAP)["id"] for i in range(4)]
    kept = {t["id"] for t in storage.list_traces()}
    assert len(kept) == 3 and ids[-1] in kept


def test_marks_roundtrip_and_evm_case_insensitive():
    storage.set_mark("ethereum", "0xAbC0000000000000000000000000000000000001", "Suspect", "red", "note")
    marks = storage.list_marks()
    assert marks["ethereum:0xabc0000000000000000000000000000000000001"]["label"] == "Suspect"
    # same EVM address in another case overwrites instead of duplicating
    storage.set_mark("ethereum", "0xabc0000000000000000000000000000000000001", "Updated", "nope-color")
    m = storage.list_marks()
    assert len(m) == 1 and next(iter(m.values()))["color"] == "amber"
    assert storage.delete_mark("ethereum", "0xABC0000000000000000000000000000000000001")
    assert storage.list_marks() == {}


def test_solana_marks_are_case_sensitive():
    storage.set_mark("solana", "AbcSolana1111111111111111111111111", "a")
    storage.set_mark("solana", "abcSolana1111111111111111111111111", "b")
    assert len(storage.list_marks()) == 2


def test_mark_requires_address():
    with pytest.raises(ValueError):
        storage.set_mark("solana", "", "x")


def test_corrupt_file_is_tolerated(tmp_data):
    (tmp_data / storage.TRACES_FILE).write_text("{not json", encoding="utf-8")
    assert storage.list_traces() == []
    storage.save_trace("fresh", PARAMS, SNAP)
    assert len(storage.list_traces()) == 1


# ---- Flask endpoints ----

@pytest.fixture
def client():
    import app as app_module
    return app_module.app.test_client()


def test_api_saved_flow(client):
    assert client.post("/api/flow/saved", json={"name": "x"}).status_code == 400
    r = client.post("/api/flow/saved", json={"name": "API", "params": PARAMS, "snapshot": SNAP}).json
    assert r["success"]
    tid = r["trace"]["id"]
    assert client.get("/api/flow/saved").json["traces"][0]["id"] == tid
    assert client.get(f"/api/flow/saved/{tid}").json["trace"]["snapshot"]["nodes"]
    assert client.get("/api/flow/saved/nope").status_code == 404
    assert client.delete(f"/api/flow/saved/{tid}").json["success"]


def test_api_marks(client):
    body = {"chain": "solana", "address": "AbcSolana1111111111111111111111111", "label": "Hot", "color": "cyan"}
    assert client.post("/api/flow/marks", json=body).json["mark"]["color"] == "cyan"
    assert len(client.get("/api/flow/marks").json["marks"]) == 1
    assert client.post("/api/flow/marks", json={"chain": "solana"}).status_code == 400
    assert client.delete("/api/flow/marks", json=body).json["success"]
