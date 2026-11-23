# 말모이 듀오 — 베트남어·영어 회화 연습 PWA

혼자 쓰는 회화 연습 앱. 베트남어(북부 표준) 2,723문장·단어 3,388개, 영어 2,569문장·표현 2,969개.
상황 27개(베트남어)·35개(영어) × 레벨 5단계(CEFR A1~C1), 카드(간격 반복)·퀴즈 4종·듣기·말하기·사전.
이메일 + PIN 계정으로 기기 간 진도 동기화(Supabase), 항목마다 새것·읽음·학습 중·앎·스킵 상태 관리.

## 폴더 구조
```
content/          문장 원본 (vi_*.txt, en_*.txt) ← 문장 추가·수정은 여기서
sources/          생성용 원본
  core_parallel_*.txt  두 언어 공통 핵심 문장(한국어 뜻 공유) → gen_core.py → content/*_y_core.txt
  biz_*            첨부 비즈니스 영어 600개 + 한국어 해석 → gen_biz.py → content/en_x_biz.txt
  ref/             기준 어휘 목록(NGSL·TSL·BSL, 베트남어 자막 빈도) — 교차검증용
tools/check.py    교차검증 → reports/check.md
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

## 문장 형식
```
@food                                  ← 상황 카테고리
레벨|한국어|원어|단어=뜻; 단어=뜻|메모(선택)
2|포장해 주세요.|Cho tôi mang về.|mang về=가지고 가다
```
- 카테고리: greet daily food shop move stay time phone work social health travel trouble opinion life
  cook hobby biz home money tech nature culture family study movie book · toeic acad mgmt org econ fin ai energy (영어)
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
- 문장: 직접 작성(공식 시험·교육과정의 주제와 수준표를 참고). 영어 비즈니스 600개는 사용자 제공 목록에 한국어 해석을 붙인 것
- NGSL 1.01 · TSL 1.1 · BSL 1.01 — Browne, C., Culligan, B. & Phillips, J., newgeneralservicelist.com, CC BY-SA 4.0
  (목록 파일은 antdurrant/word.lists 저장소 사본에서 추출)
- 베트남어 빈도 — hermitdave/FrequencyWords (OpenSubtitles 2018), 내용 CC BY-SA 4.0
- `sources/ref/`의 목록은 같은 라이선스(CC BY-SA 4.0)를 따릅니다
