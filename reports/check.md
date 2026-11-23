# 말뭉치 교차검증 리포트

`python3 tools/check.py`로 생성. 빌드 오류·완전 중복은 빌드 단계에서 차단됩니다.

## 1. 요약

| 항목 | 베트남어 | 영어 |
|---|---:|---:|
| 문장 | 4,755 | 7,134 |
| 풀이 단어(고유) | 4,759 | 6,389 |
| Lv1 · CEFR A1 (기초) | 153 | 196 |
| Lv2 · CEFR A2 (초급) | 330 | 383 |
| Lv3 · CEFR B1 (중급) | 1,497 | 1,393 |
| Lv4 · CEFR B2 (중상급) | 2,252 | 3,069 |
| Lv5 · CEFR C1 (고급) | 523 | 2,093 |

## 2. 중복

**[vi] 정규화 후 같은 문장: 0건** — 없음

[vi] 같은 한국어 뜻에 원어가 여러 개: 1건 (카드에서 정답이 모호할 수 있음)
- 여기서 내려 주세요. → `Cho tôi xuống ở đây.` / `Cho tôi dừng ở đây.`

**[en] 정규화 후 같은 문장: 0건** — 없음

[en] 같은 한국어 뜻에 원어가 여러 개: 22건 (카드에서 정답이 모호할 수 있음)
- 말씀 많이 들었어요. → `I've heard a lot about you.` / `I've heard so much about you.`
- 계산서 주세요. → `Can I get the check, please?` / `Could we get the check, please?`
- 방을 바꿀 수 있을까요? → `Is it possible to change rooms?` / `Would it be possible to switch rooms?`
- 마감이 언제예요? → `What's the deadline?` / `When's the deadline?`
- 주말 잘 보냈어요? → `How was your weekend?` / `Did you have a good weekend?`
- 농담이죠? → `You're kidding.` / `You're kidding, right?`
- 괜찮아요, 신경 쓰지 마세요. → `No worries. Don't worry about it.` / `It's fine. Don't worry about it.`
- 이 와인이랑 잘 어울리는 요리가 뭐예요? → `What would pair well with this wine?` / `What would go well with this wine?`
- 이번 주는 일정이 꽉 찼어요. → `My schedule's packed this week.` / `My schedule is packed this week.`
- 지금은 인력이 병목이에요. → `Resources are the bottleneck right now.` / `Right now, staffing is the bottleneck.`
- 이 수치는 보수적으로 잡은 거예요. → `These numbers are on the conservative side.` / `These figures are on the conservative side.`
- 최악의 시나리오도 대비해야 해요. → `We need to plan for the worst-case scenario.` / `We should prepare for the worst-case scenario as well.`
- 이해관계자들의 동의부터 받아야 해요. → `We need to get buy-in from stakeholders first.` / `We need to get buy-in from the stakeholders first.`
- 현지 음식을 꼭 먹어 보고 싶어요. → `I really want to try the local cuisine.` / `I really want to try the local food.`
- 그 둘은 별개의 문제예요. → `Those are two separate issues.` / `They are two different matters.`
- 금값이 사상 최고치를 다시 경신했다. → `Gold prices hit another record high.` / `Gold hit another record high.`
- 오늘 정말 즐거웠어요. → `I had a great time today.` / `I had a really great time today.`
- 영수증 주세요. → `Could I have the receipt?` / `Can I have the receipt?`
- 회의실 예약했어요. → `I booked a meeting room.` / `I've booked a meeting room.`
- 빨래 좀 개 줄래요? → `Could you fold the laundry?` / `Can you fold the laundry?`
- 보일러가 고장 났어요. → `The heater's broken.` / `The boiler broke down.`
- 좀 짜요. → `It's a little salty.` / `It's a bit salty.`

## 2-1. 단어·문장 구분

단어·숙어는 `w4|뜻|표현|...`처럼 레벨 앞에 w를 붙여 등록합니다. 문장 목록에는 완결된 문장만 둡니다.

**[vi] 문장 목록에 있는 단어 수준 항목: 0건** · 직접 등록한 단어·숙어 86개

**[en] 문장 목록에 있는 단어 수준 항목: 0건** · 직접 등록한 단어·숙어 2734개

## 3. 풀이·표기

