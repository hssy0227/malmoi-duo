#!/usr/bin/env python3
"""말뭉치 교차검증 → reports/check.md

검사 항목
  1. 중복: 원어 완전 중복(빌드에서 차단) + 정규화 후 유사 중복(구두점·대소문자·축약형 무시)
  2. 한국어 뜻 중복: 같은 한국어 문장에 원어가 여러 개 (카드 '한국어→원어'에서 정답이 모호)
  3. 풀이 누락: 풀이 없는 문장, 문장에 나오지 않는 풀이 단어
  4. 표기: 베트남어 NFC 정규화, 베트남어 문자 외 글자, 앞뒤 공백·이중 공백
  5. 균형: 언어별 상황×레벨 분포, 한쪽 언어에만 있는 상황
  6. 커리큘럼 대비 누락 어휘
     영어: NGSL 1.01(일반 2,801) · TSL 1.1(토익 1,259) · BSL 1.01(비즈니스 1,754)
     베트남어: 자막 빈도 상위 3,000 음절 (FrequencyWords, OpenSubtitles 2018)
사용: python3 tools/check.py [--strict]   (--strict: 1·4 항목이 있으면 종료코드 1)
"""
import re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

REF = ROOT / "sources" / "ref"
VI_LETTERS = set("aăâbcdđeêghiklmnoôơpqrstuưvxy" "fjwz")  # 외래어 허용
VI_TONES = set("̣̀́̃̉")
IRREG = {
    "be": "am is are was were been being 's 're 'm", "have": "has had having 've 'd", "do": "does did done doing",
    "go": "goes went gone going", "get": "gets got gotten getting", "make": "makes made making",
    "say": "says said saying", "take": "takes took taken taking", "come": "comes came coming",
    "see": "sees saw seen seeing", "know": "knows knew known knowing", "give": "gives gave given giving",
    "think": "thinks thought thinking", "tell": "tells told telling", "find": "finds found finding",
    "feel": "feels felt feeling", "leave": "leaves left leaving", "keep": "keeps kept keeping",
    "bring": "brings brought bringing", "buy": "buys bought buying", "pay": "pays paid paying",
    "meet": "meets met meeting", "run": "runs ran running", "write": "writes wrote written writing",
    "sit": "sits sat sitting", "stand": "stands stood standing", "lose": "loses lost losing",
    "hold": "holds held holding", "hear": "hears heard hearing", "begin": "begins began begun beginning",
    "speak": "speaks spoke spoken speaking", "send": "sends sent sending", "build": "builds built building",
    "spend": "spends spent spending", "fall": "falls fell fallen falling", "lead": "leads led leading",
    "understand": "understands understood understanding", "teach": "teaches taught teaching",
    "catch": "catches caught catching", "choose": "chooses chose chosen choosing", "eat": "eats ate eaten eating",
    "drink": "drinks drank drunk drinking", "drive": "drives drove driven driving", "fly": "flies flew flown flying",
    "forget": "forgets forgot forgotten forgetting", "grow": "grows grew grown growing", "hide": "hides hid hidden",
    "lie": "lies lay lain lying lied", "ride": "rides rode ridden riding", "rise": "rises rose risen rising",
    "sell": "sells sold selling", "sing": "sings sang sung singing", "sleep": "sleeps slept sleeping",
    "steal": "steals stole stolen", "swim": "swims swam swum swimming", "throw": "throws threw thrown",
    "wake": "wakes woke woken waking", "wear": "wears wore worn wearing", "win": "wins won winning",
    "break": "breaks broke broken breaking", "draw": "draws drew drawn drawing", "feed": "feeds fed feeding",
    "fight": "fights fought fighting", "light": "lights lit lighting", "mean": "means meant meaning",
    "seek": "seeks sought seeking", "shoot": "shoots shot shooting", "shake": "shakes shook shaken",
    "strike": "strikes struck striking", "bear": "bears bore born borne", "bind": "binds bound binding",
    "dig": "digs dug digging", "hang": "hangs hung hanging", "lay": "lays laid laying", "lend": "lends lent lending",
    "bend": "bends bent bending", "freeze": "freezes froze frozen", "deal": "deals dealt dealing",
    "good": "better best", "bad": "worse worst", "well": "better best", "far": "further farther furthest",
    "child": "children", "person": "people", "man": "men", "woman": "women", "foot": "feet", "tooth": "teeth",
    "mouse": "mice", "life": "lives", "wife": "wives", "knife": "knives", "leaf": "leaves", "half": "halves",
    "i": "me my mine", "we": "us our ours", "he": "him his", "she": "her hers", "they": "them their theirs",
    "you": "your yours", "it": "its", "will": "'ll would", "not": "n't", "can": "could cannot", "may": "might",
    "shall": "should", "must": "must", "let": "let's", "us": "let's", "phenomenon": "phenomena",
    "criterion": "criteria", "datum": "data", "analysis": "analyses", "crisis": "crises",
}


