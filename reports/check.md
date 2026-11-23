# 말뭉치 교차검증 리포트

`python3 tools/check.py`로 생성. 빌드 오류·완전 중복은 빌드 단계에서 차단됩니다.

## 1. 요약

| 항목 | 베트남어 | 영어 |
|---|---:|---:|
| 문장 | 4,678 | 4,573 |
| 풀이 단어(고유) | 4,649 | 4,092 |
| Lv1 · CEFR A1 (기초) | 163 | 111 |
| Lv2 · CEFR A2 (초급) | 325 | 275 |
| Lv3 · CEFR B1 (중급) | 1,482 | 1,241 |
| Lv4 · CEFR B2 (중상급) | 2,194 | 1,838 |
| Lv5 · CEFR C1 (고급) | 514 | 1,108 |

## 2. 중복

**[vi] 정규화 후 같은 문장: 0건** — 없음

[vi] 같은 한국어 뜻에 원어가 여러 개: 1건 (카드에서 정답이 모호할 수 있음)
- 여기서 내려 주세요. → `Cho tôi xuống ở đây.` / `Cho tôi dừng ở đây.`

**[en] 정규화 후 같은 문장: 0건** — 없음

[en] 같은 한국어 뜻에 원어가 여러 개: 21건 (카드에서 정답이 모호할 수 있음)
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
- 금값이 사상 최고치를 다시 경신했다. → `Gold prices hit another record high.` / `Gold hit another record high.`
- 오늘 정말 즐거웠어요. → `I had a great time today.` / `I had a really great time today.`
- 영수증 주세요. → `Could I have the receipt?` / `Can I have the receipt?`
- 회의실 예약했어요. → `I booked a meeting room.` / `I've booked a meeting room.`
- 빨래 좀 개 줄래요? → `Could you fold the laundry?` / `Can you fold the laundry?`
- 보일러가 고장 났어요. → `The heater's broken.` / `The boiler broke down.`
- 좀 짜요. → `It's a little salty.` / `It's a bit salty.`

## 3. 풀이·표기

**[vi] 풀이 없는 문장 404건 · 문장에 없는 풀이어 0건**
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

**[en] 풀이 없는 문장 554건 · 문장에 없는 풀이어 25건**
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
- 풀이 없음: `The race to the lowest price is squeezing suppliers.` (en_jr_d.txt)
- 풀이 없음: `Inflation is the heaviest tax on the poorest.` (en_jr_d.txt)
- 문장에 없는 풀이어 파일별: en_x_biz.txt 10, en_a.txt 3, en_l.txt 2, en_n_b.txt 2, en_c.txt 1, en_d.txt 1, en_e.txt 1, en_g.txt 1, en_jr_d.txt 1, en_jr_g.txt 1, en_mt_b.txt 1, en_n_e.txt 1
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

## 4. 상황별 분포 (언어 간 균형)

| 상황 | 베트남어 | 영어 | 메모 |
|---|---:|---:|---|
| 인사·스몰토크 | 199 | 203 |  |
| 일상·가족 | 602 | 371 |  |
| 집·날씨 | 225 | 114 |  |
| 음식·요리 | 252 | 127 |  |
| 쇼핑·돈 | 272 | 221 |  |
| 여행·교통 | 436 | 235 |  |
| 시간·약속 | 202 | 137 |  |
| 건강·문제해결 | 224 | 216 |  |
| 취미·문화 | 274 | 133 |  |
| 영화·책 | 294 | 98 |  |
| 의견·경험 | 170 | 255 |  |
| 배움·시험 | 144 | 581 |  |
| 업무·경영 | 623 | 824 |  |
| 경제·금융·에너지 | 289 | 542 |  |
| 사회·정치·외교 | 257 | 196 |  |
| IT·AI | 215 | 320 |  |

## 5. 기준 어휘 목록 대비 누락

