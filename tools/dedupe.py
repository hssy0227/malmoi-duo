#!/usr/bin/env python3
"""지정한 content 파일에서, 다른 파일(또는 같은 파일 앞부분)에 이미 있는 원어 문장 줄을 삭제
사용: python3 tools/dedupe.py content/en_n_b.txt ..."""
import re, sys, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
targets = [Path(a).resolve() for a in sys.argv[1:]]
norm = lambda t: re.sub(r"\s+", " ", unicodedata.normalize("NFC", t).strip().lower())
for tf in targets:
    lang = tf.name[:2]
    have = set()
    for f in sorted((ROOT / "content").glob(f"{lang}_*.txt")):
        if f.resolve() == tf:
            continue
        for ln in f.read_text(encoding="utf-8").splitlines():
            p = ln.split("|")
            if len(p) >= 3 and p[0].strip().lstrip("w").isdigit():
                have.add(norm(p[2]))
    out, drop = [], 0
    for ln in tf.read_text(encoding="utf-8").splitlines():
        p = ln.split("|")
        if len(p) >= 3 and p[0].strip().lstrip("w").isdigit():
            k = norm(p[2])
            if k in have:
                drop += 1
                continue
            have.add(k)
        out.append(ln)
    tf.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(tf.name, "dropped", drop)
