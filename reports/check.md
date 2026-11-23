# 말뭉치 교차검증 리포트

`python3 tools/check.py`로 생성. 빌드 오류·완전 중복은 빌드 단계에서 차단됩니다.

## 1. 요약

| 항목 | 베트남어 | 영어 |
|---|---:|---:|
| 문장 | 2,723 | 2,569 |
| 풀이 단어(고유) | 3,388 | 2,969 |
| Lv1 · CEFR A1 (기초) | 161 | 111 |
| Lv2 · CEFR A2 (초급) | 309 | 275 |
| Lv3 · CEFR B1 (중급) | 1,226 | 835 |
| Lv4 · CEFR B2 (중상급) | 983 | 849 |
| Lv5 · CEFR C1 (고급) | 44 | 499 |

## 2. 중복

**[vi] 정규화 후 같은 문장: 0건** — 없음

[vi] 같은 한국어 뜻에 원어가 여러 개: 0건 (카드에서 정답이 모호할 수 있음)

**[en] 정규화 후 같은 문장: 0건** — 없음

[en] 같은 한국어 뜻에 원어가 여러 개: 0건 (카드에서 정답이 모호할 수 있음)

## 3. 풀이·표기

**[vi] 풀이 없는 문장 0건 · 문장에 없는 풀이어 0건**
- 베트남어 문자 외 글자: 0건 — 없음

**[en] 풀이 없는 문장 0건 · 문장에 없는 풀이어 19건**
- 문장에 없는 풀이어 파일별: en_x_biz.txt 10, en_a.txt 3, en_l.txt 2, en_c.txt 1, en_d.txt 1, en_e.txt 1, en_g.txt 1
  - `not a bit` ← You haven't changed a bit. (en_a.txt)
  - `had better` ← I'd better get going. (en_a.txt)
  - `oversleep` ← I overslept. (en_a.txt)
  - `not sleep a wink` ← The room next door was loud all night. I didn't sleep a wink. (en_c.txt)
  - `play it by ear` ← I'm going to play this trip by ear. (en_d.txt)
  - `stick to` ← He stuck to his plan despite the criticism. (en_e.txt)
  - `die out` ← The language is in danger of dying out as speakers decline. (en_g.txt)
  - `replacement` ← We'll replace the faulty part. (en_l.txt)
  - `inspection` ← The factory machinery was inspected regularly. (en_l.txt)

## 4. 상황별 분포 (언어 간 균형)

| 상황 | 베트남어 | 영어 | 메모 |
|---|---:|---:|---|
| 인사·소개 | 86 | 55 |  |
| 일상·감정 | 96 | 103 |  |
| 식당·카페 | 83 | 58 |  |
| 쇼핑·결제 | 91 | 70 |  |
| 교통·길찾기 | 89 | 70 |  |
| 숙소·호텔 | 93 | 53 |  |
| 시간·숫자 | 89 | 54 |  |
| 약속·전화 | 90 | 61 |  |
| 업무·회의 | 93 | 109 |  |
| 스몰토크 | 102 | 83 |  |
| 건강·응급 | 101 | 84 |  |
| 관광·여가 | 182 | 65 |  |
| 부탁·문제해결 | 86 | 78 |  |
| 의견·토론 | 87 | 121 |  |
| 경험 이야기 | 83 | 62 |  |
| 요리·레시피 | 107 | 33 |  |
| 취미·운동 | 103 | 30 |  |
| 비즈니스·협상 | 92 | 30 |  |
| 집·생활 | 91 | 30 |  |
| 돈·금융 | 94 | 30 |  |
| IT·디지털 | 83 | 55 |  |
| 날씨·자연 | 109 | 34 |  |
| 문화·명절 | 106 | 47 |  |
| 가족·관계 | 119 | 34 |  |
| 배움·언어 | 92 | 54 |  |
| 영화·드라마 | 173 | 31 |  |
| 책·독서 | 103 | 33 |  |
| 토익·토플 | 0 | 383 | 베트남어 없음 (영어 전용 분야) |
| 학술·교양 | 0 | 119 | 베트남어 없음 (영어 전용 분야) |
| 경영·전략 | 0 | 100 | 베트남어 없음 (영어 전용 분야) |
| 조직·인사 | 0 | 50 | 베트남어 없음 (영어 전용 분야) |
| 경제·거시 | 0 | 50 | 베트남어 없음 (영어 전용 분야) |
| 금융·투자 | 0 | 100 | 베트남어 없음 (영어 전용 분야) |
| AI·데이터 | 0 | 100 | 베트남어 없음 (영어 전용 분야) |
| 에너지·원자재 | 0 | 100 | 베트남어 없음 (영어 전용 분야) |

## 5. 기준 어휘 목록 대비 누락