**NGSL 1.01 (일반 영어 핵심 2,801): 포함 80.4% · 누락 550개**
- 순위 1~500: 1개 — himself
- 순위 501~1000: 12개 — inside, press, television, bar, except, associate, male, possibility, female, agency, yeah, pound
- 순위 1001~2000: 125개 — rich, aware, administration, remove, chair, sex, inform, appeal, slightly, federal, horse, feed, presence, ball, refuse, apparently, desire, length, possibly, cancer, convince, tape, murder, hate, dear, onto, fashion, bomb, council, anybody, basically, violence, mainly, gun, troop, tear, proper, afford, frame, abuse, principal, session, appearance, elect, association, sexual, musical, declare, native, specifically, fat, fellow, surely, guard, bore, somehow, latter, command, column, criminal, properly, ill, via, legislation, county, hell, reward, meanwhile, furthermore, accuse, absence, construct, remark, northern, estate, equally, victory, permanent, urge, enemy …
- 순위 2001~2801: 412개 — prize, typically, assistance, roof, respectively, variation, tooth, representation, preparation, emphasis, edition, silver, entertainment, undertake, wire, gay, publication, slight, unknown, inch, equivalent, solid, owe, governor, port, arrival, contemporary, beer, specialist, assure, numerous, virtually, coverage, cable, isolate, prisoner, wet, secondary, recruit, exclude, string, persuade, inspire, hence, pupil, formula, perceive, sink, stare, anymore, meter, truck, sail, devote, terrorist, justify, fascinate, depression, guilty, underlie, distinction, incorporate, obligation, sir, anger, pub, perception, naturally, height, western, constantly, muscle, scare, boundary, essay, scream, withdraw, pollution, disorder, symbol …

**TSL 1.1 (토익): 포함 45.0% · 누락 692개**
- 순위 1~500: 158개 — mister, e-book, logical, goods, résumé, traveler, caller, preview, garage, oval, occupation, cellphone, compact, merchandise, dentist, tactic, replacement, underline, electrical, airplane, café, comprehension, mini, fitness, closet, unreal, distractor, donation, provider, inspection, recipient, indoor, dial, container, respondent, skim, briefcase, inquire, advisor, announcer, aspect, audit, contractor, stadium, weekday, waitress, cleaner, alike, commonly, captain, trainer, midnight, rainy, unhappy, automobile, incomplete, dock, seldom, carrier, designate, dental, duration, painter, patron, salad, delegate, salesperson, omit, spite, correspondence, sculpture, ice cream, basketball, delete, illogical, textbook, accurately, cabin, conductor, inspector …
- 순위 501~1000: 341개 — considerably, informal, microscope, newsstand, rack, remodel, tunnel, unlimited, vitamin, zoo, auditorium, celebrity, deduct, enthusiastic, graduation, icy, irregular, login, mineral, motorcycle, planner, programmer, recruiter, remainder, statue, accessory, basket, closure, dislike, downstairs, nail, pedestrian, sleeve, suburb, takeover, unsure, verbal, wildlife, absent, accumulate, apprentice, businessman, colorful, costume, editorial, firefighter, gasoline, inappropriate, layout, lunchtime, pharmaceutical, plausible, safely, specialty, unspecified, adhere, bankrupt, caution, clip, diner, eager, embassy, fasten, informative, institute, kit, mentor, nominate, opt, parade, physician, polish, postage, recreational, rehearse, removal, satisfactory, accordingly, applicable, balcony …
- 순위 1001~1259: 193개 — loudly, microwave, misidentify, neat, outfit, pastry, poorly, prestigious, purser, reassure, reunion, revolutionize, seafood, signify, slot, sue, superb, traditionally, unpleasant, violin, ward, worthwhile, advisable, archive, artistic, assurance, athletic, attire, butter, centimeter, circulate, comb, comfortably, cookbook, cushion, dose, drum, embed, expedite, extinguisher, familiarity, fluent, hurricane, hygiene, integral, interactive, interfere, lightweight, needy, overpay, pamphlet, partial, penalize, pollute, prescribe, prominent, relocation, residence, retrieve, rider, salespeople, someday, spectator, stereo, storeroom, subsidize, suspicious, tasty, terrific, underground, unpaid, volleyball, wheelchair, wool, wrinkle, anyhow, appetizer, arc, audition, backpack …

