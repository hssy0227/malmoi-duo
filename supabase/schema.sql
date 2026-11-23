-- 말모이 듀오 — Supabase 스키마
-- Supabase 대시보드 → SQL Editor → 이 파일 전체를 붙여 넣고 Run (여러 번 실행해도 안전)

-- ───────── 기준 테이블: 레벨(CEFR 매핑) · 상황 ─────────
create table if not exists public.levels (
  lv      smallint primary key,
  cefr    text not null,
  name_ko text not null,
  label   text generated always as ('Lv' || lv || ' · CEFR ' || cefr) stored
);
insert into public.levels (lv, cefr, name_ko) values
  (1, 'A1', '기초'), (2, 'A2', '초급'), (3, 'B1', '중급'), (4, 'B2', '중상급'), (5, 'C1', '고급')
on conflict (lv) do update set cefr = excluded.cefr, name_ko = excluded.name_ko;

create table if not exists public.categories (
  key     text primary key,
  name_ko text not null,
  sort    smallint not null default 0
);

create table if not exists public.sources (      -- 출처: 사전 범례 (G 일반, TE 토익, TF 토플, Biz 비즈니스 …)
  key     text primary key,
  name_ko text not null,
  how     text,                                   -- 어떻게 가져왔는지
  sort    smallint not null default 0
);

-- ───────── 학습 항목 (문장·단어) — GitHub Actions가 content/에서 자동 동기화 ─────────
create table if not exists public.items (
  lang      text not null check (lang in ('vi', 'en')),
  item_id   text not null,
  kind      text not null check (kind in ('s', 'w')),       -- s=문장, w=단어
  lv        smallint not null references public.levels (lv),
  cat       text references public.categories (key),
  ko        text not null,
  target    text not null,
  gloss     text,
  note      text,
  source    text,                                             -- content 파일명
  src       text,                                             -- 출처 키 (단어는 쉼표로 여러 개)
  active    boolean not null default true,                    -- 원본에서 빠지면 false
  synced_at timestamptz not null default now(),
  primary key (lang, item_id)
);
alter table public.items add column if not exists src text;
create index if not exists items_lv_idx on public.items (lang, lv);

-- ───────── 사용자별 학습 상태 ─────────
create table if not exists public.progress (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  lang       text not null check (lang in ('vi', 'en')),
  item_id    text not null,
  status     text not null default 'new'
             check (status in ('new', 'seen', 'learning', 'known', 'skip')),
  star       boolean not null default false,
  reps       int,          -- 간격 반복: 연속 성공 횟수
  ease       real,         -- 간격 반복: 난이도 계수
  ivl        real,         -- 간격 반복: 복습 간격(일)
  due_at     bigint,       -- 다음 복습 시각(ms)
  lapses     int,
  last_at    bigint,       -- 마지막 복습 시각(ms)
  quiz_ok    int not null default 0,
  quiz_ng    int not null default 0,
  speak_best smallint,
  seen_at    bigint,
  updated_at bigint not null,                 -- 기기에서 바뀐 시각(ms) — 충돌 시 최신 우선
  server_at  timestamptz not null default now(),  -- 서버 반영 시각 — 증분 내려받기 기준
  primary key (user_id, lang, item_id)
);
create index if not exists progress_pull_idx on public.progress (user_id, server_at);

create table if not exists public.user_state (     -- 설정·학습 범위·일별 기록
  user_id    uuid primary key default auth.uid() references auth.users (id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at bigint not null,
  server_at  timestamptz not null default now()
);

create or replace function public.touch_server_at() returns trigger
language plpgsql as $$ begin new.server_at := now(); return new; end $$;
drop trigger if exists progress_touch on public.progress;
create trigger progress_touch before insert or update on public.progress
  for each row execute function public.touch_server_at();
drop trigger if exists user_state_touch on public.user_state;
create trigger user_state_touch before insert or update on public.user_state
  for each row execute function public.touch_server_at();

-- ───────── 휴면 방지 (GitHub Actions가 주 1회 호출) ─────────
create table if not exists public.heartbeat (
  id int primary key,
  at timestamptz not null default now(),
  n  bigint not null default 0
);
insert into public.heartbeat (id) values (1) on conflict do nothing;
create or replace function public.keepalive() returns timestamptz
language sql security definer set search_path = public as $$
  update public.heartbeat set at = now(), n = n + 1 where id = 1 returning at
$$;
revoke all on function public.keepalive() from public;
grant execute on function public.keepalive() to anon, authenticated;

-- ───────── 조회용 뷰 (대시보드에서 'CEFR B1 / Lv3' 형태로 보기) ─────────
drop view if exists public.items_view;
create view public.items_view with (security_invoker = true) as
select i.lang, i.item_id, i.kind, i.lv, l.cefr, l.label as level_label,
       i.cat, c.name_ko as cat_name, i.src, i.ko, i.target, i.gloss, i.note, i.source, i.active
from public.items i
left join public.levels l on l.lv = i.lv
left join public.categories c on c.key = i.cat;

drop view if exists public.progress_view;
create view public.progress_view with (security_invoker = true) as
select p.*, i.kind, i.lv, l.cefr, l.label as level_label, i.cat, c.name_ko as cat_name, i.ko, i.target
from public.progress p
left join public.items i on i.lang = p.lang and i.item_id = p.item_id
left join public.levels l on l.lv = i.lv
left join public.categories c on c.key = i.cat;

-- ───────── 접근 권한 (RLS) ─────────
alter table public.levels     enable row level security;
alter table public.categories enable row level security;
alter table public.sources    enable row level security;
alter table public.items      enable row level security;
alter table public.progress   enable row level security;
alter table public.user_state enable row level security;
alter table public.heartbeat  enable row level security;   -- 정책 없음: keepalive() 함수로만 갱신

drop policy if exists "read levels" on public.levels;
create policy "read levels" on public.levels for select to anon, authenticated using (true);
drop policy if exists "read categories" on public.categories;
create policy "read categories" on public.categories for select to anon, authenticated using (true);
drop policy if exists "read sources" on public.sources;
create policy "read sources" on public.sources for select to anon, authenticated using (true);
drop policy if exists "read items" on public.items;
create policy "read items" on public.items for select to anon, authenticated using (true);

drop policy if exists "own progress" on public.progress;
create policy "own progress" on public.progress for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
drop policy if exists "own state" on public.user_state;
create policy "own state" on public.user_state for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

-- Data API 노출 권한 (2026-05-30 이후 생성된 프로젝트는 명시적 grant 필요)
grant usage on schema public to anon, authenticated, service_role;
grant select on public.levels, public.categories, public.sources, public.items, public.items_view to anon, authenticated;
grant select, insert, update, delete on public.progress, public.user_state to authenticated;
grant select on public.progress_view to authenticated;
grant all on public.levels, public.categories, public.sources, public.items to service_role;
