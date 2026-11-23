#!/usr/bin/env python3
"""Supabase 무료 플랜 휴면(7일 무활동 시 일시정지) 방지: keepalive() RPC로 DB에 쓰기 1회"""
import json, os, sys, urllib.request
from pathlib import Path

cfg = json.loads((Path(__file__).resolve().parent.parent / "config.json").read_text())
URL = (os.environ.get("SUPABASE_URL") or cfg.get("supabaseUrl") or "").rstrip("/")
KEY = os.environ.get("SUPABASE_ANON_KEY") or cfg.get("supabaseAnonKey") or ""
if not URL or not KEY:
    print("::notice::config.json에 Supabase 주소·키가 없어 건너뜁니다.")
    sys.exit(0)
h = {"apikey": KEY, "Content-Type": "application/json"}
if KEY.startswith("eyJ"):
    h["Authorization"] = "Bearer " + KEY
r = urllib.request.Request(URL + "/rest/v1/rpc/keepalive", data=b"{}", method="POST", headers=h)
with urllib.request.urlopen(r, timeout=30) as res:
    print("keepalive", res.status, res.read().decode())