**NGSL 1.01 (일반 영어 핵심 2,801): 포함 74.4% · 누락 718개**
- 순위 1~500: 6개 — such, state, political, body, bear, himself
- 순위 501~1000: 26개 — act, kill, lie, fight, poor, attack, private, inside, press, drug, race, military, television, relation, bar, except, associate, male, dead, possibility, female, nor, agency, yeah, pound, judge
- 순위 1001~2000: 188개 — rich, wind, content, aware, administration, remove, chair, sex, inform, appeal, speed, slightly, apart, federal, institution, horse, feed, surface, lift, extent, presence, defense, ball, refuse, reform, plus, apparently, union, desire, aid, length, commit, weapon, code, possibly, threat, cancer, convince, blow, tape, murder, hate, camera, cycle, dear, onto, belong, fashion, bomb, council, sight, anybody, basically, violence, minister, mainly, manner, gun, civil, troop, arrangement, tear, shake, proper, afford, frame, tie, threaten, recommendation, resident, abuse, principal, master, session, appearance, odd, elect, association, soft, row …
- 순위 2001~2801: 498개 — prize, typically, pension, wing, assistance, roof, respectively, variation, smart, tooth, representation, preparation, emphasis, edition, silver, entertainment, undertake, retail, wire, unlikely, gay, publication, slight, unknown, inch, equivalent, solid, elderly, owe, governor, port, pitch, arrival, contemporary, gate, beer, specialist, assure, numerous, virtually, coverage, cable, sensitive, isolate, prisoner, wet, secondary, welfare, recruit, exclude, string, persuade, inspire, hence, crew, pupil, assist, restore, formula, perceive, sink, stare, anymore, meter, truck, sail, devote, terrorist, justify, fascinate, depression, guilty, underlie, distinction, incorporate, obligation, sir, anger, pub, perception …

**TSL 1.1 (토익): 포함 38.4% · 누락 775개**
- 순위 1~500: 188개 — mister, e-book, logical, goods, résumé, traveler, caller, correctly, preview, garage, oval, occupation, cellphone, compact, merchandise, dentist, tactic, replacement, media, underline, electrical, airplane, café, comprehension, mini, fitness, closet, unreal, distractor, donation, snack, provider, inspection, recipient, rewrite, indoor, dial, container, lab, respondent, skim, briefcase, inquire, overnight, advisor, shopper, announcer, aspect, audit, contractor, stadium, weekday, waitress, cleaner, developer, alike, flavor, recipe, commonly, accommodate, flu, captain, installation, trainer, bargain, midnight, rainy, unhappy, automobile, incomplete, dock, seldom, carrier, designate, suite, dental, duration, painter, patron, productive …
- 순위 501~1000: 374개 — considerably, informal, microscope, newsstand, rack, remodel, statistics, tunnel, unlimited, vitamin, zoo, alert, auditorium, celebrity, deduct, enthusiastic, graduation, icy, irregular, login, mineral, motorcycle, necessity, planner, programmer, recruiter, remainder, statue, accessory, assembly, basket, closure, dislike, downstairs, nail, pedestrian, sleeve, suburb, takeover, unsure, verbal, visa, wildlife, absent, accumulate, apprentice, businessman, colorful, costume, editorial, firefighter, gasoline, inappropriate, layout, lunchtime, pharmaceutical, plausible, safely, specialty, tech, unspecified, adhere, bankrupt, caution, clip, diner, duplicate, eager, embassy, fasten, harmful, informative, institute, kit, mentor, nominate, opt, parade, physician, polish …
- 순위 1001~1259: 213개 — lighter, loudly, loyalty, microwave, misidentify, neat, outfit, pastry, personalize, poorly, prestigious, purser, reassure, resume, reunion, revolutionize, seafood, signify, slot, steer, sue, superb, traditionally, unpleasant, violin, ward, worthwhile, advisable, archive, artistic, assurance, athletic, attire, butter, centimeter, circulate, comb, comfortably, cookbook, cushion, dose, drum, embed, evacuate, expedite, extinguisher, familiarity, fluent, hurricane, hygiene, integral, interactive, interfere, layoff, lightweight, needy, overpay, pamphlet, partial, penalize, pollute, prescribe, prominent, relocation, residence, retrieve, rider, rubber, rug, salespeople, someday, spectator, stereo, storeroom, subsidize, suspicious, tasty, terrific, underground, unpaid …