def en_forms(lemma):
    w = lemma.lower()
    f = {w, w + "s", w + "es", w + "ed", w + "d", w + "ing", w + "er", w + "est", w + "ly", w + "'s"}
    if w.endswith("e"):
        f |= {w[:-1] + "ing", w[:-1] + "er", w[:-1] + "est"}
    if w.endswith("y") and len(w) > 2 and w[-2] not in "aeiou":
        f |= {w[:-1] + "ies", w[:-1] + "ied", w[:-1] + "ier", w[:-1] + "iest", w[:-1] + "ily"}
    if len(w) >= 3 and w[-1] not in "aeiouwxy" and w[-2] in "aeiou" and w[-3] not in "aeiou":
        f |= {w + w[-1] + "ed", w + w[-1] + "ing", w + w[-1] + "er"}
    if w.endswith("le"):
        f.add(w[:-1] + "y")
    if w.endswith("ic"):
        f |= {w + "al", w + "ally"}
    for x in IRREG.get(w, "").split():
        f.add(x)
    return f


def tokens_en(text):
    t = text.lower().replace("’", "'")
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", t)
    out = set()
    for x in words:
        out.add(x)
        if "'" in x:
            a, b = x.split("'", 1)
            out |= {a, "'" + b}
        for part in x.split("-"):
            out.add(part)
    return out


def norm_key(t, lang):
    t = unicodedata.normalize("NFC", t.lower()).replace("’", "'")
    if lang == "en":
        for a, b in (("n't", " not"), ("'re", " are"), ("'m", " am"), ("'ll", " will"), ("'ve", " have"), ("let's", "let us")):
            t = t.replace(a, b)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def vi_bad_chars(t):
    bad = set()
    t = re.sub(r"[\uac00-\ud7a3]", "", t)  # 한글 예시(한자어 비교 등)는 허용
    for ch in unicodedata.normalize("NFD", t.lower()):
        if ch.isalpha():
            if ch not in VI_LETTERS:
                bad.add(ch)
        elif unicodedata.category(ch) == "Mn" and ch not in VI_TONES and ch not in "̛̂̆":
            bad.add(repr(ch))
    return bad


def present(term, text, lang):
    term = unicodedata.normalize("NFC", term.lower())
    text = unicodedata.normalize("NFC", text.lower())
    if lang == "en":
        toks = tokens_en(text)
        wild = {"~", "sb", "sth", "a", "b", "the", "one's", "oneself", "someone", "somebody", "something", "-ing", "be", "a~", "b~"}
        parts = [p for p in re.split(r"[\s/]+", term.replace("…", " ").replace("...", " ")) if p and p.lower() not in wild]
        if not parts:
            return True
        return all(any(f in toks for f in en_forms(p.strip("()'"))) or p in text for p in parts)
    parts = [p for p in re.split(r"[\s/…]+", term.replace("...", " ").replace("~", " ")) if p and p not in ("A", "B", "a", "b")]
    return all(p in text for p in parts)