**[vi] 풀이 없는 문장 406건 · 문장에 없는 풀이어 0건**
- 풀이 없음: `Việc sử dụng dịch vụ công trực tuyến tăng.` (vi_jr_c.txt)
- 풀이 없음: `Lừa đảo bằng deepfake đang gia tăng.` (vi_jr_c.txt)
- 풀이 없음: `Nhu cầu điện đạt mức cao kỷ lục.` (vi_jr_c.txt)
- 풀이 없음: `An ninh năng lượng là điều kiện tiên quyết cho tăng trưởng kinh tế.` (vi_jr_c.txt)
- 풀이 없음: `Cơ chế giá điện đang là rào cản thu hút đầu tư.` (vi_jr_c.txt)
- 풀이 없음: `Lương đã được tăng.` (vi_jr_d.txt)
- 풀이 없음: `Samsung là nhà đầu tư nước ngoài lớn nhất tại Việt Nam.` (vi_jr_d.txt)
- 풀이 없음: `Một nhà máy mới sẽ được xây dựng tại Hải Phòng.` (vi_jr_d.txt)
- 풀이 없음: `Người trẻ muốn cơ hội phát triển hơn là sự ổn định.` (vi_jr_d.txt)
- 풀이 없음: `Công ty đầu tư nhiều hơn vào đào tạo nhân viên.` (vi_jr_d.txt)
- 풀이 없음: `Văn hóa doanh nghiệp ảnh hưởng lớn đến hiệu quả làm việc.` (vi_jr_d.txt)
- 풀이 없음: `Miền Bắc thu hút nhiều vốn FDI nhất.` (vi_jr_d.txt)
- 풀이 없음: `Bắc Ninh là trung tâm công nghiệp điện tử.` (vi_jr_d.txt)
- 풀이 없음: `Các bệnh viện đang thiếu nhân viên y tế.` (vi_jr_e.txt)
- 풀이 없음: `Chất lượng giáo dục không thể vượt quá chất lượng giáo viên.` (vi_jr_e.txt)
- 풀이 없음: `Giá cả tăng trước Tết.` (vi_jr_e.txt)
- 풀이 없음: `Các chuỗi cà phê cạnh tranh gay gắt.` (vi_jr_e.txt)
- 풀이 없음: `Luật Bảo vệ quyền lợi người tiêu dùng đã được sửa đổi.` (vi_jr_e.txt)
- 풀이 없음: `Nhu cầu sản phẩm xanh tăng nhưng rào cản về giá vẫn còn.` (vi_jr_e.txt)
- 풀이 없음: `Người dân tập thể dục bên hồ.` (vi_jr_e.txt)
- 베트남어 문자 외 글자: 0건 — 없음

