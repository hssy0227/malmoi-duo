#!/usr/bin/env python3
"""Parse content/*.txt -> data, inline into src/app.html -> dist/index.html (+ PWA files)."""
import hashlib, json, re, shutil, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
# 상황 15개 (2026-11 통폐합). content 파일의 옛 @키는 CAT_MAP으로 묶음
CATS = [
    ("greet", "인사·스몰토크"), ("daily", "일상·가족"), ("home", "집·날씨"), ("food", "음식·요리"),
    ("shop", "쇼핑·돈"), ("travel", "여행·교통"), ("time", "시간·약속"), ("health", "건강·문제해결"),
    ("hobby", "취미·문화"), ("movie", "영화·책"), ("opinion", "의견·경험"), ("study", "배움·시험"),
    ("work", "업무·경영"), ("econ", "경제·금융·에너지"), ("tech", "IT·AI"),
]
CAT_MAP = {
    "social": "greet", "family": "daily", "nature": "home", "cook": "food", "money": "shop",
    "move": "travel", "stay": "travel", "phone": "time", "trouble": "health", "culture": "hobby",
    "book": "movie", "life": "opinion", "toeic": "study", "acad": "study",
    "biz": "work", "mgmt": "work", "org": "work", "fin": "econ", "energy": "econ", "ai": "tech",
}
CAT_KEYS = {k for k, _ in CATS} | set(CAT_MAP)
# 두 언어 공통 5단계 — CEFR 매핑 (Supabase levels 테이블과 동일)
LEVELS = [(1, "A1", "기초"), (2, "A2", "초급"), (3, "B1", "중급"), (4, "B2", "중상급"), (5, "C1", "고급")]
LV_KEYS = {str(l) for l, _, _ in LEVELS}
# 출처(어떻게 가져왔는지) — 사전 범례·필터, Supabase sources 테이블과 동일
SOURCES = [
    ("G", "일반", "일상 회화 기본 세트, 여행·영화·책 회화, 두 언어 공통 핵심 문장(CEFR A1~B1 주제). 특정 시험이나 단어 목록이 아니라 일반 회화 상황을 기준으로 직접 작성했어요."),
    ("NG", "핵심어휘", "영어 핵심 단어 목록 NGSL(2,801개, CC BY-SA)과 비교해 빠져 있던 고빈도 단어를 넣어 직접 작성한 문장이에요."),
    ("TE", "토익", "토익 Part 1~7에 자주 나오는 사진·업무·생활 장면과 토익 단어 목록 TSL(CC BY-SA)의 누락 어휘로 직접 작성한 문장, 그리고 첨부 DB의 '토익·토플 고급 어휘' 50개예요."),
    ("TF", "토플", "토플 강의 주제(생물·지구과학·역사·문학 등)와 스피킹 의견·경험 답변 형식으로 직접 작성한 문장이에요."),
    ("Biz", "비즈니스", "첨부해 주신 비즈니스 영어 DB(경영·조직·경제·금융·IT·AI·에너지)예요. 영문 예문은 그대로 두고 한국어 해석과 단어 뜻을 붙였어요."),
    ("Mv", "영화 구어", "베트남어 자막 빈도 목록(OpenSubtitles, CC BY-SA)에서 빠져 있던 구어·반말·사극 표현을 영화 대사 형식으로 직접 작성한 문장이에요."),
    ("Adv", "고급", "베트남어 능력 기준 5등급(CEFR C1) 수준의 시사·속담·격식체·추상 토론 주제로 직접 작성한 문장이에요."),
]
SRC_FILE = {"en_e.txt": "TE", "en_f.txt": "TE", "en_i.txt": "TE", "en_l.txt": "TE", "en_g.txt": "TF",
            "en_j.txt": "NG", "en_k.txt": "NG", "vi_p.txt": "Mv", "vi_q.txt": "Adv"}


def src_of(fname, cat):
    if fname == "en_x_biz.txt":
        return "TE" if cat == "toeic" else "Biz"
    if fname == "en_h.txt":
        return "TF" if cat in ("opinion", "life") else "TE"
    return SRC_FILE.get(fname, "G")


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
            if lv not in LV_KEYS or not ko or not t:
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
            items.append({"id": hid(lang + ":" + t), "c": CAT_MAP.get(cat, cat), "l": int(lv), "k": ko, "t": t, "w": words, "n": note, "f": f.name, "s": src_of(f.name, cat), "oc": cat})
    ids = [i["id"] for i in items]
    if len(ids) != len(set(ids)):
        errors.append("id collision")
    return items, errors


PARSED = {}


def main():
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8")) if (ROOT / "config.json").exists() else {}
    import os
    sb_url = os.environ.get("MALMOI_SB_URL", cfg.get("supabaseUrl", ""))  # 테스트용 덮어쓰기
    sb_key = os.environ.get("MALMOI_SB_KEY", cfg.get("supabaseAnonKey", ""))
    data = {"cats": CATS, "catMap": CAT_MAP, "levels": LEVELS, "srcs": SOURCES, "langs": {}, "sb": {"url": sb_url, "key": sb_key}}
    all_err = []
    for lang in ("vi", "en"):
        items, errs = parse(lang)
        all_err += [f"[{lang}] {e}" for e in errs]
        data["langs"][lang] = [{k: v for k, v in i.items() if k not in ("f", "oc")} for i in items]
        (ROOT / "dist").mkdir(exist_ok=True)
        PARSED[lang] = items
        per, lvs = {}, {}
        for i in items:
            lvs[i["l"]] = lvs.get(i["l"], 0) + 1
            per[i["c"]] = per.get(i["c"], 0) + 1
        terms = {w[0].lower() for i in items for w in i["w"]}
        print(f"{lang}: {len(items)} sentences, {len(terms)} unique terms, levels {dict(sorted(lvs.items()))}")
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