def main():
    strict = "--strict" in sys.argv
    out, hard = [], 0
    data = {}
    for lang in ("vi", "en"):
        items, errs = build.parse(lang)
        if errs:
            out.append(f"### [{lang}] 빌드 오류\n" + "\n".join("- " + e for e in errs))
            hard += len(errs)
        data[lang] = items
    cat_name = dict(build.CATS)
    lv_name = {l: f"Lv{l}·{c}" for l, c, _ in build.LEVELS}

    out.insert(0, "# 말뭉치 교차검증 리포트\n\n`python3 tools/check.py`로 생성. 빌드 오류·완전 중복은 빌드 단계에서 차단됩니다.\n")
    # 요약
    out.append("## 1. 요약\n\n| 항목 | 베트남어 | 영어 |\n|---|---:|---:|")
    summ = {}
    for lang, items in data.items():
        terms = {w[0].lower() for i in items for w in i["w"]}
        summ[lang] = (len(items), len(terms))
    out.append(f"| 문장 | {summ['vi'][0]:,} | {summ['en'][0]:,} |")
    out.append(f"| 풀이 단어(고유) | {summ['vi'][1]:,} | {summ['en'][1]:,} |")
    for l, c, nm in build.LEVELS:
        a = sum(1 for i in data["vi"] if i["l"] == l)
        b = sum(1 for i in data["en"] if i["l"] == l)
        out.append(f"| Lv{l} · CEFR {c} ({nm}) | {a:,} | {b:,} |")

    # 중복
    out.append("\n## 2. 중복\n")
    for lang, items in data.items():
        nk = defaultdict(list)
        for i in items:
            nk[norm_key(i["t"], lang)].append(i)
        near = [v for v in nk.values() if len(v) > 1]
        hard += len(near)
        out.append(f"**[{lang}] 정규화 후 같은 문장: {len(near)}건**" + ("" if near else " — 없음"))
        for v in near[:50]:
            out.append("- " + " ↔ ".join(f"`{x['t']}` ({x['f']})" for x in v))
        kk = defaultdict(list)
        for i in items:
            kk[re.sub(r"[\s.?!,]", "", i["k"])].append(i)
        amb = [v for v in kk.values() if len(v) > 1]
        out.append(f"\n[{lang}] 같은 한국어 뜻에 원어가 여러 개: {len(amb)}건 (카드에서 정답이 모호할 수 있음)")
        for v in amb[:40]:
            out.append(f"- {v[0]['k']} → " + " / ".join(f"`{x['t']}`" for x in v))
        out.append("")

    # 풀이·표기
    out.append("## 3. 풀이·표기\n")
    for lang, items in data.items():
        nog = [i for i in items if not i["w"]]
        miss = [(i, w[0]) for i in items for w in i["w"] if not present(w[0], i["t"], lang)]
        out.append(f"**[{lang}] 풀이 없는 문장 {len(nog)}건 · 문장에 없는 풀이어 {len(miss)}건**")
        for i in nog[:20]:
            out.append(f"- 풀이 없음: `{i['t']}` ({i['f']})")
        byf = Counter(i["f"] for i, _ in miss)
        if miss:
            out.append("- 문장에 없는 풀이어 파일별: " + ", ".join(f"{f} {n}" for f, n in byf.most_common()))
            for i, w in [m for m in miss if m[0]["f"] != "en_x_biz.txt"][:40]:
                out.append(f"  - `{w}` ← {i['t']} ({i['f']})")
        sp = [i for i in items if "  " in i["t"] or i["t"] != i["t"].strip()]
        hard += len(sp)
        if sp:
            out.append(f"- 공백 문제 {len(sp)}건: " + ", ".join(f"`{i['t']}`" for i in sp[:10]))
        if lang == "vi":
            raw_nfd = 0
            for f in sorted((build.ROOT / "content").glob("vi_*.txt")):
                txt = f.read_text(encoding="utf-8")
                if unicodedata.normalize("NFC", txt) != txt:
                    raw_nfd += 1
                    out.append(f"- NFC 아님(조합형 섞임): {f.name}")
            hard += raw_nfd
            bad = [(i, vi_bad_chars(i["t"])) for i in items]
            bad = [(i, b) for i, b in bad if b]
            hard += len(bad)
            out.append(f"- 베트남어 문자 외 글자: {len(bad)}건" + ("" if bad else " — 없음"))
            for i, b in bad[:20]:
                out.append(f"  - {sorted(b)} ← `{i['t']}`")
        out.append("")

    # 균형
    out.append("## 4. 상황별 분포 (언어 간 균형)\n\n| 상황 | 베트남어 | 영어 | 메모 |\n|---|---:|---:|---|")
    cv, ce = Counter(i["c"] for i in data["vi"]), Counter(i["c"] for i in data["en"])
    for k, nm in build.CATS:
        a, b = cv.get(k, 0), ce.get(k, 0)
        memo = ""
        if a and not b:
            memo = "영어 없음"
        elif b and not a:
            memo = "베트남어 없음" + (" (영어 전용 분야)" if k in ("econ",) else "")
        elif min(a, b) < 30:
            memo = "30개 미만"
        out.append(f"| {nm} | {a} | {b} | {memo} |")

    # 커리큘럼 대비 누락
    out.append("\n## 5. 기준 어휘 목록 대비 누락\n")
    en_tok = set()
    for i in data["en"]:
        en_tok |= tokens_en(i["t"])
    for fn, label in (("en_ngsl_1.01.txt", "NGSL 1.01 (일반 영어 핵심 2,801)"), ("en_tsl_1.1.txt", "TSL 1.1 (토익)"), ("en_bsl_1.01.txt", "BSL 1.01 (비즈니스)")):
        lst = [w.strip() for w in (REF / fn).read_text().splitlines() if w.strip()]
        miss = [w for w in lst if not (en_forms(w) & en_tok)]
        cov = 1 - len(miss) / len(lst)
        out.append(f"**{label}: 포함 {cov:.1%} · 누락 {len(miss):,}개**")
        bands = [(0, 500), (500, 1000), (1000, 2000), (2000, 9999)]
        for a, b in bands:
            seg = [w for w in miss if a <= lst.index(w) < b]
            if seg:
                out.append(f"- 순위 {a+1}~{min(b, len(lst))}: {len(seg)}개 — " + ", ".join(seg[:80]) + (" …" if len(seg) > 80 else ""))
        out.append("")
    vi_text = " ".join(i["t"].lower() for i in data["vi"])
    vi_syl = set(re.findall(r"[\wđ]+", unicodedata.normalize("NFC", vi_text)))
    lst = []
    for w in (REF / "vi_subtitle_freq_top5000.txt").read_text(encoding="utf-8").splitlines():
        w = unicodedata.normalize("NFC", w.strip().lower())
        if w and w not in lst:
            lst.append(w)
    lst = lst[:3000]
    miss = [w for w in lst if w not in vi_syl and not re.search(r"[0-9]", w)]
    out.append(f"**베트남어 자막 빈도 상위 3,000 음절: 포함 {1-len(miss)/len(lst):.1%} · 누락 {len(miss):,}개**")
    for a, b in ((0, 500), (500, 1000), (1000, 2000), (2000, 3000)):
        seg = [w for w in miss if a <= lst.index(w) < b]
        if seg:
            out.append(f"- 순위 {a+1}~{b}: {len(seg)}개 — " + ", ".join(seg[:100]) + (" …" if len(seg) > 100 else ""))
    out.append("\n(자막 음절에는 인명·외래어 표기가 섞여 있어 전부가 학습 대상은 아님)\n")
    out.append("## 출처\n- NGSL·TSL·BSL: Browne, C., Culligan, B. & Phillips, J., newgeneralservicelist.com — CC BY-SA 4.0\n- 베트남어 빈도: hermitdave/FrequencyWords (OpenSubtitles 2018) — 내용 CC BY-SA 4.0\n")

    rep = ROOT / "reports" / "check.md"
    rep.parent.mkdir(exist_ok=True)
    rep.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"reports/check.md 작성 · 심각 항목 {hard}건")
    if strict and hard:
        sys.exit(1)


if __name__ == "__main__":
    main()
