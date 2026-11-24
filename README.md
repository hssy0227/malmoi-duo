# 말모이 듀오 — 베트남어·영어 회화 연습 PWA

혼자 쓰는 회화 연습 앱. 베트남어(북부 표준) 4,755문장·단어 4,830개, 영어 7,134문장·단어 6,403개.
상황 17개 × 레벨 5단계(CEFR A1~C1), 카드(간격 반복)·퀴즈 4종·듣기·말하기·사전.
이메일 + PIN 계정으로 기기 간 진도 동기화(Supabase), 항목마다 새것·읽음·학습 중·앎·스킵 상태 관리.

## 폴더 구조
```
content/          문장 원본 (vi_*.txt, en_*.txt) ← 문장 추가·수정은 여기서
sources/          생성용 원본
  core_parallel_*.txt  두 언어 공통 핵심 문장(한국어 뜻 공유) → gen_core.py → content/*_y_core.txt
  biz_*            첨부 비즈니스 영어 600개 + 한국어 해석 → gen_biz.py → content/en_x_biz.txt
  ref/             기준 어휘 목록(NGSL·TSL·BSL, 베트남어 자막 빈도) — 교차검증용
tools/check.py    교차검증 → reports/check.md
tools/dedupe.py   새 파일에서 같은 언어 다른 파일과 겹치는 문장 자동 제거
tools/items.py    content → Supabase items 행
tools/sync_items.py · tools/keepalive.py   GitHub Actions에서 실행
supabase/schema.sql  Supabase 테이블·권한 (SQL Editor에서 1회 실행)
src/              앱 소스 (app.html, sw.js, manifest.json, icons/)
build.py          content + src → dist 생성
config.json       Supabase 주소·공개 키 (공개돼도 되는 값만)
```

## 수정 → 배포
```
python3 sources/gen_core.py   # core_parallel을 고쳤을 때
python3 tools/dedupe.py content/새파일.txt   # 새 파일을 추가했을 때 기존 문장과 겹치는 줄 제거
python3 tools/check.py        # 중복·누락 교차검증 → reports/check.md
python3 build.py              # dist/ 갱신
git add -A && git commit -m "변경 내용" && git push
```
push하면 Vercel이 배포하고, content가 바뀌었으면 GitHub Actions가 Supabase items 테이블도 갱신합니다.

## 레벨 (두 언어 공통)
| 레벨 | CEFR | 이름 | 베트남어 능력 기준(2015년 고시) |
|---|---|---|---|
| Lv1 | A1 | 기초 | 1등급 |
| Lv2 | A2 | 초급 | 2등급 |
| Lv3 | B1 | 중급 | 3등급 |
| Lv4 | B2 | 중상급 | 4등급 |
| Lv5 | C1 | 고급 | 5등급 |

Supabase `items_view`·`progress_view`에서 `level_label`이 `Lv3 · CEFR B1` 형태로 보입니다.

## 출처 표기 (사전의 약자·범례)
파일·상황에 따라 `build.py`의 `src_of()`가 자동으로 붙입니다. 단어는 예문들의 출처를 모두 표시합니다.

| 약자 | 이름 | 어떻게 만들었나 | 파일 |
|---|---|---|---|
| G | 일반 | 일반 회화 상황 기준으로 직접 작성 (기본 세트, 여행·영화·책, 두 언어 공통 핵심) | 나머지 전부 |
| NG | 핵심어휘 | NGSL 2,801 대비 누락 고빈도 단어로 작성 | en_j, en_k |
| TE | 토익 | 토익 Part 1~7 장면 + TSL 누락 어휘 + 첨부 DB의 토익·토플 고급 어휘 | en_e, en_f, en_i, en_l, en_h(토익), en_x_biz(토익), en_wd_toeic(단어), en_wx_toeic(예문), en_wm_toeic(다의어 보조 예문) |
| TF | 토플 | 토플 강의 주제 + 스피킹 의견·경험 답변 | en_g, en_h(의견·경험), en_wd_toefl(단어), en_wx_toefl(예문), en_wm_toefl(다의어 보조 예문) |
| Biz | 비즈니스 | 첨부 비즈니스 영어 DB (예문 원문 + 한국어 해석) | en_x_biz |
| Mv | 영화 구어 | 베트남어 자막 빈도 대비 누락 구어로 작성 | vi_p |
| Adv | 고급 | 베트남어 능력 기준 5등급(C1) 주제로 작성 | vi_q |
| Jr | 저널·뉴스 | 경제·사회·외교·IT·에너지·커머스 기사 문체로 직접 작성 (실제 기사 문장 복제 없음) | en_jr_*, en_wd_news(단어), en_wx_news(예문), en_wm_news(다의어 보조 예문), vi_jr_* |
| Pv | 속담·명언 | 두 언어의 전래 속담·관용구·민요(ca dao) + 출처가 분명한 1929년 이전 저작·미국 정부 공문서의 짧은 명언. 메모에 직역·출처 | en_pv_*, vi_pv_* |
| Mt | 비즈니스 미팅 | 회의 진행·협상·보고·발표·메일·접대 상황으로 직접 작성 | en_mt_*, vi_mt_* |

