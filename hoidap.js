// Hỏi đáp AI (Gemini) — POST /api/hoi {q, h:[{r:'u'|'m',t}]} → {a}
// Tiết kiệm token: lời dặn ngắn, chỉ gửi 4 lượt gần nhất, giới hạn độ dài, tắt "thinking", cache câu trùng, 30 câu/ngày/tài khoản.
const SYS = 'Bạn là trợ giảng của lớp "Anh Trọng Dạy JFT" (luyện thi JFT-Basic, giáo trình いろどり). Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu, có ví dụ tiếng Nhật kèm cách đọc. Giải thích chữ Hán thì kèm âm Hán Việt. Chỉ trả lời về tiếng Nhật, JFT, cuộc sống/làm việc ở Nhật; câu ngoài lề thì từ chối lịch sự.';
const LIMIT = Number(globalThis.HOI_LIMIT || 100), ALL = 900, MAXQ = 600; // ALL: tổng cả lớp/ngày, dưới hạn mức miễn phí ~1000 lượt/ngày của Flash-Lite
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
  const gk = new Request(`${origin}/__hoi_all/${day}`);
  const all = Number(await (await cache.match(gk))?.text() || 0);
  if (all >= ALL) return J({ e: 'Hôm nay cả lớp đã dùng hết lượt hỏi miễn phí. Mai hỏi tiếp nhé!' }, 429);
  if (used >= LIMIT) return J({ e: `Hôm nay bạn đã hỏi ${LIMIT} câu. Mai hỏi tiếp nhé!` }, 429);
  const body = { system_instruction: { parts: [{ text: SYS }] }, contents: [...h, { role: 'user', parts: [{ text: q }] }],
    generationConfig: { maxOutputTokens: 700, temperature: 0.4, thinkingConfig: { thinkingBudget: 0 } } };
  let a = '', err = '';
  const call = async (m, cfg) => {
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': env.GEMINI_KEY }, body: JSON.stringify({ ...body, generationConfig: cfg }) });
    const d = await r.json().catch(() => ({}));
    return r.ok ? { a: (d.candidates?.[0]?.content?.parts || []).filter(p => !p.thought).map(p => p.text || '').join('').trim() } : { e: d.error?.message || String(r.status) };
  };
  const tryModel = async m => {
    let x = await call(m, body.generationConfig);
    if (x.e && /thinking/i.test(x.e)) x = await call(m, { maxOutputTokens: 700, temperature: 0.4 });
    return x;
  };
  // model đã chọn được lần trước (lưu 1 ngày) → model khai báo → tự dò danh sách model của khoá
  const mk = new Request(`${origin}/__hoi_model`);
  const saved = await (await cache.match(mk))?.text();
  const tried = new Set();
  for (const m of [saved, env.GEMINI_MODEL, 'gemini-flash-lite-latest'].filter(Boolean)) {
    if (tried.has(m)) continue; tried.add(m);
    const x = await tryModel(m); if (x.a) { a = x.a; if (m !== saved) await cache.put(mk, new Response(m, { headers: { 'Cache-Control': 'max-age=86400' } })); break; } err = x.e;
  }
  if (!a) {
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', { headers: { 'x-goog-api-key': env.GEMINI_KEY } });
    const L = ((await r.json().catch(() => ({}))).models || []).filter(x => (x.supportedGenerationMethods || []).includes('generateContent')).map(x => x.name.replace('models/', ''));
    const score = n => (/flash-lite/.test(n) ? 0 : /flash/.test(n) ? 100 : 1000) + (/preview|exp|tts|image|audio|live|embed/.test(n) ? 50 : 0) - (parseFloat((n.match(/gemini-(\d+(?:\.\d+)?)/) || [0, 0])[1]) || 0);
    for (const m of L.filter(n => /^gemini/.test(n) && !/tts|image|audio|live|embed/.test(n)).sort((x, y) => score(x) - score(y)).slice(0, 4)) {
      if (tried.has(m)) continue; tried.add(m);
      const x = await tryModel(m); if (x.a) { a = x.a; await cache.put(mk, new Response(m, { headers: { 'Cache-Control': 'max-age=86400' } })); break; } err = x.e;
    }
  }
  if (!a) return J({ e: 'AI đang bận, bạn thử lại sau nhé.' + (err ? ` (${String(err).slice(0, 120)})` : '') }, 502);
  await cache.put(gk, new Response(String(all + 1), { headers: { 'Cache-Control': 'max-age=90000' } }));
  await cache.put(rk, new Response(String(used + 1), { headers: { 'Cache-Control': 'max-age=90000' } }));
  if (!h.length) await cache.put(ck, new Response(a, { headers: { 'Cache-Control': 'max-age=604800' } }));
  return J({ a, left: LIMIT - used - 1 });
}
