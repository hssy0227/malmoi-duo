-- 말모이 듀오 — 학습 알림(웹 푸시) 테이블
-- Supabase → SQL Editor에 붙여 넣고 Run (여러 번 실행해도 안전)

create table if not exists public.push_subs (
  endpoint   text primary key,                       -- 기기(브라우저)별 푸시 주소
  user_id    uuid not null references auth.users(id) on delete cascade,
  p256dh     text not null,
  auth       text not null,
  mode       text not null default 'daily' check (mode in ('daily', 'alt', 'week')),   -- 매일 / 격일 / 매주 요일
  days       smallint[] not null default '{1,2,3,4,5}',   -- 0=일 … 6=토 (mode=week일 때)
  hour       smallint not null default 21 check (hour between 0 and 23),                -- 한국 시간 시각
  enabled    boolean not null default true,
  last_sent  date,                                   -- 마지막으로 보낸 날(KST) — 격일 계산·중복 방지
  updated_at timestamptz not null default now()
);
create index if not exists push_subs_hour_idx on public.push_subs (hour) where enabled;

alter table public.push_subs enable row level security;

drop policy if exists push_subs_own on public.push_subs;
create policy push_subs_own on public.push_subs
  for all to authenticated
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

grant select, insert, update, delete on public.push_subs to authenticated;
grant all on public.push_subs to service_role;