**BSL 1.01 (비즈니스): 포함 31.6% · 누락 1,200개**
- 순위 1~500: 265개 — mister, goods, sponsorship, media, audit, e-book, anti, entity, euro, aggregate, payable, aspect, calculation, subsidiary, receivable, pre, creditor, sub, incur, annuity, disclosure, regime, broker, coalition, maximize, beta, lender, fraud, regulator, par, provider, constitution, trader, monopoly, stockmarket, ex, breach, subsidy, corruption, issuer, borrower, insurer, patent, debit, duration, terrorism, respondent, takeover, coefficient, classify, offset, merchandise, bound, bargain, statistics, taxpayer, alliance, debtor, liable, scandal, defer, carrier, payoff, ethical, contractor, marketer, rebel, statute, born, bubble, acceptance, execute, defendant, matrix, graph, commerce, enforce, founder, replacement, telecom …
- 순위 501~1000: 353개 — willingness, tempt, broadly, demographic, prominent, conglomerate, contrary, credibility, simulation, senator, standardize, opt, sensible, headline, exemption, concession, occupation, privately, guerrilla, pharmaceutical, administer, repurchase, denote, plunge, nonetheless, overview, correctly, horizontal, revive, array, ballot, treasury, intermediary, reproduce, boast, militant, fate, qualitative, gang, oblige, curb, robust, brokerage, accurately, devise, inspector, incremental, fighter, subsidize, grip, mathematical, assert, underwrite, differentiate, correlate, agriculture, multiplier, adverse, suspicion, virtue, flee, threshold, timely, wholesale, legitimate, privacy, behavioral, dump, documentation, poorly, unemployed, discharge, explicit, breakdown, span, bail, incumbent, albeit, spokesman, correction …
- 순위 1001~1754: 582개 — rocket, debenture, collar, outperform, irrelevant, diamond, promotional, broadband, reactor, traveler, equality, entail, compile, circulation, petition, attributable, revolutionary, carmaker, discretionary, reconciliation, mutually, subprime, refusal, outfit, consortium, speculative, policeman, resemble, amortize, exploration, mill, loser, subjective, builder, mainland, retreat, peaceful, importantly, backward, ambassador, overwhelm, unprecedented, declaration, rebate, covariance, jointly, resignation, removal, exclusion, bomber, occurrence, viewer, spur, hazard, packet, omit, prospectus, conscious, robot, placement, desktop, telecommunication, buffer, infect, socialist, browser, cyclical, likewise, cartel, triumph, processor, divert, arguably, ordinate, casualty, verdict, dot, distinctive, inflationary, salesperson …

**베트남어 자막 빈도 상위 3,000 음절: 포함 54.0% · 누락 1,380개**
- 순위 1~500: 22개 — giết, ngươi, chúa, thằng, i, ko, oh, bắn, t, quân, c, n, đấu, quái, yeah, ng, khốn, sàng, gã, the, m, ư
- 순위 501~1000: 78개 — ổng, you, s, tiệt, okay, l, hey, vời, ma, ngu, đức, tụi, nè, lũ, kiếp, đem, uh, thậm, lão, ngựa, binh, v, trợ, đạn, kì, ok, th, hi, john, quỷ, huy, ch, đằng, lai, rắc, b, săn, tướng, thượng, soát, thánh, giây, dõi, and, cơn, jack, ah, tín, phủ, loạn, bom, nh, huynh, dĩ, lí, phóng, khỉ, á, sóc, frank, thủy, não, new, ngừng, siêu, it, diệt, chà, đài, can, khắp, chặn, hảo, xinh, cục, trấn, h, hữu
- 순위 1001~2000: 481개 — tàn, bang, kh, of, kêu, ẩn, úy, dàng, ngàn, hổ, châu, ngục, sam, whoa, me, ám, my, lạy, vinh, tổn, đệ, o, york, mông, bội, ống, bi, ha, d, dặm, hỏa, well, peter, james, lôi, giam, chiếm, e, on, địch, cắp, đâm, wow, that, phu, cặp, bạo, khiếp, vớ, thí, michael, thảm, rồng, um, kẹt, ngực, ben, rồ, đế, bả, g, đe, hư, khứ, harry, cóc, lẫn, câm, trần, cổng, ngọn, bám, phó, thai, mẽ, đụng, mike, jim, hung, claire, tống, ép, lui, mạch, charlie, tước, rachel, đc, mồm, don, david, vẩn, joey, đậu, phiếu, tom, mưu, nát, dũng, ngang …
- 순위 2001~3000: 799개 — đo, nạp, yo, bobby, city, xài, nhạy, xí, dàn, sờ, chóc, rick, nỗ, cạo, andy, tảng, doug, francis, wilson, dãy, finch, there, hank, ow, lật, độn, dại, hắc, marty, côn, ted, hiển, đệch, đô-la, now, nốt, quấy, hoá, queen, hello, ryan, maria, was, amy, bruce, chém, đãi, dược, if, khoái, radio, đếch, nọ, khấu, texas, lăn, lỏng, cừu, xíu, mm, bầy, toà, té, chuộc, viêm, dỗ, katie, cò, jones, they, ơ, tể, ngộ, good, victor, su, gordon, bẻ, roy, lạp, simon, xà, here, đai, lincoln, hố, sherlock, annie, eric, wayne, hạm, xưởng, nhấc, tẩy, vặt, edward, mại, carter, trích, jesse …

(자막 음절에는 인명·외래어 표기가 섞여 있어 전부가 학습 대상은 아님)

## 출처
- NGSL·TSL·BSL: Browne, C., Culligan, B. & Phillips, J., newgeneralservicelist.com — CC BY-SA 4.0
- 베트남어 빈도: hermitdave/FrequencyWords (OpenSubtitles 2018) — 내용 CC BY-SA 4.0

