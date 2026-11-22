# 말모이 듀오 — 베트남어·영어 회화 연습 PWA

혼자 쓰는 회화 연습 앱. 베트남어(북부 표준) 2,100문장·단어 2,876개, 영어 668문장·표현 749개.
상황 25개(영어는 15개) × 레벨 4단계(기초~고급), 카드(간격 반복)·퀴즈 4종·듣기·말하기·사전.

## 폴더 구조
```
content/     문장 원본 (vi_*.txt, en_*.txt) ← 문장 추가·수정은 여기서
src/         앱 소스 (app.html, sw.js, manifest.json, icons/)
build.py     content + src → dist 생성
dist/        배포되는 결과물 (Vercel이 이 폴더를 서비스)
vercel.json  Vercel 설정 (빌드 없이 dist 배포)
```

## 수정 → 배포
```
python3 build.py      # dist/ 갱신
git add -A && git commit -m "변경 내용" && git push
```
push하면 Vercel이 자동으로 배포합니다 (보통 1분 이내).

## 문장 형식
```
@food                                  ← 상황 카테고리
레벨|한국어|원어|단어=뜻; 단어=뜻|메모(선택)
2|포장해 주세요.|Cho tôi mang về.|mang về=가지고 가다
```
- 카테고리: greet daily food shop move stay time phone work social health travel trouble opinion life
  cook hobby biz home money tech nature culture family study (현재 베트남어 전용)
- 메모 칸에 연결 문형을 적어 두면 카드 뒷면에 표시됨 (예: vì A nên B = A 때문에 B)
- 레벨: 1 기초 · 2 초중급 · 3 중급 · 4 고급
- 진도는 원어 문장 기준 ID로 저장 → 순서를 바꾸거나 추가해도 기존 진도 유지 (원어를 고친 문장만 새 카드)
- 단어장은 단어 풀이에서 자동 생성

## 음성
- 발음: 기기 내장 TTS. 베트남어 음성이 없으면 재생하지 않고 설치 안내 (갤럭시: 설정 → 일반 → 텍스트 음성 변환)
- 말하기: 브라우저 음성 인식 — Chrome 권장, 마이크 허용 필요
- 진도는 그 기기 브라우저에만 저장 → 설정 → 백업
