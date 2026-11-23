#!/usr/bin/env python3
"""content/ -> Supabase items 행 목록 (앱과 같은 ID 규칙: 문장 md5, 단어 'w'+djb2)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402


def djb2(s):
    """앱의 hash()와 동일: h=(h*33 ^ c)>>>0, 36진수"""
    h = 5381
    b = s.encode("utf-16-le")  # JS charCodeAt = UTF-16 코드 단위
    for i in range(0, len(b), 2):
        h = ((h * 33) ^ (b[i] | b[i + 1] << 8)) & 0xFFFFFFFF
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if h == 0:
        return "0"
    out = ""
    while h:
        h, r = divmod(h, 36)
        out = digits[r] + out
    return out


def rows():
    out = []
    for lang in ("vi", "en"):
        items, errs = build.parse(lang)
        if errs:
            raise SystemExit("\n".join(errs))
        words = {}
        for s in items:
            out.append({"lang": lang, "item_id": s["id"], "kind": "s", "lv": s["l"], "cat": s["c"], "ko": s["k"],
                        "target": s["t"], "gloss": "; ".join(f"{a}={b}" for a, b in s["w"]) or None,
                        "note": s["n"] or None, "source": s["f"]})
            for term, mean in s["w"]:
                key = term.lower()
                w = words.get(key)
                if not w:
                    w = words[key] = {"t": term, "means": [], "c": s["c"], "l": s["l"], "f": s["f"]}
                if mean not in w["means"]:
                    w["means"].append(mean)
                w["l"] = min(w["l"], s["l"])
        for key, w in words.items():
            m = [a for a in w["means"] if not any(b != a and a in b for b in w["means"])]
            out.append({"lang": lang, "item_id": "w" + djb2(lang + key), "kind": "w", "lv": w["l"], "cat": w["c"],
                        "ko": " · ".join(m[:4]), "target": w["t"], "gloss": None, "note": None, "source": w["f"]})
    return out


if __name__ == "__main__":
    r = rows()
    print(len(r), "rows;", sum(1 for x in r if x["kind"] == "w"), "words")
