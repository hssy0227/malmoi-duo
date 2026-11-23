#!/usr/bin/env python3
"""sources/biz_vocab_en.txt(영문 600) + biz_ko_*.txt(한국어 해석) -> content/en_x_biz.txt"""
from pathlib import Path
D = Path(__file__).parent
# 레벨: 4=B2, 5=C1 (전문 분야 용어)
MAP = {"Management": ("mgmt", 4), "Strategy": ("mgmt", 4), "Organization": ("org", 4),
       "Economics": ("econ", 5), "Finance": ("fin", 5), "Trading": ("fin", 5),
       "Technology": ("tech", 5), "AI": ("ai", 5), "Analytics": ("ai", 5),
       "Energy": ("energy", 5), "Commodity": ("energy", 5), "Advanced": ("toeic", 4)}
ko = {}
for f in sorted(D.glob("src_biz_ko_*.txt")) + sorted(D.glob("biz_ko_*.txt")):
    for ln in f.read_text(encoding="utf-8").splitlines():
        if ln and not ln.startswith("#"):
            i, w, s = ln.split("|")
            ko[i] = (w.strip(), s.strip())
groups = {}
for ln in (D / "biz_vocab_en.txt").read_text(encoding="utf-8").splitlines():
    p = [x.strip() for x in ln.split("|")]
    if len(p) != 4 or not p[0].isdigit():
        continue
    i, cat, word, sent = p
    c, lv = MAP[cat]
    w, s = ko[i]
    groups.setdefault(c, []).append(f"{lv}|{s}|{sent}|{word}={w}")
out = ["# 첨부 비즈니스·고급 영어 600 (sources/gen_biz.py로 생성 — 직접 수정 금지)"]
for c, rows in groups.items():
    out += ["", "@" + c] + rows
(D.parent / "content" / "en_x_biz.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print(sum(len(v) for v in groups.values()), {k: len(v) for k, v in groups.items()})
