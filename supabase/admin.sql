-- 말모이 듀오 — 관리자 기능: 사용 로그(events)·일별 요약(daily_stats)·관리자 조회 함수·밤 집계
-- Supabase → SQL Editor에 통째로 붙여 넣고 Run (여러 번 실행해도 안전)
-- 실행 후 맨 아래 "관리자 지정" 한 줄을 본인 이메일로 바꿔서 한 번 더 Run

-- ───────── 관리자 ─────────
create table if not exists public.admins (
  user_id  uuid primary key references auth.users (id) on delete cascade,
  added_at timestamptz not null default now()
);
alter table public.admins enable row level security;          -- 정책 없음: 앱에서 직접 못 읽음

alter table public.admins add column if not exists otp_required boolean not null default false;  -- true면 서버가 이메일 OTP로 로그인한 세션만 관리자 함수를 허용

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admins where user_id = auth.uid())
$$;
revoke all on function public.is_admin() from public;
grant execute on function public.is_admin() to authenticated;

-- 이 세션이 이메일 OTP(코드)로 인증됐는지: 로그인 토큰의 amr 기록에서 확인
create or replace function public.session_otp() returns boolean
language sql stable set search_path = public as $$
  select exists (select 1 from jsonb_array_elements(coalesce(auth.jwt() -> 'amr', '[]'::jsonb)) a where a ->> 'method' = 'otp')
$$;
grant execute on function public.session_otp() to authenticated;

create or replace function public.admin_check() returns void
language plpgsql stable security definer set search_path = public as $$
declare a public.admins;
begin
  select * into a from public.admins where user_id = auth.uid();
  if not found then
    raise exception 'admin only' using errcode = '42501';
  end if;
  if a.otp_required and not public.session_otp() then
    raise exception 'otp required' using errcode = '42501';
  end if;
end $$;
revoke all on function public.admin_check() from public;

-- 앱이 로그인 직후 묻는 함수: 관리자인지, 이 세션이 OTP 인증됐는지, 서버가 OTP를 강제하는지
create or replace function public.admin_status() returns jsonb
language sql stable security definer set search_path = public as $$
  select coalesce(
    (select jsonb_build_object('admin', true, 'otp', public.session_otp(), 'enforced', a.otp_required)
       from public.admins a where a.user_id = auth.uid()),
    jsonb_build_object('admin', false, 'otp', false, 'enforced', false))
$$;
revoke all on function public.admin_status() from public;
grant execute on function public.admin_status() to authenticated;

-- 회원 탈퇴: 본인 계정과 모든 기록(진도·설정·알림·사용 로그·일별 요약)을 삭제. 되돌릴 수 없음.
-- 관리자 계정은 탈퇴할 수 없음(마지막 관리자를 잃지 않도록): 먼저 admins에서 제거해야 함.
create or replace function public.delete_my_account() returns void
language plpgsql security definer set search_path = public, auth as $$
begin
  if auth.uid() is null then raise exception 'login required' using errcode = '42501'; end if;
  if exists (select 1 from public.admins where user_id = auth.uid()) then
    raise exception 'admin cannot leave' using errcode = '42501';
  end if;
  delete from auth.users where id = auth.uid();   -- 나머지 테이블은 on delete cascade 로 함께 삭제
end $$;
revoke all on function public.delete_my_account() from public;
grant execute on function public.delete_my_account() to authenticated;

-- 관리자 강제 탈퇴: 본인·다른 관리자 계정은 대상이 될 수 없음
create or replace function public.admin_delete_user(p_uid uuid) returns void
language plpgsql security definer set search_path = public, auth as $$
begin
  perform public.admin_check();
  if p_uid = auth.uid() then raise exception 'cannot delete self' using errcode = '42501'; end if;
  if exists (select 1 from public.admins where user_id = p_uid) then
    raise exception 'cannot delete admin' using errcode = '42501';
  end if;
  delete from auth.users where id = p_uid;
  if not found then raise exception 'no such user' using errcode = 'P0002'; end if;
end $$;
revoke all on function public.admin_delete_user(uuid) from public;
grant execute on function public.admin_delete_user(uuid) to authenticated;

