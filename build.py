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
    ("work", "업무·경영"), ("econ", "경제·금융·에너지"), ("society", "사회·정치·외교"), ("tech", "IT·AI"),
    ("saying", "명언·속담"),
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
    ("TE", "토익", "토익 Part 1~7에 자주 나오는 사진·업무·생활 장면과 토익 단어 목록 TSL(CC BY-SA)의 누락 어휘로 직접 작성한 문장, 첨부 DB의 '토익·토플 고급 어휘' 50개, 첨부 어휘 목록의 토익·비즈니스 단어예요."),
    ("TF", "토플", "토플 강의 주제(생물·지구과학·역사·문학 등)와 스피킹 의견·경험 답변 형식으로 직접 작성한 문장, 첨부 어휘 목록의 토플·아카데믹 단어예요."),
    ("Biz", "비즈니스", "첨부해 주신 비즈니스 영어 DB(경영·조직·경제·금융·IT·AI·에너지)예요. 영문 예문은 그대로 두고 한국어 해석과 단어 뜻을 붙였어요."),
    ("Mv", "영화 구어", "베트남어 자막 빈도 목록(OpenSubtitles, CC BY-SA)에서 빠져 있던 구어·반말·사극 표현을 영화 대사 형식으로 직접 작성한 문장이에요."),
    ("Jr", "저널·뉴스", "경제·사회·정치·외교·IT·커머스 분야의 최근 1~2년 주요 이슈를 바탕으로, 저널 헤드라인과 기사 핵심 문장 형식으로 직접 새로 작성한 문장이에요. 실제 기사 문장을 옮기지 않았어요. 첨부 어휘 목록의 시사·뉴스 단어도 이 출처예요."),
    ("Mt", "비즈니스 미팅", "회의 시작·안건·의견 조율·협상·후속 조치 등 실제 미팅 흐름에 맞춰 직접 작성한 문장이에요."),
    ("Pv", "속담·명언", "두 언어의 전래 속담·관용구·민요(ca dao)와, 출처가 분명한 고전 인물·옛 공문서(1929년 이전)의 짧은 명언이에요. 한국어 칸에는 비슷한 우리 속담이나 뜻을, 메모에는 직역과 유래를 적었어요."),
    ("Adv", "고급", "베트남어 능력 기준 5등급(CEFR C1) 수준의 시사·속담·격식체·추상 토론 주제로 직접 작성한 문장이에요."),
]
SRC_FILE = {"en_e.txt": "TE", "en_f.txt": "TE", "en_i.txt": "TE", "en_l.txt": "TE", "en_g.txt": "TF",
            "en_j.txt": "NG", "en_k.txt": "NG",
            "en_wd_toefl.txt": "TF", "en_wd_toeic.txt": "TE", "en_wd_news.txt": "Jr", "en_wx_toefl.txt": "TF", "en_wx_toeic.txt": "TE", "en_wx_news.txt": "Jr", "en_wm_toefl.txt": "TF", "en_wm_toeic.txt": "TE", "en_wm_news.txt": "Jr", "vi_p.txt": "Mv", "vi_q.txt": "Adv"}


def src_of(fname, cat):
    if fname[3:6] == "jr_":
        return "Jr"
    if fname[3:6] == "mt_":
        return "Mt"
    if fname[3:6] == "pv_":
        return "Pv"
    if fname == "en_x_biz.txt":
        return "TE" if cat == "toeic" else "Biz"
    if fname == "en_h.txt":
        return "TF" if cat in ("opinion", "life") else "TE"
    return SRC_FILE.get(fname, "G")


def hid(s):
    return hashlib.md5(s.encode()).hexdigest()[:8]


WORDX = {}  # 단어·숙어로 직접 등록한 항목(레벨 앞에 w) — 문장 목록에는 넣지 않음


def parse(lang):
    items, errors, seen = [], [], {}
    wx = WORDX[lang] = []
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
            lv, ko, t = parts[0].strip(), parts[1].strip(), unicodedata.normalize("NFC", parts[2].strip())
            is_word = lv.startswith("w")
            if is_word:
                lv = lv[1:]
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
            if is_word:
                term = re.sub(r"[.!?…]+$", "", t).strip()
                wx.append({"t": term, "k": re.sub(r"[.!?…]+$", "", ko).strip(), "c": CAT_MAP.get(cat, cat), "l": int(lv),
                           "w": words, "n": note, "s": src_of(f.name, cat), "o": hid(lang + ":" + t), "f": f.name})
                continue
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
    data = {"cats": CATS, "catMap": CAT_MAP, "levels": LEVELS, "srcs": SOURCES, "langs": {}, "sb": {"url": sb_url, "key": sb_key, "vapid": cfg.get("vapidPublicKey", "")}}
    all_err = []
    for lang in ("vi", "en"):
        items, errs = parse(lang)
        all_err += [f"[{lang}] {e}" for e in errs]
        data["langs"][lang] = [{k: v for k, v in i.items() if k not in ("f", "oc")} for i in items]
        data.setdefault("wx", {})[lang] = [{k: v for k, v in w.items() if k != "f"} for w in WORDX[lang]]
        (ROOT / "dist").mkdir(exist_ok=True)
        PARSED[lang] = items
        per, lvs = {}, {}
        for i in items:
            lvs[i["l"]] = lvs.get(i["l"], 0) + 1
            per[i["c"]] = per.get(i["c"], 0) + 1
        terms = {w[0].lower() for i in items for w in i["w"]}
        terms |= {w["t"].lower() for w in WORDX[lang]}
        print(f"{lang}: {len(items)} sentences, {len(terms)} unique terms ({len(WORDX[lang])} 직접 등록), levels {dict(sorted(lvs.items()))}")
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