**BSL 1.01 (비즈니스): 포함 40.5% · 누락 1,043개**
- 순위 1~500: 208개 — mister, goods, sponsorship, audit, e-book, anti, entity, euro, aggregate, payable, aspect, calculation, receivable, creditor, sub, annuity, broker, coalition, maximize, beta, lender, par, provider, constitution, trader, monopoly, stockmarket, ex, corruption, issuer, borrower, patent, debit, duration, terrorism, respondent, takeover, coefficient, classify, offset, merchandise, bound, taxpayer, debtor, liable, scandal, defer, carrier, payoff, ethical, contractor, marketer, rebel, statute, acceptance, defendant, matrix, graph, replacement, telecom, accumulate, exploit, diagram, referendum, indirect, sophisticate, businessman, commonly, superior, taxation, multinational, plaintiff, withdrawal, consolidate, taxable, subordinate, pledge, modest, convertible, thereby …
- 순위 501~1000: 305개 — willingness, tempt, broadly, prominent, conglomerate, contrary, simulation, senator, standardize, opt, sensible, exemption, concession, occupation, privately, guerrilla, pharmaceutical, administer, repurchase, denote, nonetheless, overview, horizontal, array, ballot, treasury, intermediary, reproduce, boast, militant, fate, qualitative, gang, oblige, curb, robust, brokerage, accurately, devise, inspector, incremental, fighter, subsidize, grip, mathematical, assert, underwrite, differentiate, correlate, agriculture, multiplier, adverse, suspicion, virtue, flee, threshold, legitimate, behavioral, dump, documentation, poorly, unemployed, discharge, explicit, breakdown, span, bail, incumbent, albeit, spokesman, contingency, recipient, subtract, surrender, judicial, certainty, administrator, logical, rebuild, corrupt …
- 순위 1001~1754: 530개 — rocket, debenture, collar, outperform, irrelevant, diamond, promotional, broadband, traveler, equality, entail, compile, circulation, petition, attributable, revolutionary, carmaker, discretionary, reconciliation, mutually, subprime, refusal, outfit, consortium, speculative, policeman, resemble, amortize, exploration, mill, subjective, mainland, retreat, peaceful, importantly, backward, overwhelm, unprecedented, declaration, rebate, covariance, jointly, resignation, removal, exclusion, bomber, occurrence, viewer, spur, hazard, packet, omit, prospectus, conscious, placement, desktop, telecommunication, infect, socialist, browser, cyclical, likewise, cartel, triumph, processor, divert, arguably, ordinate, casualty, verdict, dot, distinctive, inflationary, salesperson, tort, positively, unlimited, inflate, constituency, mineral …

**베트남어 자막 빈도 상위 3,000 음절: 포함 59.8% · 누락 1,207개**
- 순위 1~500: 19개 — giết, ngươi, chúa, thằng, i, ko, oh, bắn, t, c, n, quái, yeah, ng, khốn, gã, the, m, ư
- 순위 501~1000: 51개 — ổng, you, s, tiệt, okay, l, hey, vời, ngu, đức, tụi, nè, kiếp, uh, thậm, lão, ngựa, binh, v, đạn, kì, ok, th, hi, john, quỷ, ch, b, săn, thánh, giây, and, cơn, jack, ah, bom, nh, huynh, dĩ, lí, khỉ, frank, não, new, ngừng, diệt, chà, can, xinh, trấn, h
- 순위 1001~2000: 405개 — tàn, kh, of, úy, dàng, ngàn, hổ, ngục, sam, whoa, me, ám, my, lạy, vinh, đệ, o, york, mông, bội, ống, ha, dặm, hỏa, well, peter, james, lôi, giam, on, địch, cắp, đâm, wow, that, phu, michael, thảm, rồng, um, kẹt, ngực, ben, rồ, đế, bả, g, hư, khứ, harry, cóc, câm, cổng, ngọn, bám, thai, mẽ, đụng, mike, jim, hung, claire, tống, ép, charlie, tước, rachel, đc, mồm, don, david, vẩn, joey, đậu, tom, mưu, nát, ngang, gan, ross, man, kí, thèm, alex, chôn, liều, đéo, all, đương, đếm, george, what, we, fbi, sỹ, nô, hmm, hoại, huấn, gác …
- 순위 2001~3000: 732개 — yo, bobby, city, xài, xí, dàn, sờ, chóc, rick, cạo, andy, doug, francis, wilson, dãy, finch, there, hank, ow, lật, độn, dại, hắc, marty, côn, ted, hiển, đệch, đô-la, now, nốt, quấy, hoá, queen, hello, ryan, maria, was, amy, bruce, đãi, dược, if, khoái, radio, đếch, nọ, texas, lăn, cừu, xíu, mm, bầy, toà, té, chuộc, viêm, dỗ, katie, cò, jones, they, ơ, tể, good, victor, gordon, bẻ, roy, lạp, simon, xà, here, lincoln, hố, sherlock, annie, eric, wayne, hạm, xưởng, nhấc, tẩy, vặt, edward, carter, trích, jesse, king, cưỡi, sean, vịt, trộn, giùm, tát, tiềm, ối, time, giảng, let …

(자막 음절에는 인명·외래어 표기가 섞여 있어 전부가 학습 대상은 아님)

## 출처
- NGSL·TSL·BSL: Browne, C., Culligan, B. & Phillips, J., newgeneralservicelist.com — CC BY-SA 4.0
- 베트남어 빈도: hermitdave/FrequencyWords (OpenSubtitles 2018) — 내용 CC BY-SA 4.0

