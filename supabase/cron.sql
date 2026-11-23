-- 말모이 듀오 — 매시 정각에 알림 함수를 깨우는 스케줄 (pg_cron + pg_net)
-- 아래 두 군데를 바꿔서 SQL Editor에서 Run:
--   <PROJECT_URL>   예) https://xxxx.supabase.co
--   <CRON_SECRET>   Edge Function Secrets에 넣은 CRON_SECRET과 같은 값
create extension if not exists pg_cron;
create extension if not exists pg_net;

select cron.schedule(
  'malmoi-push-hourly',
  '0 * * * *',
  $$ select net.http_post(
       url     := '<PROJECT_URL>/functions/v1/send-push',
       headers := '{"Content-Type":"application/json","x-cron-secret":"<CRON_SECRET>"}'::jsonb,
       body    := '{}'::jsonb
     ) $$
);
-- 끄려면: select cron.unschedule('malmoi-push-hourly');
