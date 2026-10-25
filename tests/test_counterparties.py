"""Unit tests for Tab 6 counterparties aggregation, filtering, and metrics."""
import os
import sys
import time
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import counterparties as cp


def test_aggregate_counterparties_direction_filtering(monkeypatch):
    # Mock token price map to return 1.0 for TEST
    monkeypatch.setattr(cp, "get_token_price_map", lambda transfers, chain="ethereum": {("TEST", ""): 2.0})

    target = "0xTarget1111111111111111111111111111111111"
    sender_in = "0xSenderIn2222222222222222222222222222222"
    recipient_out = "0xRecipientOut33333333333333333333333333"

    now_ts = int(time.time())
    transfers = [
        # Inflow: sender_in -> target (amount: 10 => $20)
        {"from": sender_in, "to": target, "token": "TEST", "mint": "", "amount": 10.0, "ts": now_ts - 100, "tx": "0xtx1", "chain": "ethereum"},
        # Outflow: target -> recipient_out (amount: 5 => $10)
        {"from": target, "to": recipient_out, "token": "TEST", "mint": "", "amount": 5.0, "ts": now_ts - 200, "tx": "0xtx2", "chain": "ethereum"},
        # Self-transfer: target -> target (should be ignored)
        {"from": target, "to": target, "token": "TEST", "mint": "", "amount": 1.0, "ts": now_ts - 50, "tx": "0xtx3", "chain": "ethereum"},
    ]

    # 1. Test direction = "all"
    res_all = cp.aggregate_counterparties_data(transfers, target, time_range="all", direction="all", sort_by="usd")
    c_list_all = res_all["counterparties"]
    assert len(c_list_all) == 2
    assert res_all["summary"]["total_volume_usd"] == 30.0
    assert res_all["summary"]["total_inflow_usd"] == 20.0
    assert res_all["summary"]["total_outflow_usd"] == 10.0

    # 2. Test direction = "in"
    res_in = cp.aggregate_counterparties_data(transfers, target, time_range="all", direction="in", sort_by="usd")
    c_list_in = res_in["counterparties"]
    assert len(c_list_in) == 1
    assert c_list_in[0]["address"] == sender_in
    assert c_list_in[0]["flow_type"] == "in"
    assert c_list_in[0]["in_volume_usd"] == 20.0
    assert c_list_in[0]["out_volume_usd"] == 0.0

    # 3. Test direction = "out"
    res_out = cp.aggregate_counterparties_data(transfers, target, time_range="all", direction="out", sort_by="usd")
    c_list_out = res_out["counterparties"]
    assert len(c_list_out) == 1
    assert c_list_out[0]["address"] == recipient_out
    assert c_list_out[0]["flow_type"] == "out"
    assert c_list_out[0]["out_volume_usd"] == 10.0
    assert c_list_out[0]["in_volume_usd"] == 0.0


def test_aggregate_counterparties_time_range(monkeypatch):
    monkeypatch.setattr(cp, "get_token_price_map", lambda transfers, chain="ethereum": {("TEST", ""): 1.0})

    target = "0xTarget1111111111111111111111111111111111"
    recent_cp = "0xRecent22222222222222222222222222222222"
    old_cp = "0xOld333333333333333333333333333333333333"

    now_ts = int(time.time())
    transfers = [
        {"from": recent_cp, "to": target, "token": "TEST", "mint": "", "amount": 10.0, "ts": now_ts - 600, "tx": "0xtx1", "chain": "base"},  # 10m ago
        {"from": old_cp, "to": target, "token": "TEST", "mint": "", "amount": 20.0, "ts": now_ts - 7200, "tx": "0xtx2", "chain": "base"},  # 2h ago
    ]

    # Under 1h: only recent_cp should be included
    res_1h = cp.aggregate_counterparties_data(transfers, target, time_range="1h", direction="all", sort_by="usd")
    assert len(res_1h["counterparties"]) == 1
    assert res_1h["counterparties"][0]["address"] == recent_cp

    # Under 24h: both should be included
    res_24h = cp.aggregate_counterparties_data(transfers, target, time_range="24h", direction="all", sort_by="usd")
    assert len(res_24h["counterparties"]) == 2


def test_aggregate_counterparties_sorting(monkeypatch):
    monkeypatch.setattr(cp, "get_token_price_map", lambda transfers, chain="ethereum": {("TEST", ""): 1.0})

    target = "0xTarget1111111111111111111111111111111111"
    high_vol_cp = "0xHighVol2222222222222222222222222222222"
    high_tx_cp = "0xHighTx33333333333333333333333333333333"

    now_ts = int(time.time())
    transfers = [
        # 1 tx of $1000
        {"from": high_vol_cp, "to": target, "token": "TEST", "mint": "", "amount": 1000.0, "ts": now_ts - 100, "tx": "0xtx1", "chain": "base"},
        # 3 txs of $10 each ($30 total)
        {"from": high_tx_cp, "to": target, "token": "TEST", "mint": "", "amount": 10.0, "ts": now_ts - 150, "tx": "0xtx2", "chain": "base"},
        {"from": high_tx_cp, "to": target, "token": "TEST", "mint": "", "amount": 10.0, "ts": now_ts - 120, "tx": "0xtx3", "chain": "base"},
        {"from": high_tx_cp, "to": target, "token": "TEST", "mint": "", "amount": 10.0, "ts": now_ts - 90, "tx": "0xtx4", "chain": "base"},
    ]

    # Sort by USD: high_vol_cp ranks #1
    res_usd = cp.aggregate_counterparties_data(transfers, target, sort_by="usd")
    assert res_usd["counterparties"][0]["address"] == high_vol_cp
    assert res_usd["counterparties"][0]["rank"] == 1

    # Sort by TX count: high_tx_cp ranks #1
    res_tx = cp.aggregate_counterparties_data(transfers, target, sort_by="tx")
    assert res_tx["counterparties"][0]["address"] == high_tx_cp
    assert res_tx["counterparties"][0]["rank"] == 1