**[en] 풀이 없는 문장 590건 · 문장에 없는 풀이어 30건**
- 풀이 없음: `It is what it is.` (en_a.txt)
- 풀이 없음: `Let me see what I can do.` (en_d.txt)
- 풀이 없음: `Changing people is harder than changing technology.` (en_jr_a.txt)
- 풀이 없음: `A leader's most important job is setting priorities.` (en_jr_a.txt)
- 풀이 없음: `The biggest risk may be not using AI at all.` (en_jr_b.txt)
- 풀이 없음: `In diplomacy, silence is also a message.` (en_jr_c.txt)
- 풀이 없음: `The rules of the international order are being rewritten.` (en_jr_c.txt)
- 풀이 없음: `Trust between nations is hard to build and easy to lose.` (en_jr_c.txt)
- 풀이 없음: `Budgets reveal true priorities better than politicians' words.` (en_jr_c.txt)
- 풀이 없음: `The health of a democracy shows in the quality of its debate, not just turnout.` (en_jr_c.txt)
- 풀이 없음: `Climate refugees are already a reality.` (en_jr_c.txt)
- 풀이 없음: `The international community is demanding action, not words.` (en_jr_c.txt)
- 풀이 없음: `Education reform is the longest-term investment in the next generation.` (en_jr_c.txt)
- 풀이 없음: `Social media has become the new shopping mall.` (en_jr_d.txt)
- 풀이 없음: `Black Friday sales hit a record.` (en_jr_d.txt)
- 풀이 없음: `One good review is worth more than ten ads.` (en_jr_d.txt)
- 풀이 없음: `Strong brands gain market share during downturns.` (en_jr_d.txt)
- 풀이 없음: `The next stage of commerce is conversation, not search.` (en_jr_d.txt)
- 풀이 없음: `Getting customers to come back is the key to growth.` (en_jr_d.txt)
- 풀이 없음: `Companies are cutting business travel to save costs.` (en_jr_d.txt)
- 문장에 없는 풀이어 파일별: en_x_biz.txt 10, en_a.txt 3, en_wx_toefl.txt 3, en_l.txt 2, en_n_b.txt 2, en_wx_news.txt 2, en_c.txt 1, en_d.txt 1, en_e.txt 1, en_g.txt 1, en_jr_d.txt 1, en_jr_g.txt 1, en_mt_b.txt 1, en_n_e.txt 1
  - `not a bit` ← You haven't changed a bit. (en_a.txt)
  - `had better` ← I'd better get going. (en_a.txt)
  - `oversleep` ← I overslept. (en_a.txt)
  - `not sleep a wink` ← The room next door was loud all night. I didn't sleep a wink. (en_c.txt)
  - `play it by ear` ← I'm going to play this trip by ear. (en_d.txt)
  - `stick to` ← He stuck to his plan despite the criticism. (en_e.txt)
  - `die out` ← The language is in danger of dying out as speakers decline. (en_g.txt)
  - `buy now, pay later` ← Use of buy-now-pay-later services has jumped. (en_jr_d.txt)
  - `diagnosis` ← AI is improving the accuracy of medical diagnoses. (en_jr_g.txt)
  - `replacement` ← We'll replace the faulty part. (en_l.txt)
  - `inspection` ← The factory machinery was inspected regularly. (en_l.txt)
  - `make it right` ← We'd like to discuss how we can make this right. (en_mt_b.txt)
  - `overdo it` ← I overdid it lately and now I'm all achy. (en_n_b.txt)
  - `misunderstand` ← I must have misunderstood. (en_n_b.txt)
  - `have one's back` ← She's always got my back. (en_n_e.txt)
  - `deterioration` ← As his health deteriorated, he was hospitalized. (en_wx_news.txt)
  - `flee` ← Residents fled from the flood. (en_wx_news.txt)
  - `creep` ← The cat crept toward the mouse. (en_wx_toefl.txt)
  - `fisherman` ← The fishermen go out by boat at dawn. (en_wx_toefl.txt)
  - `foretell` ← The fortune teller foretold the future. (en_wx_toefl.txt)

## 4. 상황별 분포 (언어 간 균형)

| 상황 | 베트남어 | 영어 | 메모 |
|---|---:|---:|---|
| 인사·스몰토크 | 192 | 200 |  |
| 일상·가족 | 597 | 375 |  |
| 집·날씨 | 225 | 159 |  |
| 음식·요리 | 252 | 142 |  |
| 쇼핑·돈 | 275 | 221 |  |
| 여행·교통 | 435 | 244 |  |
| 시간·약속 | 192 | 136 |  |
| 건강·문제해결 | 224 | 243 |  |
| 취미·문화 | 274 | 158 |  |
| 영화·책 | 294 | 107 |  |
| 의견·경험 | 170 | 290 |  |
| 배움·시험 | 145 | 1793 |  |
| 업무·경영 | 623 | 1215 |  |
| 경제·금융·에너지 | 289 | 573 |  |
| 사회·정치·외교 | 257 | 802 |  |
| IT·AI | 216 | 332 |  |
| 명언·속담 | 95 | 144 |  |

## 5. 기준 어휘 목록 대비 누락

**NGSL 1.01 (일반 영어 핵심 2,801): 포함 89.7% · 누락 288개**
- 순위 501~1000: 4개 — television, male, possibility, yeah
- 순위 1001~2000: 56개 — aware, administration, sex, inform, appeal, slightly, presence, apparently, possibly, tape, murder, anybody, basically, mainly, tear, proper, afford, abuse, principal, session, association, sexual, musical, native, specifically, fat, surely, bore, latter, properly, ill, via, legislation, county, reward, meanwhile, permanent, urge, producer, accompany, liberal, disk, aircraft, maximum, motion, breast, accommodation, brown, occupy, journalist, advertisement, aside, secondly, prospect, plot, primarily
- 순위 2001~2801: 228개 — prize, typically, assistance, respectively, variation, tooth, representation, undertake, wire, gay, publication, unknown, inch, owe, contemporary, assure, numerous, virtually, coverage, isolate, wet, secondary, recruit, persuade, inspire, perceive, sink, stare, anymore, justify, underlie, incorporate, obligation, sir, pub, perception, naturally, constantly, boundary, withdraw, steel, designer, album, loose, tank, brilliant, adviser, stem, reverse, mode, awful, pose, nowadays, alcohol, van, web, log, independence, pink, strip, impress, vice, radical, similarly, subsequent, infection, dirty, resort, bloody, bend, alarm, newly, parallel, sponsor, boot, button, mate, occasionally, bath, tap …