-- ───────── 사용 로그 (원본, 90일 보관) ─────────
create table if not exists public.events (
  id        bigint generated always as identity primary key,
  user_id   uuid not null default auth.uid() references auth.users (id) on delete cascade,
  at        timestamptz not null,                 -- 기기에서 일어난 시각
  lang      text,                                 -- vi / en
  kind      text not null,                        -- open, view, card, quiz, speak, game, mark, err
  item_id   text,
  v         jsonb,
  ver       text,                                 -- 앱 버전
  server_at timestamptz not null default now()
);
create index if not exists events_at_idx on public.events (at);
create index if not exists events_user_at_idx on public.events (user_id, at);
create index if not exists events_kind_at_idx on public.events (kind, at);

alter table public.events enable row level security;
drop policy if exists events_insert_own on public.events;
create policy events_insert_own on public.events for insert to authenticated
  with check (user_id = (select auth.uid()));
drop policy if exists events_select_own on public.events;
create policy events_select_own on public.events for select to authenticated
  using (user_id = (select auth.uid()));
grant select, insert on public.events to authenticated;
grant all on public.events to service_role;

-- ───────── 일별 요약 (계속 보관) ─────────
create table if not exists public.daily_stats (
  d       date not null,                          -- 한국 날짜
  user_id uuid not null references auth.users (id) on delete cascade,
  lang    text not null default '',
  kind    text not null,
  n       int  not null,                          -- 건수
  ok      int  not null default 0,                -- 그중 정답(퀴즈 등)
  primary key (d, user_id, lang, kind)
);
alter table public.daily_stats enable row level security;     -- 정책 없음: 관리자 함수로만
grant all on public.daily_stats to service_role;

-- 지정한 날(한국 날짜)의 로그를 요약하고, 90일 지난 원본을 지움
create or replace function public.admin_rollup(p_day date default ((now() at time zone 'Asia/Seoul')::date - 1))
returns int language plpgsql security definer set search_path = public as $$
declare n int;
begin
  delete from public.daily_stats where d = p_day;
  insert into public.daily_stats (d, user_id, lang, kind, n, ok)
  select p_day, user_id, coalesce(lang, ''), kind, count(*)::int,
         (count(*) filter (where (v ->> 'ok') = 'true'))::int
  from public.events
  where (at at time zone 'Asia/Seoul')::date = p_day
  group by user_id, coalesce(lang, ''), kind;
  get diagnostics n = row_count;
  delete from public.events where at < now() - interval '90 days';
  return n;
end $$;
revoke all on function public.admin_rollup(date) from public;

-- ───────── 관리자 조회 함수 (관리자 계정만, 읽기 전용) ─────────
-- p_self=false 이면 관리자 본인 기록을 뺌

-- 사용자 목록 + 계정별 요약
create or replace function public.admin_users(p_days int default 30, p_self boolean default true)
returns jsonb language plpgsql stable security definer set search_path = public, auth as $$
declare r jsonb;
begin
  perform public.admin_check();
  select coalesce(jsonb_agg(x order by x ->> 'last' desc nulls last), '[]'::jsonb) into r from (
    select jsonb_build_object(
      'id', u.id, 'email', u.email, 'created', u.created_at, 'signin', u.last_sign_in_at,
      'me', u.id = auth.uid(),
      'admin', exists (select 1 from public.admins a where a.user_id = u.id),
      'last', greatest(u.last_sign_in_at, (select max(e.at) from public.events e where e.user_id = u.id), s.server_at),
      'hist', coalesce(s.data -> 'hist', '{}'::jsonb),
      'game', coalesce(s.data -> 'game', '{}'::jsonb),
      'notif', exists (select 1 from public.push_subs p where p.user_id = u.id and p.enabled),
      'kinds', (select coalesce(jsonb_object_agg(k.kind, k.n), '{}'::jsonb) from (
                 select e.kind, count(*) n from public.events e
                 where e.user_id = u.id and e.at > now() - make_interval(days => p_days) group by e.kind) k),
      'langs', (select coalesce(jsonb_object_agg(k.lang, k.n), '{}'::jsonb) from (
                 select e.lang, count(*) n from public.events e
                 where e.user_id = u.id and e.lang is not null and e.kind in ('card','quiz','speak','game')
                   and e.at > now() - make_interval(days => p_days) group by e.lang) k),
      'prog', (select coalesce(jsonb_object_agg(k.lang, k.o), '{}'::jsonb) from (
                 select pr.lang, jsonb_build_object(
                   'known', count(*) filter (where pr.status = 'known'),
                   'skip',  count(*) filter (where pr.status = 'skip'),
                   'learn', count(*) filter (where pr.reps is not null and pr.status not in ('known','skip')),
                   'due',   count(*) filter (where pr.due_at is not null and pr.due_at < (extract(epoch from now()) * 1000)::bigint and pr.status not in ('known','skip')),
                   'qok', coalesce(sum(pr.quiz_ok), 0), 'qng', coalesce(sum(pr.quiz_ng), 0),
                   'sp', round(avg(pr.speak_best))) o
                 from public.progress pr where pr.user_id = u.id group by pr.lang) k)
    ) x
    from auth.users u
    left join public.user_state s on s.user_id = u.id
    where p_self or u.id <> auth.uid()
  ) t;
  return r;
