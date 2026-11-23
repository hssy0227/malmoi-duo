#!/usr/bin/env python3
"""sources/core_parallel_*.txt (한국어 뜻 공유) -> content/vi_y_core.txt, content/en_y_core.txt
형식: 레벨|한국어|베트남어|베트남어 풀이|영어|영어 풀이  (@상황 줄로 구분)"""
from pathlib import Path
D = Path(__file__).parent
import unicodedata
out = {"vi": [], "en": []}
n = 0
# 이미 다른 파일에 같은 원어 문장이 있으면 그쪽을 쓰고 여기서는 건너뜀 (짝은 유지)
have = {L: set() for L in out}
for L in out:
    for f in (D.parent / "content").glob(f"{L}_*.txt"):
        if f.name.endswith("_y_core.txt"):
            continue
        for ln in f.read_text(encoding="utf-8").splitlines():
            q = ln.split("|")
            if len(q) >= 3 and q[0].strip().isdigit():
                have[L].add(unicodedata.normalize("NFC", q[2].strip()).lower())
skipped = {"vi": 0, "en": 0}
for f in sorted(D.glob("core_parallel_*.txt")):
    for i, raw in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            out["vi"].append(line); out["en"].append(line); continue
        p = line.split("|")
        if len(p) != 6:
            raise SystemExit(f"{f.name}:{i} 필드 6개 필요: {line}")
        lv, ko, vi, vg, en, eg = [x.strip() for x in p]
        for L, t, g in (("vi", vi, vg), ("en", en, eg)):
            if unicodedata.normalize("NFC", t).lower() in have[L]:
                skipped[L] += 1
            else:
                out[L].append(f"{lv}|{ko}|{t}|{g}")
        n += 1
for L in out:
    (D.parent / "content" / f"{L}_y_core.txt").write_text(
        "# 두 언어 공통 핵심 문장 (sources/gen_core.py로 생성 — 직접 수정 금지)\n" + "\n".join(out[L]) + "\n", encoding="utf-8")
print("core pairs", n, "already present elsewhere", skipped)