**TSL 1.1 (토익): 포함 61.8% · 누락 481개**
- 순위 1~500: 106개 — mister, e-book, logical, résumé, caller, preview, oval, occupation, cellphone, merchandise, dentist, tactic, replacement, underline, airplane, café, comprehension, mini, closet, unreal, distractor, provider, inspection, recipient, indoor, dial, container, skim, briefcase, inquire, advisor, announcer, contractor, weekday, waitress, cleaner, commonly, trainer, midnight, automobile, incomplete, carrier, dental, patron, salad, salesperson, omit, spite, sculpture, ice cream, illogical, textbook, cabin, conductor, inspector, taker, sightsee, soup, lane, poster, housekeeper, knowledgeable, organizer, booklet, packet, auto, flyer, interrupt, showroom, administrator, ferry, instruct, overview, accomplishment, accustom, desktop, jog, leisure, nap, reinforce …
- 순위 501~1000: 237개 — considerably, informal, microscope, newsstand, rack, remodel, tunnel, unlimited, auditorium, icy, irregular, login, mineral, motorcycle, planner, programmer, recruiter, remainder, accessory, dislike, downstairs, pedestrian, sleeve, suburb, takeover, unsure, verbal, absent, businessman, colorful, costume, inappropriate, layout, lunchtime, pharmaceutical, plausible, specialty, unspecified, caution, diner, informative, institute, kit, mentor, nominate, opt, parade, physician, postage, recreational, rehearse, removal, satisfactory, accordingly, balcony, culinary, generic, jazz, massage, maximize, mild, ongoing, periodically, plug, referral, runner, sock, surf, timetable, vase, aboard, advancement, advertiser, alternatively, attorney, authorization, campus, candy, concierge, consistently …
- 순위 1001~1259: 138개 — microwave, misidentify, pastry, poorly, prestigious, purser, reassure, reunion, revolutionize, seafood, signify, slot, superb, violin, ward, worthwhile, advisable, archive, artistic, athletic, attire, butter, comb, comfortably, cookbook, cushion, extinguisher, integral, interactive, interfere, lightweight, needy, overpay, pamphlet, partial, penalize, prescribe, prominent, relocation, residence, retrieve, rider, salespeople, someday, spectator, stereo, storeroom, subsidize, suspicious, terrific, underground, unpaid, volleyball, wheelchair, wool, wrinkle, anyhow, appetizer, arc, audition, backpack, biography, bound, broom, cheeseburger, chilly, circus, continental, diagnostic, donut, doorman, electronically, euro, getaway, hardworking, impatient, indirect, irrelevant, jeans, journalism …

