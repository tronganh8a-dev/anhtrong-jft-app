// Bài kiểm tra theo buổi: học sinh làm qua link công khai /kiemtra/<id> (không cần đăng nhập),
// bấm Nộp → máy chủ chấm theo đáp án trong kiemtra/<id>.json (không nằm trong public/) và lưu vào
// Durable Object "KiemTra" (SQLite). Giáo viên xem kết quả ở /kiemtra/ketqua (phải đăng nhập;
// nếu đặt biến môi trường GIAOVIEN = "ten1,ten2" thì chỉ các tài khoản đó xem được).
import { DurableObject } from 'cloudflare:workers';
import TESTS from './kiemtra/tests.js';
import { currentUser } from './auth.js';

export class KiemTra extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec(`CREATE TABLE IF NOT EXISTS sub(id INTEGER PRIMARY KEY AUTOINCREMENT, test TEXT, name TEXT, score INTEGER, total INTEGER, secs TEXT, ans TEXT, dur INTEGER, ts INTEGER)`);
  }
  add(r) {
    this.sql.exec('INSERT INTO sub(test,name,score,total,secs,ans,dur,ts) VALUES (?,?,?,?,?,?,?,?)', r.test, r.name, r.score, r.total, JSON.stringify(r.secs), JSON.stringify(r.ans), r.dur, r.ts);
    return true;
  }
  list(test) { return this.sql.exec('SELECT * FROM sub WHERE test=? ORDER BY id DESC LIMIT 2000', test).toArray(); }
  counts() { return this.sql.exec('SELECT test, COUNT(*) AS n FROM sub GROUP BY test').toArray(); }
  del(id) { this.sql.exec('DELETE FROM sub WHERE id=?', id); return true; }
}
const db = env => env.KT.get(env.KT.idFromName('main'));
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } });
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export const isPublic = p => p === '/api/kiemtra/nop' || (p.startsWith('/kiemtra/') && !p.startsWith('/kiemtra/ketqua'));

export async function kiemtraPublic(req, env) {
  const url = new URL(req.url);
  if (url.pathname === '/api/kiemtra/nop') {
    if (req.method !== 'POST') return J({ ok: false, error: 'Sai phương thức' }, 405);
    const raw = await req.text();
    if (raw.length > 20000) return J({ ok: false, error: 'Dữ liệu quá lớn' }, 413);
    let b; try { b = JSON.parse(raw); } catch { return J({ ok: false, error: 'Dữ liệu không hợp lệ' }, 400); }
    const T = TESTS[b && b.test];
    if (!T) return J({ ok: false, error: 'Không tìm thấy bài kiểm tra' }, 404);
    const name = String(b.name || '').replace(/\s+/g, ' ').trim().slice(0, 60);
    if (name.length < 2) return J({ ok: false, error: 'Thiếu họ tên' }, 400);
    const N = T.key.length;
    if (!Array.isArray(b.ans) || b.ans.length !== N) return J({ ok: false, error: 'Bài làm không đúng số câu' }, 400);
    const ans = b.ans.map(x => (Number.isInteger(x) && x >= 0 && x < 6 ? x : -1));
    let score = 0, k = 0;
    const secs = T.secs.map(s => { let c = 0; for (let i = 0; i < s.n; i++, k++) if (ans[k] === T.key[k].a) c++; score += c; return { name: s.name, c, n: s.n }; });
    const dur = Math.max(0, Math.min(86400, Number(b.dur) | 0));
    try { await db(env).add({ test: b.test, name, score, total: N, secs, ans, dur, ts: Date.now() }); }
    catch (e) { return J({ ok: false, error: 'Máy chủ chưa lưu được bài, thử lại sau ít phút' }, 503); }
    return J({ ok: true, score, total: N, secs, key: T.key });
  }
  const res = await env.ASSETS.fetch(req);
  const out = new Response(res.body, res);
  out.headers.set('Cache-Control', 'no-cache');
  out.headers.set('X-Robots-Tag', 'noindex');
  return out;
}