## 문장 형식
```
@food                                  ← 상황 카테고리
레벨|한국어|원어|단어=뜻; 단어=뜻|메모(선택)
2|포장해 주세요.|Cho tôi mang về.|mang về=가지고 가다
w4|용두사미.|Đầu voi đuôi chuột.|đầu=머리; chuột=쥐|직역: 코끼리 머리에 쥐 꼬리   ← 단어·숙어
```
- **단어와 문장 구분**: 단어·복합어·구·숙어(영어 idiom·구동사, 베트남어 thành ngữ)는 레벨 앞에 `w`를 붙여 **단어**로 등록하고, 문장 목록에는 완결된 문장(속담 tục ngữ·명언 포함)만 둡니다. 문장 풀이의 단어도 자동으로 단어장에 들어가며, 같은 표제어면 합쳐집니다. 문장 하나가 통째로 풀이어인 경우는 `check.py --strict`가 막습니다.
- **단어 목록 추가**: 첨부 어휘 CSV(단어·품사·분야·레벨·뜻)는 `en_wd_*.txt`에 `w레벨|뜻|단어||품사` 줄로 넣었습니다(예문 없이 단어만). 이미 있는 단어는 없던 뜻만 합쳤고, 레벨은 NGSL 순위로 기초 단어를 낮췄습니다(CSV의 B2/C1/C2 → 4/5/5).
- 문장을 단어로 옮기면 앱이 옛 문장 ID의 진도·즐겨찾기·상태를 단어 ID로 자동 이관합니다.
- 상황 17개 (content 파일의 옛 @키는 build.py의 CAT_MAP으로 묶임 — 파일은 그대로 둬도 됨)

| 키 | 상황 | 묶인 옛 키 |
|---|---|---|
| greet | 인사·스몰토크 | greet, social |
| daily | 일상·가족 | daily, family |
| home | 집·날씨 | home, nature |
| food | 음식·요리 | food, cook |
| shop | 쇼핑·돈 | shop, money |
| travel | 여행·교통 | travel, move, stay |
| time | 시간·약속 | time, phone |
| health | 건강·문제해결 | health, trouble |
| hobby | 취미·문화 | hobby, culture |
| movie | 영화·책 | movie, book |
| opinion | 의견·경험 | opinion, life |
| study | 배움·시험 | study, toeic, acad |
| work | 업무·경영 | work, biz, mgmt, org |
| econ | 경제·금융·에너지 | econ, fin, energy |
| society | 사회·정치·외교 | society |
| saying | 명언·속담 | saying |
| tech | IT·AI | tech, ai |
- 진도는 원어 문장 기준 ID로 저장 → 순서를 바꾸거나 추가해도 기존 진도 유지 (원어를 고친 문장만 새 카드)
- 단어장은 단어 풀이에서 자동 생성

## 교차검증 (`tools/check.py`)
완전 중복은 빌드에서 막고, 아래는 리포트로 확인합니다.
- 구두점·축약형을 무시한 유사 중복, 같은 한국어 뜻에 원어가 여러 개인 경우(카드 정답 모호)
- 풀이 없는 문장, 문장에 없는 풀이어, 베트남어 NFC·문자 검사
- 언어별 상황 × 레벨 분포
- 기준 어휘 대비 누락: NGSL(일반 2,801) · TSL(토익) · BSL(비즈니스), 베트남어 자막 빈도 상위 3,000 음절
- `core_parallel`은 한 줄에 두 언어를 함께 적어 한쪽 언어만 빠지는 일이 없게 함

## 계정·동기화 설정 (Supabase, 처음 한 번)
1. supabase.com → New project (무료 플랜, 지역은 Seoul 또는 Tokyo)
2. **SQL Editor** → `supabase/schema.sql` 전체 붙여 넣고 Run
3. **Authentication → Sign In / Providers → Email**
   - 비밀번호 최소 길이: **6** (PIN 6자리를 쓰기 위해)
   - Confirm email: 켜 두면 가입 시 인증 메일 → 링크를 누르면 앱으로 돌아와 로그인. 끄면 바로 로그인