end $$;

-- 일별 추이: 학습량·활성 계정(기존 user_state.hist 기준) + 기능·언어별 건수(events 기준)
create or replace function public.admin_daily(p_days int default 30, p_self boolean default true)
returns jsonb language plpgsql stable security definer set search_path = public as $$
declare r jsonb; d0 date := (now() at time zone 'Asia/Seoul')::date - (p_days - 1);
begin
  perform public.admin_check();
  with h as (
    select h.key::date d, s.user_id, h.value::numeric n
    from public.user_state s, jsonb_each_text(coalesce(s.data -> 'hist', '{}'::jsonb)) h
    where h.key ~ '^\d{4}-\d{2}-\d{2}$' and h.key::date >= d0 and (p_self or s.user_id <> auth.uid())
  ), e as (
    select (e.at at time zone 'Asia/Seoul')::date d, e.user_id, e.kind, e.lang
    from public.events e
    where e.at >= (d0::timestamp at time zone 'Asia/Seoul') and (p_self or e.user_id <> auth.uid())
  ), days as (select generate_series(d0, d0 + (p_days - 1), interval '1 day')::date d)
  select coalesce(jsonb_agg(jsonb_build_object(
      'd', days.d,
      'study', (select coalesce(sum(n), 0) from h where h.d = days.d),
      'users', (select count(distinct user_id) from (select user_id from h where h.d = days.d and h.n > 0
                                                     union select user_id from e where e.d = days.d) a),
      'kinds', (select coalesce(jsonb_object_agg(kind, n), '{}'::jsonb) from (select kind, count(*) n from e where e.d = days.d group by kind) k),
      'langs', (select coalesce(jsonb_object_agg(lang, n), '{}'::jsonb) from (select lang, count(*) n from e where e.d = days.d and lang is not null and kind in ('card','quiz','speak','game') group by lang) k)
    ) order by days.d), '[]'::jsonb) into r
  from days;
  return r;
end $$;

-- 한 계정 상세
create or replace function public.admin_user(p_uid uuid)
returns jsonb language plpgsql stable security definer set search_path = public, auth as $$
declare r jsonb;
begin
  perform public.admin_check();
  select jsonb_build_object(
    'id', u.id, 'email', u.email, 'created', u.created_at, 'signin', u.last_sign_in_at,
    'state', coalesce(s.data, '{}'::jsonb) - 'scope',
    'push', (select coalesce(jsonb_agg(jsonb_build_object('mode', p.mode, 'days', p.days, 'hour', p.hour, 'enabled', p.enabled, 'last', p.last_sent)), '[]'::jsonb)
             from public.push_subs p where p.user_id = u.id),
    'prog', (select coalesce(jsonb_object_agg(k.lang, k.o), '{}'::jsonb) from (
               select pr.lang, jsonb_build_object(
                 'known', count(*) filter (where pr.status = 'known'),
                 'skip',  count(*) filter (where pr.status = 'skip'),
                 'learn', count(*) filter (where pr.reps is not null and pr.status not in ('known','skip')),
                 'seen',  count(*) filter (where pr.seen_at is not null),
                 'due',   count(*) filter (where pr.due_at is not null and pr.due_at < (extract(epoch from now()) * 1000)::bigint and pr.status not in ('known','skip')),
                 'qok', coalesce(sum(pr.quiz_ok), 0), 'qng', coalesce(sum(pr.quiz_ng), 0),
                 'sp', round(avg(pr.speak_best))) o
               from public.progress pr where pr.user_id = u.id group by pr.lang) k),
    'wrong', (select coalesce(jsonb_agg(jsonb_build_object('lang', w.lang, 'id', w.item_id, 'ok', w.quiz_ok, 'ng', w.quiz_ng) order by w.quiz_ng desc, w.quiz_ok), '[]'::jsonb)
              from (select * from public.progress pr where pr.user_id = u.id and pr.quiz_ng > 0 order by pr.quiz_ng desc, pr.quiz_ok limit 10) w),
    'kinds', (select coalesce(jsonb_agg(jsonb_build_object('d', k.d, 'kind', k.kind, 'n', k.n)), '[]'::jsonb) from (
               select (e.at at time zone 'Asia/Seoul')::date d, e.kind, count(*) n from public.events e
               where e.user_id = u.id and e.at > now() - interval '30 days' and e.kind in ('card','quiz','speak','game')
               group by 1, 2) k),
    'recent', (select coalesce(jsonb_agg(jsonb_build_object('at', e.at, 'kind', e.kind, 'lang', e.lang, 'id', e.item_id, 'v', e.v, 'ver', e.ver) order by e.at desc), '[]'::jsonb)
               from (select * from public.events e where e.user_id = u.id order by e.at desc limit 50) e),
    'device', (select e.v from public.events e where e.user_id = u.id and e.kind = 'open' order by e.at desc limit 1),
    'ver', (select e.ver from public.events e where e.user_id = u.id and e.ver is not null order by e.at desc limit 1)
  ) into r
  from auth.users u left join public.user_state s on s.user_id = u.id
  where u.id = p_uid;
  return r;