**BSL 1.01 (비즈니스): 포함 58.9% · 누락 721개**
- 순위 1~500: 136개 — mister, sponsorship, e-book, anti, euro, payable, calculation, receivable, sub, annuity, maximize, beta, par, provider, trader, monopoly, stockmarket, ex, issuer, patent, debit, takeover, coefficient, offset, merchandise, bound, taxpayer, liable, scandal, carrier, payoff, contractor, marketer, rebel, statute, acceptance, matrix, replacement, telecom, referendum, indirect, sophisticate, businessman, commonly, superior, taxation, multinational, plaintiff, withdrawal, taxable, pledge, modest, convertible, thereby, ledger, linear, ministry, multiply, presidency, rational, violation, spreadsheet, predecessor, sole, chancellor, notably, likelihood, orient, insider, railway, minus, constitutional, privatization, tactic, missile, remedy, accordance, parliamentary, vertical, reinforce …
- 순위 501~1000: 209개 — willingness, broadly, prominent, simulation, senator, standardize, opt, sensible, occupation, privately, pharmaceutical, repurchase, nonetheless, overview, treasury, intermediary, reproduce, militant, qualitative, oblige, robust, brokerage, inspector, incremental, subsidize, mathematical, underwrite, agriculture, multiplier, flee, threshold, legitimate, behavioral, documentation, poorly, unemployed, span, bail, incumbent, spokesman, contingency, recipient, subtract, surrender, judicial, administrator, logical, rebuild, litigation, generic, layout, unchanged, queue, bidder, respective, textbook, redemption, meaningful, interface, inevitably, withhold, sterling, thrive, commander, toll, incorporation, termination, invasion, bondholder, computation, advisory, modification, customize, spectrum, tuple, magnitude, gallon, considerably, intervene, repertoire …
- 순위 1001~1754: 376개 — rocket, debenture, collar, outperform, irrelevant, promotional, petition, attributable, carmaker, discretionary, reconciliation, mutually, subprime, speculative, policeman, resemble, amortize, mill, subjective, mainland, retreat, importantly, backward, overwhelm, unprecedented, declaration, rebate, covariance, jointly, removal, bomber, occurrence, spur, packet, omit, prospectus, placement, desktop, telecommunication, infect, socialist, browser, cyclical, likewise, cartel, triumph, processor, arguably, ordinate, inflationary, salesperson, tort, positively, unlimited, inflate, mineral, liberalization, buyout, separation, internationally, retrieve, individually, dip, inclusion, copper, justification, outright, stance, wheat, enlargement, lesser, republic, artificial, trait, maximization, afterward, spouse, continually, interference, proportional …

**베트남어 자막 빈도 상위 3,000 음절: 포함 60.4% · 누락 1,187개**
- 순위 1~500: 20개 — giết, ngươi, chúa, thằng, i, ko, oh, bắn, t, c, n, quái, yeah, ng, khốn, gã, a, the, m, ư
- 순위 501~1000: 48개 — ổng, you, s, tiệt, okay, l, hey, vời, ngu, đức, tụi, nè, kiếp, uh, thậm, binh, v, đạn, kì, ok, th, hi, john, quỷ, ch, b, thánh, giây, and, cơn, jack, ah, bom, nh, huynh, dĩ, lí, khỉ, frank, não, new, ngừng, diệt, chà, can, xinh, trấn, h
- 순위 1001~2000: 395개 — tàn, kh, of, úy, dàng, ngàn, hổ, ngục, sam, whoa, me, ám, my, lạy, đệ, o, york, mông, bội, ống, ha, hỏa, well, peter, james, lôi, giam, on, địch, cắp, đâm, wow, that, phu, vớ, michael, thảm, rồng, um, kẹt, ngực, ben, rồ, đế, bả, g, hư, khứ, harry, cóc, câm, cổng, ngọn, bám, thai, mẽ, đụng, mike, jim, hung, claire, tống, ép, charlie, tước, rachel, đc, mồm, don, david, vẩn, joey, đậu, tom, nát, ngang, gan, ross, man, kí, thèm, alex, chôn, liều, đéo, all, đương, đếm, george, what, we, fbi, sỹ, nô, hmm, hoại, huấn, gác, joe, túy …
- 순위 2001~3000: 724개 — yo, bobby, city, xài, xí, dàn, sờ, chóc, rick, cạo, andy, doug, francis, wilson, dãy, finch, there, hank, ow, lật, độn, dại, hắc, marty, côn, ted, hiển, đệch, đô-la, now, nốt, quấy, hoá, queen, hello, ryan, maria, was, amy, bruce, đãi, dược, if, khoái, radio, đếch, texas, lăn, cừu, xíu, mm, bầy, toà, té, chuộc, viêm, dỗ, katie, cò, jones, they, ơ, tể, good, victor, gordon, bẻ, roy, lạp, simon, xà, here, lincoln, hố, sherlock, annie, eric, wayne, hạm, xưởng, nhấc, tẩy, vặt, edward, carter, trích, jesse, king, cưỡi, sean, vịt, trộn, giùm, tát, tiềm, ối, time, giảng, let, al …

(자막 음절에는 인명·외래어 표기가 섞여 있어 전부가 학습 대상은 아님)

## 출처
- NGSL·TSL·BSL: Browne, C., Culligan, B. & Phillips, J., newgeneralservicelist.com — CC BY-SA 4.0
- 베트남어 빈도: hermitdave/FrequencyWords (OpenSubtitles 2018) — 내용 CC BY-SA 4.0

