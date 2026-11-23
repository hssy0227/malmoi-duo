#!/usr/bin/env python3
"""content/의 문장·단어를 Supabase items 테이블로 올림 (GitHub Actions에서 실행)
환경변수: SUPABASE_URL (없으면 config.json), SUPABASE_SERVICE_KEY (secret 키 또는 service_role 키)"""
import datetime, json, os, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
import build, items  # noqa: E402

cfg = json.loads((ROOT / "config.json").read_text())
URL = (os.environ.get("SUPABASE_URL") or cfg.get("supabaseUrl") or "").rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
if not URL or not KEY:
    print("::notice::SUPABASE_URL 또는 SUPABASE_SERVICE_KEY가 없어 items 동기화를 건너뜁니다.")
    sys.exit(0)


def req(method, path, body=None, prefer="return=minimal"):
    h = {"apikey": KEY, "Content-Type": "application/json", "Prefer": prefer}
    if KEY.startswith("eyJ"):
        h["Authorization"] = "Bearer " + KEY
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    r = urllib.request.Request(URL + "/rest/v1/" + path, data=data, method=method, headers=h)
    with urllib.request.urlopen(r, timeout=60) as res:
        return res.status


now = datetime.datetime.now(datetime.timezone.utc).isoformat()
merge = "resolution=merge-duplicates,return=minimal"
req("POST", "levels?on_conflict=lv", [{"lv": l, "cefr": c, "name_ko": n} for l, c, n in build.LEVELS], merge)
req("POST", "categories?on_conflict=key", [{"key": k, "name_ko": n, "sort": i} for i, (k, n) in enumerate(build.CATS)], merge)
req("POST", "sources?on_conflict=key", [{"key": k, "name_ko": n, "how": h, "sort": i} for i, (k, n, h) in enumerate(build.SOURCES)], merge)
rs = items.rows()
for r in rs:
    r["active"] = True
    r["synced_at"] = now
for i in range(0, len(rs), 800):
    req("POST", "items?on_conflict=lang,item_id", rs[i:i + 800], merge)
req("PATCH", "items?synced_at=lt." + urllib.parse.quote(now), {"active": False})
print(f"items 동기화 완료: {len(rs)}행")