4. **Authentication → URL Configuration** → Site URL: `https://malmoi-duo.vercel.app`, Redirect URLs에도 같은 주소 추가
5. **Project Settings → API Keys**에서 Project URL과 publishable(또는 anon) 키를 `config.json`에 넣고 push
6. 같은 화면의 secret(또는 service_role) 키 → GitHub 저장소 **Settings → Secrets and variables → Actions → New repository secret**
   이름 `SUPABASE_SERVICE_KEY` (절대 config.json에 넣지 말 것)
7. GitHub **Actions** 탭에서 `Sync items to Supabase`, `Supabase keepalive`를 각각 Run workflow로 한 번 실행

### 휴면 방지
- Supabase 무료 플랜은 7일간 DB 활동이 없으면 일시정지 → `keepalive.yml`이 월·목 12:17(KST)에 DB에 기록을 남김
- GitHub는 60일간 저장소 활동이 없으면 예약 실행을 끔 → 같은 워크플로가 매번 자신을 다시 활성화해 카운터를 초기화

## 음성
- 발음: 기기 내장 TTS. 베트남어 음성이 없으면 재생하지 않고 설치 안내 (갤럭시: 설정 → 일반 → 텍스트 음성 변환)
- 말하기: 브라우저 음성 인식 — Chrome 권장, 마이크 허용 필요

## 출처·라이선스
- 문장: 직접 작성(공식 시험·교육과정의 주제와 수준표를 참고). 저널·뉴스형(Jr)은 실제 기사 문장을 옮기지 않고 기사 문체로 새로 쓴 것. 영어 비즈니스 600개는 사용자 제공 목록에 한국어 해석을 붙인 것
- NGSL 1.01 · TSL 1.1 · BSL 1.01 — Browne, C., Culligan, B. & Phillips, J., newgeneralservicelist.com, CC BY-SA 4.0
  (목록 파일은 antdurrant/word.lists 저장소 사본에서 추출)
- 베트남어 빈도 — hermitdave/FrequencyWords (OpenSubtitles 2018), 내용 CC BY-SA 4.0
- `sources/ref/`의 목록은 같은 라이선스(CC BY-SA 4.0)를 따릅니다

## 학습 알림 (웹 푸시) 설정

앱 설정 → "학습 알림"에서 주기(매일/격일/매주 요일)와 시각(한국 시간)을 고르면, 서버가 정각에 푸시를 보냅니다.

1. `supabase/push.sql` 을 SQL Editor에서 실행 (구독 테이블)
2. Edge Functions → 새 함수 `send-push` 에 `supabase/functions/send-push/index.ts` 붙여 넣기, **Verify JWT 끄기**, Deploy
3. Edge Functions → Secrets 에 `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT`, `CRON_SECRET` 추가
4. `supabase/cron.sql` 의 `<PROJECT_URL>`·`<CRON_SECRET>` 을 채워 SQL Editor에서 실행 (매시 정각 호출)
5. 앱 `config.json` 의 `vapidPublicKey` 는 공개 키(앱에 들어가도 안전). 비공개 키는 Secrets 에만 둡니다.

## 관리자 화면 (사용 통계)

계정별·기능별 사용량, 학습 성과, 콘텐츠 오답률, 게임 기록, 오류·DB 용량을 앱 안에서 봅니다. `admins`에 등록된 계정만 설정 화면 맨 아래에 **admin** 버튼이 보입니다.

1. Supabase → SQL Editor에 `supabase/admin.sql`을 통째로 붙여 넣고 Run (사용 로그·일별 요약 테이블, 관리자 함수, 매일 00:10 KST 집계 스케줄)
2. 파일 맨 아래 `여기에_본인_이메일`을 본인 로그인 이메일로 바꾼 3줄만 다시 Run → 관리자 지정
3. 앱에서 로그인 상태로 설정 화면을 열면 몇 초 뒤 **admin** 버튼이 나타남

- 앱은 이메일 외 개인정보 없이 기능·결과(카드 등급, 퀴즈 정답 여부, 말하기 점수, 게임 기록, 오류 메시지, 앱 버전·기기 종류)만 `events`에 남깁니다. 원본은 90일 뒤 지우고 `daily_stats`에 일별 요약으로 남깁니다.
- 관리자 함수는 SECURITY DEFINER로, 호출한 계정이 `admins`에 없으면 거부합니다. 화면은 읽기 전용입니다.
- 관리자를 빼려면: `delete from public.admins where user_id = (select id from auth.users where email = '…');`