const jst = ts => new Date(ts + 9 * 3600e3).toISOString().slice(0, 16).replace('T', ' ');
const mmss = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

export async function ketqua(req, env) {
  const url = new URL(req.url);
  const user = await currentUser(req, env);
  const allow = String(env.GIAOVIEN || '').split(/[\s,;]+/).map(x => x.trim().toLowerCase()).filter(Boolean);
  if (!user || (allow.length && !allow.includes(user))) return new Response('Chỉ giáo viên được xem kết quả.', { status: 403, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  const ids = Object.keys(TESTS);
  if (req.method === 'POST' && url.pathname === '/kiemtra/ketqua/xoa') {
    const f = await req.formData();
    await db(env).del(Number(f.get('id')) || 0);
    return Response.redirect(`${url.origin}/kiemtra/ketqua?t=${encodeURIComponent(f.get('t') || '')}`, 303);
  }
  const t = ids.includes(url.searchParams.get('t')) ? url.searchParams.get('t') : ids[ids.length - 1];
  const T = TESTS[t];
  const rows = (await db(env).list(t)).map(r => ({ ...r, secs: JSON.parse(r.secs), ans: JSON.parse(r.ans) }));
  if (url.pathname === '/kiemtra/ketqua.csv') {
    const head = ['Thời gian (JST)', 'Họ tên', 'Điểm', 'Tổng', ...T.secs.map(s => s.name), 'Thời gian làm', ...T.key.map((_, i) => 'C' + (i + 1))];
    const lines = [head, ...rows.map(r => [jst(r.ts), r.name, r.score, r.total, ...r.secs.map(s => `${s.c}/${s.n}`), mmss(r.dur), ...r.ans.map((a, i) => (a < 0 ? '' : a === T.key[i].a ? '1' : '0'))])];
    const csv = '﻿' + lines.map(l => l.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')).join('\r\n');
    return new Response(csv, { headers: { 'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': `attachment; filename="ketqua_${t}.csv"`, 'Cache-Control': 'no-store' } });
  }
  const n = rows.length, avg = n ? (rows.reduce((a, r) => a + r.score, 0) / n).toFixed(1) : '–';
  const rate = T.key.map((k, i) => n ? Math.round(rows.filter(r => r.ans[i] === k.a).length / n * 100) : null);
  let qi = 0;
  const qtab = T.secs.map(s => `<h3>${esc(s.name)}</h3><div class="qr">${Array.from({ length: s.n }, () => { const i = qi++; const v = rate[i]; return `<div class="${v == null ? '' : v < 50 ? 'lo' : v < 75 ? 'mid' : 'hi'}" title="${esc(T.qs[i])}"><b>Câu ${i + 1}</b><span>${v == null ? '–' : v + '%'}</span><small>${esc(T.qs[i])}</small></div>`; }).join('')}</div>`).join('');
  const body = rows.map(r => {
    const wrong = r.ans.map((a, i) => (a === T.key[i].a ? null : i + 1)).filter(Boolean);
    return `<tr><td>${jst(r.ts)}</td><td class="nm">${esc(r.name)}</td><td class="sc">${r.score}/${r.total}</td>${r.secs.map(s => `<td>${s.c}/${s.n}</td>`).join('')}<td>${mmss(r.dur)}</td><td class="wr">${wrong.length ? wrong.join(', ') : '—'}</td>
<td><form method="post" action="/kiemtra/ketqua/xoa" onsubmit="return confirm('Xoá bài nộp của ${esc(r.name).replace(/'/g, '')}?')"><input type="hidden" name="id" value="${r.id}"><input type="hidden" name="t" value="${esc(t)}"><button title="Xoá">✕</button></form></td></tr>`;
  }).join('');
  const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kết quả kiểm tra · Anh Trọng Dạy JFT</title><link rel="icon" href="/app/media/brand/icon.svg" type="image/svg+xml"><link rel="icon" href="/app/media/brand/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/app/media/brand/apple-touch-icon.png"><meta name="robots" content="noindex">
<style>body{margin:0;font-family:"M PLUS Rounded 1c","Segoe UI",system-ui,sans-serif;background:#f3f6f8;color:#17222c}.w{max-width:1100px;margin:0 auto;padding:18px 16px 40px}
h1{font-size:22px;margin:0 0 4px}h3{margin:16px 0 6px;font-size:15px}.top{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0}
select,a.b{font:inherit;font-size:14px;padding:8px 12px;border-radius:10px;border:1.5px solid #cfd8de;background:#fff;color:#0d5a8c;text-decoration:none;font-weight:700}
.st{display:flex;gap:10px;flex-wrap:wrap}.st div{background:#fff;border:1px solid #e3e9ee;border-radius:12px;padding:10px 16px;font-size:13px;color:#5a6873}.st b{display:block;font-size:22px;color:#17222c}
.card{background:#fff;border:1px solid #e3e9ee;border-radius:14px;padding:14px;margin-top:14px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px;white-space:nowrap}th,td{padding:8px 10px;border-bottom:1px solid #edf1f4;text-align:left}th{font-size:12.5px;color:#5a6873;background:#f6f8fa}
td.nm{font-weight:700}td.sc{font-weight:800;color:#0d5a8c}td.wr{white-space:normal;color:#b3261e;font-size:13px;min-width:140px}
td button{border:0;background:none;color:#9aa6b0;cursor:pointer;font-size:15px}td button:hover{color:#b3261e}
.qr{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.qr div{border-radius:10px;padding:8px 10px;background:#f3f6f8;font-size:12.5px}
.qr b{font-size:12.5px}.qr span{float:right;font-weight:800}.qr small{display:block;color:#5a6873;margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.qr .lo{background:#fdeeee}.qr .lo span{color:#b3261e}.qr .mid{background:#fff4e0}.qr .mid span{color:#a5650b}.qr .hi{background:#ecf8f0}.qr .hi span{color:#2e8b4a}
.empty{color:#5a6873;padding:20px 4px}</style></head><body><div class="w">
<h1>Kết quả kiểm tra</h1><div style="color:#5a6873;font-size:14px">Giáo viên: ${esc(user)} · <a href="/">Về app</a></div>
<div class="top"><select onchange="location.search='?t='+this.value">${ids.map(x => `<option value="${x}"${x === t ? ' selected' : ''}>${esc(TESTS[x].title)}</option>`).join('')}</select>
<a class="b" href="/kiemtra/${t}" target="_blank">Mở link làm bài ↗</a><a class="b" href="/kiemtra/ketqua.csv?t=${t}">Tải Excel (CSV)</a><a class="b" href="?t=${t}">Tải lại</a></div>
<div class="st"><div><b>${n}</b>bài đã nộp</div><div><b>${avg}</b>điểm trung bình / ${T.key.length}</div><div><b>${n ? Math.max(...rows.map(r => r.score)) : '–'}</b>cao nhất</div></div>
<div class="card">${n ? `<table><tr><th>Nộp lúc (giờ Nhật)</th><th>Họ tên</th><th>Điểm</th>${T.secs.map(s => `<th>${esc(s.name)}</th>`).join('')}<th>Làm trong</th><th>Câu sai / bỏ trống</th><th></th></tr>${body}</table>` : '<div class="empty">Chưa có bài nộp nào.</div>'}</div>
<div class="card"><b>Tỉ lệ làm đúng từng câu</b> <span style="color:#5a6873;font-size:13px">(đỏ &lt; 50% → nên chữa lại trên lớp)</span>${qtab}</div>
</div></body></html>`;
  return new Response(html, { headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' } });
}
