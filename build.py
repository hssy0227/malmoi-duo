#!/usr/bin/env python3
"""Parse content/*.txt -> data, inline into src/app.html -> dist/index.html (+ PWA files)."""
import hashlib, json, re, shutil, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
CATS = [
    ("greet", "인사·소개"), ("daily", "일상·감정"), ("food", "식당·카페"), ("shop", "쇼핑·결제"),
    ("move", "교통·길찾기"), ("stay", "숙소·호텔"), ("time", "시간·숫자"), ("phone", "약속·전화"),
    ("work", "업무·회의"), ("social", "스몰토크"), ("health", "건강·응급"), ("travel", "관광·여가"),
    ("trouble", "부탁·문제해결"), ("opinion", "의견·토론"), ("life", "경험 이야기"),
    ("cook", "요리·레시피"), ("hobby", "취미·운동"), ("biz", "비즈니스·협상"), ("home", "집·생활"),
    ("money", "돈·금융"), ("tech", "IT·디지털"), ("nature", "날씨·자연"), ("culture", "문화·명절"),
    ("family", "가족·관계"), ("study", "배움·언어"),
    ("movie", "영화·드라마"), ("book", "책·독서"), ("toeic", "토익·토플"), ("acad", "학술·교양"),
    ("mgmt", "경영·전략"), ("org", "조직·인사"), ("econ", "경제·거시"), ("fin", "금융·투자"),
    ("ai", "AI·데이터"), ("energy", "에너지·원자재"),
]
CAT_KEYS = {k for k, _ in CATS}


def hid(s):
    return hashlib.md5(s.encode()).hexdigest()[:8]


def parse(lang):
    items, errors, seen = [], [], {}
    for f in sorted((ROOT / "content").glob(f"{lang}_*.txt")):
        cat = None
        for n, raw in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("@"):
                cat = line[1:].strip()
                if cat not in CAT_KEYS:
                    errors.append(f"{f.name}:{n} unknown cat {cat}")
                continue
            parts = line.split("|")
            if len(parts) < 3 or len(parts) > 5:
                errors.append(f"{f.name}:{n} bad field count: {line}")
                continue
            lv, ko, t = parts[0], parts[1].strip(), unicodedata.normalize("NFC", parts[2].strip())
            gl = parts[3].strip() if len(parts) > 3 else ""
            note = parts[4].strip() if len(parts) > 4 else ""
            if lv not in ("1","2","3","4") or not ko or not t:
                errors.append(f"{f.name}:{n} bad level/empty: {line}")
                continue
            words = []
            for g in [x.strip() for x in gl.split(";") if x.strip()]:
                if "=" not in g:
                    errors.append(f"{f.name}:{n} bad gloss '{g}'")
                    continue
                a, b = g.split("=", 1)
                words.append([unicodedata.normalize("NFC", a.strip()), b.strip()])
            key = t.lower()
            if key in seen:
                errors.append(f"{f.name}:{n} duplicate of {seen[key]}: {t}")
                continue
            seen[key] = f"{f.name}:{n}"
            items.append({"id": hid(lang + ":" + t), "c": cat, "l": int(lv), "k": ko, "t": t, "w": words, "n": note})
    ids = [i["id"] for i in items]
    if len(ids) != len(set(ids)):
        errors.append("id collision")
    return items, errors


def main():
    data = {"cats": CATS, "langs": {}}
    all_err = []
    for lang in ("vi", "en"):
        items, errs = parse(lang)
        all_err += [f"[{lang}] {e}" for e in errs]
        data["langs"][lang] = items
        per = {}
        for i in items:
            per[i["c"]] = per.get(i["c"], 0) + 1
        terms = {w[0].lower() for i in items for w in i["w"]}
        print(f"{lang}: {len(items)} sentences, {len(terms)} unique terms, per-cat {per}")
    if all_err:
        print("\n".join(all_err))
        sys.exit(1)
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    html = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
    ver = hid(blob + html)
    html = html.replace("/*__DATA__*/null", blob).replace("__VER__", ver)
    (dist / "index.html").write_text(html, encoding="utf-8")
    sw = (ROOT / "src" / "sw.js").read_text(encoding="utf-8").replace("__VER__", ver)
    (dist / "sw.js").write_text(sw, encoding="utf-8")
    shutil.copy(ROOT / "src" / "manifest.json", dist / "manifest.json")
    shutil.copytree(ROOT / "src" / "icons", dist / "icons", dirs_exist_ok=True)
    print("built", ver, f"{len(html)/1024:.0f} KB")


if __name__ == "__main__":
    main()
