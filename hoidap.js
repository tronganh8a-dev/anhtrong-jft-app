// Hỏi đáp AI (Gemini) — POST /api/hoi {q, h:[{r:'u'|'m',t}]} → {a}
// Tiết kiệm token: lời dặn ngắn, chỉ gửi 4 lượt gần nhất, giới hạn độ dài, tắt "thinking", cache câu trùng, 30 câu/ngày/tài khoản.
const SYS = 'Bạn là trợ giảng của lớp "Anh Trọng Dạy JFT" (luyện thi JFT-Basic, giáo trình いろどり). Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu, có ví dụ tiếng Nhật kèm cách đọc. Giải thích chữ Hán thì kèm âm Hán Việt. Chỉ trả lời về tiếng Nhật, JFT, cuộc sống/làm việc ở Nhật; câu ngoài lề thì từ chối lịch sự.';
const LIMIT = 30, MAXQ = 600;
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } });
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
export async function hoi(req, env, user) {
  if (req.method !== 'POST') return J({ e: 'POST' }, 405);
  if (!env.GEMINI_KEY) return J({ e: 'Chưa cài GEMINI_KEY trên Cloudflare.' }, 500);
  let b; try { b = await req.json(); } catch { return J({ e: 'Dữ liệu không hợp lệ' }, 400); }
  const q0 = String(b.q || '').trim().slice(0, MAXQ);
  const ctx = String(b.ctx || '').slice(0, 1200);
  const q = ctx ? `${ctx}\n\nCâu hỏi của học viên: ${q0}` : q0;
  if (!q0) return J({ e: 'Bạn chưa nhập câu hỏi.' }, 400);
  const h = (Array.isArray(b.h) ? b.h : []).slice(-4).map(x => ({ role: x.r === 'm' ? 'model' : 'user', parts: [{ text: String(x.t || '').slice(0, 800) }] }));
  const cache = caches.default, origin = new URL(req.url).origin;
  // câu hỏi trùng (không kèm lịch sử) → lấy lại câu trả lời cũ, không tốn token
  const ck = new Request(`${origin}/__hoi/${await sha(q.toLowerCase())}`);
  if (!h.length) { const c = await cache.match(ck); if (c) return J({ a: await c.text(), cached: 1 }); }
  // giới hạn mỗi ngày
  const day = new Date(Date.now() + 9 * 36e5).toISOString().slice(0, 10);
  const rk = new Request(`${origin}/__hoi_rate/${encodeURIComponent(user)}/${day}`);
  const used = Number(await (await cache.match(rk))?.text() || 0);
  if (used >= LIMIT) return J({ e: `Hôm nay bạn đã hỏi ${LIMIT} câu. Mai hỏi tiếp nhé!` }, 429);
  const body = { system_instruction: { parts: [{ text: SYS }] }, contents: [...h, { role: 'user', parts: [{ text: q }] }],
    generationConfig: { maxOutputTokens: 700, temperature: 0.4, thinkingConfig: { thinkingBudget: 0 } } };
  let a = '', err = '';
  for (const m of [env.GEMINI_MODEL, 'gemini-flash-lite-latest', 'gemini-2.5-flash-lite'].filter(Boolean)) {
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': env.GEMINI_KEY }, body: JSON.stringify(body) });
    const d = await r.json().catch(() => ({}));
    if (r.ok) { a = (d.candidates?.[0]?.content?.parts || []).map(p => p.text || '').join('').trim(); break; }
    err = d.error?.message || r.status;
    if (r.status !== 404 && r.status !== 400) break;
  }
  if (!a) return J({ e: 'AI đang bận, bạn thử lại sau nhé.' + (err ? ` (${String(err).slice(0, 120)})` : '') }, 502);
  await cache.put(rk, new Response(String(used + 1), { headers: { 'Cache-Control': 'max-age=90000' } }));
  if (!h.length) await cache.put(ck, new Response(a, { headers: { 'Cache-Control': 'max-age=604800' } }));
  return J({ a, left: LIMIT - used - 1 });
}