end $$;

-- 콘텐츠: 항목별 누적(정답·오답·스킵·앎·학습 계정 수). 문장 내용·레벨·상황은 앱 데이터로 붙임
create or replace function public.admin_content(p_self boolean default true)
returns jsonb language plpgsql stable security definer set search_path = public as $$
declare r jsonb;
begin
  perform public.admin_check();
  select coalesce(jsonb_agg(jsonb_build_array(lang, item_id, users, ok, ng, skip, known)), '[]'::jsonb) into r from (
    select pr.lang, pr.item_id, count(*) filter (where pr.reps is not null or pr.quiz_ok + pr.quiz_ng > 0 or pr.seen_at is not null) users,
           sum(pr.quiz_ok) ok, sum(pr.quiz_ng) ng,
           count(*) filter (where pr.status = 'skip') skip, count(*) filter (where pr.status = 'known') known
    from public.progress pr
    where p_self or pr.user_id <> auth.uid()
    group by pr.lang, pr.item_id
  ) t;
  return r;
end $$;

-- 게임: 계정별 최고 기록(user_state) + 기간 내 플레이 수·평균(events)
create or replace function public.admin_games(p_days int default 30, p_self boolean default true)
returns jsonb language plpgsql stable security definer set search_path = public, auth as $$
declare r jsonb;
begin
  perform public.admin_check();
  select jsonb_build_object(
    'best', (select coalesce(jsonb_agg(jsonb_build_object('id', u.id, 'email', u.email, 'game', s.data -> 'game')), '[]'::jsonb)
             from public.user_state s join auth.users u on u.id = s.user_id
             where s.data ? 'game' and (p_self or u.id <> auth.uid())),
    'plays', (select coalesce(jsonb_agg(jsonb_build_object('lang', g.lang, 'game', g.game, 'n', g.n, 'avg', g.avg, 'users', g.users)), '[]'::jsonb) from (
               select e.lang, e.v ->> 'g' game, count(*) n, round(avg((e.v ->> 'score')::numeric), 1) avg, count(distinct e.user_id) users
               from public.events e where e.kind = 'game' and e.at > now() - make_interval(days => p_days) and (p_self or e.user_id <> auth.uid())
               group by 1, 2) g),
    'missed', (select coalesce(jsonb_agg(jsonb_build_object('lang', m.lang, 't', m.t, 'n', m.n) order by m.n desc), '[]'::jsonb) from (
               select e.lang, x.t, count(*) n
               from public.events e, jsonb_array_elements_text(coalesce(e.v -> 'missed', '[]'::jsonb)) x(t)
               where e.kind = 'game' and e.v ->> 'g' = 'bomb' and e.at > now() - make_interval(days => p_days) and (p_self or e.user_id <> auth.uid())
               group by 1, 2 order by 3 desc limit 20) m)
  ) into r;
  return r;
end $$;

