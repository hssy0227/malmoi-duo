// 말모이 듀오 — 학습 알림 발송 (매시 정각 pg_cron이 호출)
// 필요한 Secrets: VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_SUBJECT, CRON_SECRET
// (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY 는 Supabase가 자동 제공)
// 배포 시 "Verify JWT"는 끕니다 — 대신 x-cron-secret 헤더로 호출자를 확인합니다.
import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";

const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
webpush.setVapidDetails(
  Deno.env.get("VAPID_SUBJECT") ?? "mailto:admin@example.com",
  Deno.env.get("VAPID_PUBLIC_KEY")!,
  Deno.env.get("VAPID_PRIVATE_KEY")!,
);

const DAY = 86400000;
const toDay = (s: string) => Date.parse(s + "T00:00:00Z");

Deno.serve(async (req) => {
  if (req.headers.get("x-cron-secret") !== Deno.env.get("CRON_SECRET")) {
    return new Response("forbidden", { status: 403 });
  }
  let body: { test?: boolean } = {};
  try { body = await req.json(); } catch (_) { /* 본문 없음 */ }

  const kst = new Date(Date.now() + 9 * 3600e3);        // 한국 시간
  const hour = kst.getUTCHours(), dow = kst.getUTCDay();
  const today = kst.toISOString().slice(0, 10);

  let q = sb.from("push_subs").select("*").eq("enabled", true);
  if (!body.test) q = q.eq("hour", hour);
  const { data: rows, error } = await q;
  if (error) return new Response(error.message, { status: 500 });

  const due = (rows ?? []).filter((r) => {
    if (body.test) return true;
    if (r.last_sent === today) return false;
    if (r.mode === "daily") return true;
    if (r.mode === "alt") return !r.last_sent || (toDay(today) - toDay(r.last_sent)) / DAY >= 2;
    if (r.mode === "week") return (r.days ?? []).includes(dow);
    return false;
  });

  const payload = JSON.stringify({
    title: "말모이 듀오",
    body: "오늘의 학습을 시작해 볼까요? 카드 몇 장만 넘겨 봐요.",
    url: "./#cards",
  });

  let sent = 0, gone = 0, failed = 0;
  await Promise.all(due.map(async (r) => {
    try {
      await webpush.sendNotification(
        { endpoint: r.endpoint, keys: { p256dh: r.p256dh, auth: r.auth } },
        payload,
        { TTL: 6 * 3600 },
      );
      sent++;
      if (!body.test) await sb.from("push_subs").update({ last_sent: today }).eq("endpoint", r.endpoint);
    } catch (e) {
      const st = (e as { statusCode?: number }).statusCode;
      if (st === 404 || st === 410) { gone++; await sb.from("push_subs").delete().eq("endpoint", r.endpoint); }
      else { failed++; console.error("push 실패", st, (e as Error).message); }
    }
  }));

  return Response.json({ kst: `${today} ${hour}시`, due: due.length, sent, gone, failed });
});