-- 운영: 오류, 앱 버전·기기, 알림, DB 용량, keepalive
create or replace function public.admin_ops(p_days int default 30, p_self boolean default true)
returns jsonb language plpgsql stable security definer set search_path = public, auth as $$
declare r jsonb;
begin
  perform public.admin_check();
  select jsonb_build_object(
    'errors', (select coalesce(jsonb_agg(jsonb_build_object('at', e.at, 'email', u.email, 'v', e.v, 'ver', e.ver) order by e.at desc), '[]'::jsonb)
               from (select * from public.events e where e.kind = 'err' and (p_self or e.user_id <> auth.uid()) order by e.at desc limit 50) e
               join auth.users u on u.id = e.user_id),
    'vers', (select coalesce(jsonb_object_agg(coalesce(v.ver, '?'), v.n), '{}'::jsonb) from (
               select l.ver, count(*) n from (select distinct on (e.user_id) e.user_id, e.ver from public.events e
                                              where e.at > now() - make_interval(days => p_days) and (p_self or e.user_id <> auth.uid())
                                              order by e.user_id, e.at desc) l group by l.ver) v),
    'devices', (select coalesce(jsonb_object_agg(d.k, d.n), '{}'::jsonb) from (
               select coalesce(l.v ->> 'dev', '?') || case when (l.v ->> 'pwa') = 'true' then ' · 홈 화면 앱' else ' · 브라우저' end k, count(*) n
               from (select distinct on (e.user_id) e.user_id, e.v from public.events e
                     where e.kind = 'open' and e.at > now() - make_interval(days => p_days) and (p_self or e.user_id <> auth.uid())
                     order by e.user_id, e.at desc) l group by 1) d),
    'push', jsonb_build_object(
               'subs', (select count(*) from public.push_subs),
               'enabled', (select count(*) from public.push_subs where enabled),
               'users', (select count(distinct user_id) from public.push_subs where enabled),
               'sent7', (select count(*) from public.push_subs where last_sent >= (now() at time zone 'Asia/Seoul')::date - 6),
               'opens', (select count(*) from public.events e where e.kind = 'open' and (e.v ->> 'src') = 'push' and e.at > now() - make_interval(days => p_days))),
    'opens', (select count(*) from public.events e where e.kind = 'open' and e.at > now() - make_interval(days => p_days) and (p_self or e.user_id <> auth.uid())),
    'db', jsonb_build_object(
               'size', pg_database_size(current_database()),
               'tables', (select jsonb_object_agg(c.relname, jsonb_build_object('rows', c.reltuples::bigint, 'bytes', pg_total_relation_size(c.oid)))
                          from pg_class c join pg_namespace n on n.oid = c.relnamespace
                          where n.nspname = 'public' and c.relkind = 'r')),
    'events', jsonb_build_object('n', (select count(*) from public.events), 'oldest', (select min(at) from public.events)),
    'stats', jsonb_build_object('n', (select count(*) from public.daily_stats), 'last', (select max(d) from public.daily_stats)),
    'heartbeat', (select jsonb_build_object('at', h.at, 'n', h.n) from public.heartbeat h where h.id = 1)
  ) into r;
  return r;
end $$;

revoke all on function public.admin_users(int, boolean), public.admin_daily(int, boolean), public.admin_user(uuid),
  public.admin_content(boolean), public.admin_games(int, boolean), public.admin_ops(int, boolean) from public;
grant execute on function public.admin_users(int, boolean), public.admin_daily(int, boolean), public.admin_user(uuid),
  public.admin_content(boolean), public.admin_games(int, boolean), public.admin_ops(int, boolean) to authenticated;

-- ───────── 밤 집계 (매일 00:10 KST, 늦게 올라온 로그를 위해 최근 3일 다시 계산) ─────────
create extension if not exists pg_cron;
select cron.unschedule('malmoi-admin-rollup') where exists (select 1 from cron.job where jobname = 'malmoi-admin-rollup');
select cron.schedule('malmoi-admin-rollup', '10 15 * * *',
  $$ select public.admin_rollup((now() at time zone 'Asia/Seoul')::date - g) from generate_series(1, 3) g $$);

-- ───────── 관리자 지정: 아래 이메일을 본인 로그인 이메일로 바꿔서 Run ─────────
insert into public.admins (user_id)
select id from auth.users where email = '여기에_본인_이메일'
on conflict do nothing;
