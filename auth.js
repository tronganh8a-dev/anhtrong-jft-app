// Anh Trọng Dạy JFT — đăng nhập phía máy chủ (Cloudflare Pages Functions)
// Danh sách tài khoản nằm ở biến môi trường ACCOUNTS trên Cloudflare (không nằm trong code):
//   mỗi dòng (hoặc cách nhau dấu phẩy) một tài khoản dạng  ten:matkhau
//   ví dụ:  lan:Lan2026, minh:Minh2026, hocvien:jft2026
// Muốn khoá 1 bạn: xoá dòng của bạn đó rồi Deploy lại. Đổi mật khẩu: sửa rồi Deploy lại.
// Tuỳ chọn: biến SECRET (chuỗi bất kỳ, dài) để ký cookie.

const COOKIE = 'jft_s';
const DAYS = 5; // lưu đăng nhập 5 ngày (12/11 theo yêu cầu anh)
const enc = new TextEncoder();

function accounts(env) {
  const m = new Map();
  for (const part of String(env.ACCOUNTS || '').split(/[\n,;]+/)) {
    const i = part.indexOf(':');
    if (i < 1) continue;
    const u = part.slice(0, i).trim().toLowerCase();
    const p = part.slice(i + 1).trim();
    if (u && p) m.set(u, p);
  }
  return m;
}

async function sign(env, msg) {
  const key = await crypto.subtle.importKey('raw', enc.encode(env.SECRET || 'anh-trong-day-jft'), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(msg));
  return btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/[+/=]/g, c => ({ '+': '-', '/': '_', '=': '' }[c]));
}

function getCookie(req, name) {
  const m = (req.headers.get('Cookie') || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
  return m ? decodeURIComponent(m[1]) : null;
}

// Cookie: ten|hethan|phien|chuky — "phien" đổi mỗi lần đăng nhập (1 tài khoản = 1 thiết bị)
async function session(req, env) {
  const v = getCookie(req, COOKIE);
  if (!v) return null;
  const [u, exp, sid, sig] = v.split('|');
  if (!u || !exp || !sid || !sig || Date.now() > Number(exp) || Number(exp) > Date.now() + DAYS * 864e5 + 6e4) return null; // cookie cũ hạn dài hơn → đăng nhập lại
  const pass = accounts(env).get(u);
  if (!pass) return null; // tài khoản đã bị xoá → mất quyền ngay
  return (await sign(env, `${u}|${exp}|${sid}|${pass}`)) === sig ? { u, sid } : null;
}

export async function currentUser(req, env) {
  const s = await session(req, env);
  return s ? s.u : null;
}

// ---- Giới hạn 1 thiết bị: mỗi tài khoản 1 Durable Object nhỏ giữ mã phiên mới nhất ----
// Đăng nhập máy mới → mã phiên đổi → máy cũ bị đẩy ra. Tài khoản trong biến NHIEUMAY (vd "anhtrong,giaovien") được dùng nhiều máy.
// gộp tiến độ: số lấy lớn nhất, object gộp đệ quy (không bao giờ làm mất tiến độ cũ)
function gopTD(a, b) {
  if (typeof a === 'number' && typeof b === 'number') return Math.max(a, b);
  if (a && b && typeof a === 'object' && typeof b === 'object' && !Array.isArray(a) && !Array.isArray(b)) {
    const o = { ...a }; for (const k of Object.keys(b)) o[k] = k in a ? gopTD(a[k], b[k]) : b[k]; return o;
  }
  return b === undefined ? a : b;
}
export class Phien {
  constructor(ctx) { this.ctx = ctx; }
  async fetch(req) {
    const u = new URL(req.url);
    if (u.pathname === '/so') { // sổ tay ghi chú của tài khoản (12/11): {id:{t,b,w,c,u,del}} — gộp theo thời điểm sửa u mới hơn
      const cur = (await this.ctx.storage.get('so')) || {};
      if (req.method === 'POST') {
        const body = await req.text();
        if (body.length > 400000) return new Response('too big', { status: 413 });
        let inc = {}; try { inc = JSON.parse(body) || {}; } catch {}
        for (const [k, n] of Object.entries(inc)) if (n && typeof n === 'object' && (!cur[k] || (n.u || 0) >= (cur[k].u || 0))) cur[k] = n;
        await this.ctx.storage.put('so', cur);
      }
      return new Response(JSON.stringify(cur));
    }
    if (u.pathname === '/td') { // tiến độ học của tài khoản (12/11)
      const cur = (await this.ctx.storage.get('td')) || {};
      if (req.method === 'POST') {
        const body = await req.text();
        if (body.length > 200000) return new Response('too big', { status: 413 });
        let inc = {}; try { inc = JSON.parse(body) || {}; } catch {}
        const m = gopTD(cur, inc); await this.ctx.storage.put('td', m);
        return new Response(JSON.stringify(m));
      }
      return new Response(JSON.stringify(cur));
    }
    // (12/11) dùng cùng lúc 2 thiết bị → đá cả hai, khoá tài khoản 5 phút (giống app Gino)
    const S = this.ctx.storage, now = Date.now();
    if (u.pathname === '/claim') {   // đăng nhập: máy KHÁC (mã thiết bị did khác) còn mở app trong ACTIVE ms → khoá; còn lại máy mới thay máy cũ
      const sid = u.searchParams.get('sid'), dev = u.searchParams.get('dev') || '', did = u.searchParams.get('did') || '';
      const lk = (await S.get('lock')) || 0;
      if (lk > now) return Response.json({ lock: lk });
      const c = await S.get('cur');
      if (c && c.sid && c.did && c.did !== did && now - (c.seen || c.at) < ACTIVE) {
        await S.delete('cur'); await S.put('sid', 'khoa'); await S.put('lock', now + LOCK);
        return Response.json({ lock: now + LOCK });
      }
      await S.put('cur', { sid, dev, did, at: now, seen: now }); await S.put('sid', sid);
      return Response.json({ ok: 1 });
    }
    if (u.pathname === '/st') return Response.json({ sid: (await S.get('sid')) || '', lock: (await S.get('lock')) || 0 });
    if (u.pathname === '/touch') {   // máy đang mở app báo "còn hoạt động" (ghi tối đa 1 lần / 45 giây)
      const c = await S.get('cur'), sid = u.searchParams.get('sid');
      if (c && c.sid === sid && now - (c.seen || 0) > 45e3) { c.seen = now; await S.put('cur', c); }
      return new Response('ok');
    }
    if (u.pathname === '/drop') {    // đăng xuất
      const c = await S.get('cur'); if (c && c.sid === u.searchParams.get('sid')) { await S.delete('cur'); await S.put('sid', ''); }
      return new Response('ok');
    }
    if (req.method === 'PUT') { await this.ctx.storage.put('sid', u.searchParams.get('sid')); return new Response('ok'); }
    return new Response((await this.ctx.storage.get('sid')) || '');
  }
}
// BẬT mặc định (11/11 theo yêu cầu anh): đăng nhập máy mới → máy cũ bị đẩy ra. Tắt bằng biến môi trường MOTMAY=0
const batMotMay = env => String(env.MOTMAY || '').trim() !== '0';
const nhieuMay = (env, u) => String(env.NHIEUMAY || '').toLowerCase().split(/[\s,;]+/).includes(u);
const phien = (env, u) => env.PHIEN.get(env.PHIEN.idFromName(u));
const ACTIVE = 150e3, LOCK = 5 * 60e3;   // máy coi là "đang dùng" nếu mở app trong 2,5 phút gần nhất; khoá 5 phút
async function trangThai(env, u) { try { return await (await phien(env, u).fetch('https://p/st')).json(); } catch { return null; } }
async function giuPhien(env, u, sid, dev, did) {   // → { ok } | { lock }
  try { return await (await phien(env, u).fetch('https://p/claim?' + new URLSearchParams({ sid, dev, did }), { method: 'POST' })).json(); } catch { return { ok: 1 }; }
}
async function baoHoatDong(env, s) { try { await phien(env, s.u).fetch('https://p/touch?sid=' + encodeURIComponent(s.sid), { method: 'POST' }); } catch {} }
async function boPhien(env, s) { try { await phien(env, s.u).fetch('https://p/drop?sid=' + encodeURIComponent(s.sid), { method: 'POST' }); } catch {} }
function tenMay(req) {
  const ua = req.headers.get('User-Agent') || '';
  const os = /iPhone/.test(ua) ? 'iPhone' : /iPad/.test(ua) ? 'iPad' : /Android/.test(ua) ? 'Android' : /Windows/.test(ua) ? 'Windows' : /Mac OS X|Macintosh/.test(ua) ? 'Mac' : /Linux/.test(ua) ? 'Linux' : 'Thiết bị khác';
  const br = /Edg\//.test(ua) ? 'Edge' : /CriOS|Chrome\//.test(ua) ? 'Chrome' : /FxiOS|Firefox\//.test(ua) ? 'Firefox' : /Safari\//.test(ua) ? 'Safari' : '';
  return br ? `${os} · ${br}` : os;
}
async function sidHienTai(env, u) {
  try { return await (await phien(env, u).fetch('https://p/')).text(); } catch { return null; }
}
async function datSid(env, u, sid) {
  try { await phien(env, u).fetch('https://p/?sid=' + encodeURIComponent(sid), { method: 'PUT' }); } catch {}
}
// false = còn hiệu lực; { lock } = phiên này đã bị thiết bị khác thay thế (lock > 0: tài khoản đang bị khoá tạm)
async function biDay(env, s) {
  if (!batMotMay(env) || !env.PHIEN || nhieuMay(env, s.u)) return false;
  const t = await trangThai(env, s.u);
  if (!t || t.sid === '' || t.sid === s.sid) return false;
  return { lock: t.lock > Date.now() ? t.lock : 0 };
}
const KICK = 'Tài khoản này vừa được đăng nhập trên thiết bị khác. Mỗi tài khoản chỉ dùng được trên 1 thiết bị cùng lúc.';
const LOCKMSG = m => `Tài khoản đang được dùng cùng lúc trên 2 thiết bị nên cả hai đã bị đăng xuất. Tài khoản bị khoá tạm, vui lòng đợi ${m} phút rồi đăng nhập lại. Mỗi tài khoản chỉ dùng trên 1 thiết bị.`;
const mins = until => Math.max(1, Math.ceil((until - Date.now()) / 60e3));

// Watermark tên tài khoản + chống sao chép: chèn /app/bv.js vào mọi trang HTML của người đã đăng nhập
function bv(res, u) {
  if (!/text\/html/i.test(res.headers.get('Content-Type') || '')) return res;
  const tag = `<script>window.__WM=${JSON.stringify(u).replace(/</g, '\\u003c')}</script><script src="/app/bv.js?v=3"></script>`;
  return new HTMLRewriter().on('head', { element(e) { e.prepend(tag, { html: true }); } }).transform(res);
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function loginPage(err = '', user = '', next = '/', origin = '') {
  return new Response(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Đăng nhập · Anh Trọng Dạy JFT</title><link rel="icon" href="/app/media/brand/icon.svg" type="image/svg+xml"><link rel="icon" href="/app/media/brand/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/app/media/brand/apple-touch-icon.png"><link rel="manifest" href="/app/media/brand/site.webmanifest"><meta name="theme-color" content="#0d5a8c"><meta name="description" content="Học và luyện thi JFT-Basic theo giáo trình いろどり cùng Anh Trọng Dạy JFT."><meta property="og:title" content="Anh Trọng Dạy JFT · Học & luyện thi JFT-Basic"><meta property="og:description" content="Học và luyện thi JFT-Basic theo giáo trình いろどり: bài học, đề thi thử giống máy thi, video chữa đề."><meta property="og:type" content="website"><meta property="og:image" content="${origin}/app/media/brand/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&display=swap" rel="stylesheet"><meta name="robots" content="noindex"><meta name="theme-color" content="#0a4670">
<style>
*{box-sizing:border-box}
html,body{margin:0;min-height:100%}
body{min-height:100vh;display:grid;grid-template-columns:1.15fr 1fr;font-family:"M PLUS Rounded 1c","Hiragino Maru Gothic ProN","Segoe UI",system-ui,sans-serif;color:#17222c;background:#f3f6f8}
.jp{font-family:"M PLUS Rounded 1c","Hiragino Maru Gothic ProN",sans-serif}
.side{position:relative;overflow:hidden;color:#fff;padding:48px 56px;display:flex;flex-direction:column;background:radial-gradient(900px 600px at 90% 0%,#1a78b4 0%,rgba(26,120,180,0) 60%),linear-gradient(140deg,#0b3d60 0%,#0d5a8c 55%,#0a4670 100%)}
.side::after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:44px 44px;mask-image:linear-gradient(180deg,#000,transparent 80%);pointer-events:none}
.brand{position:relative;z-index:1}.brand img{display:block;width:230px;height:auto}
.logo{width:42px;height:42px;border-radius:11px;background:#c42f66;color:#fff;display:grid;place-items:center;font-weight:800;font-size:16px;flex:none}
.side h1{position:relative;z-index:1;font-size:46px;line-height:1.2;margin:56px 0 22px;letter-spacing:-.01em;font-weight:800}
.side h1 span{color:#ffd166;white-space:nowrap}
.side p.lead{position:relative;z-index:1;margin:0;font-size:17px;color:#d4e6f3;max-width:470px;line-height:1.55}
.chips{position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.chips span{border:1px solid rgba(255,255,255,.35);border-radius:99px;padding:6px 14px;font-size:13.5px;font-weight:600}
.books{position:relative;z-index:1;margin-top:auto;height:260px}
.books img{position:absolute;bottom:-70px;width:150px;border-radius:8px;box-shadow:0 18px 40px rgba(0,0,0,.45);transform-origin:50% 100%;transform:rotate(var(--r));animation:wob 3s ease-in-out infinite;animation-delay:var(--d)}
.books img:nth-child(1){left:0;--r:-13deg;--d:0s}.books img:nth-child(2){left:105px;bottom:-52px;--r:-4deg;--d:-.75s}
.books img:nth-child(3){left:210px;bottom:-52px;--r:5deg;--d:-1.5s}.books img:nth-child(4){left:315px;--r:13deg;--d:-2.25s}
@keyframes wob{0%,100%{transform:rotate(var(--r)) translateY(0)}20%{transform:rotate(calc(var(--r) - 3deg)) translateY(-7px)}40%{transform:rotate(calc(var(--r) + 2.5deg)) translateY(-2px)}60%{transform:rotate(calc(var(--r) - 1.5deg)) translateY(-8px)}80%{transform:rotate(calc(var(--r) + 1deg)) translateY(-1px)}}
@media (prefers-reduced-motion:reduce){.books img{animation:none}}
main{display:grid;place-items:center;padding:32px 20px}
form{background:#fff;border-radius:20px;padding:34px 32px;width:100%;max-width:400px;box-shadow:0 24px 60px rgba(13,40,60,.14);border:1px solid #e3e9ee}
form h2{font-size:24px;margin:0 0 4px}
form p{margin:0 0 20px;color:#5a6873;font-size:14.5px}
label{display:block;font-weight:600;font-size:13px;margin:14px 0 6px;color:#2a3a47}
.f{position:relative}
input{width:100%;border:1.5px solid #dbe2e7;border-radius:12px;padding:13px 14px;font:inherit;font-size:16px;background:#f8fafb;transition:border-color .15s,box-shadow .15s,background .15s}
input:focus{outline:0;border-color:#0d5a8c;background:#fff;box-shadow:0 0 0 4px rgba(13,90,140,.12)}
.eye{position:absolute;right:8px;top:50%;transform:translateY(-50%);border:0;background:none;color:#5a6873;font-family:inherit;font-weight:600;font-size:12.5px;padding:6px 8px;cursor:pointer;border-radius:8px}
.err{color:#b3261e;font-size:13.5px;min-height:20px;margin-top:12px;font-weight:600}
button.go{width:100%;margin-top:4px;border:0;border-radius:12px;background:linear-gradient(135deg,#0d5a8c,#0a4670);color:#fff;font-family:inherit;font-weight:700;font-size:16.5px;padding:14px;cursor:pointer;box-shadow:0 8px 20px rgba(13,90,140,.28);transition:transform .15s,box-shadow .15s}
button.go:hover{transform:translateY(-1px);box-shadow:0 12px 26px rgba(13,90,140,.34)}
.help{margin-top:16px;font-size:13px;color:#5a6873;text-align:center}
.soc{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.soc a{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:12px;text-decoration:none;color:#fff;transition:transform .15s,box-shadow .15s}
.soc a:hover{transform:translateY(-1px);box-shadow:0 8px 18px rgba(0,0,0,.15)}
.soc svg{width:22px;height:22px;flex:none}.soc span{display:flex;flex-direction:column;line-height:1.2;min-width:0}.soc b{font-size:14px}.soc small{font-size:11.5px;opacity:.85;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.soc .fb{background:#1877f2}.soc .tt{background:#111}
small.cr{display:block;margin-top:22px;color:#9aa6b0;font-size:11.5px;text-align:center;line-height:1.5}
@media (max-width:880px){
 body{grid-template-columns:1fr}
 .side{padding:24px 20px 0;min-height:auto}
 .brand img{width:180px}.side h1{font-size:28px;margin:22px 0 8px}.side p.lead{font-size:14.5px}.chips{display:none}
 .books{height:150px;margin-top:18px;align-self:center;width:330px}
 .books img{width:96px;bottom:-44px}.books img:nth-child(2){left:70px;bottom:-34px}.books img:nth-child(3){left:140px;bottom:-34px}.books img:nth-child(4){left:210px}
 main{padding:22px 16px 32px}form{padding:26px 22px;margin-top:-8px}
}
</style></head><body>
<aside class="side">
 <div class="brand"><img src="/app/media/brand/logo-ngang-trang.svg" alt="Anh Trọng Dạy JFT" width="224" height="57"></div>
 <h1>Học và Luyện thi <span>JFT-Basic</span></h1>
 <div class="chips"><span class="jp">入門 A1</span><span class="jp">初級1 A2</span><span class="jp">初級2 A2</span><span class="jp">初中級 A2/B1</span></div>
 <div class="books" aria-hidden="true"><img src="/app/media/cover/nyumon.jpg" alt=""><img src="/app/media/cover/s1.jpg" alt=""><img src="/app/media/cover/s2.jpg" alt=""><img src="/app/media/cover/sc.jpg" alt=""></div>
</aside>
<main>
<form method="post" action="/login">
 <h2>Đăng nhập</h2><p>Dùng tài khoản lớp học được cấp.</p>
 <input type="hidden" name="next" value="${esc(next)}">
 <label for="u">Tài khoản</label><div class="f"><input id="u" name="u" autocomplete="username" value="${esc(user)}" required autofocus></div>
 <label for="p">Mật khẩu</label><div class="f"><input id="p" name="p" type="password" autocomplete="current-password" required style="padding-right:64px"><button class="eye" type="button" onclick="const i=document.getElementById('p');i.type=i.type==='password'?'text':'password';this.textContent=i.type==='password'?'Hiện':'Ẩn'">Hiện</button></div>
 <div class="err" role="alert">${esc(err)}</div>
 <button class="go" type="submit">Vào học →</button>
 <div class="help">Chưa có tài khoản? Nhắn Anh Trọng Dạy JFT để được cấp:</div>
 <div class="soc"><a class="fb" href="https://www.facebook.com/anh.trongg.2024/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 8V6.5c0-.7.5-1 1-1h2V2h-3c-3 0-4 2-4 4.3V8H7.5v3.5H10V22h4V11.5h2.8l.5-3.5H14z"/></svg><span><b>Facebook</b><small>Anh Trọng</small></span></a><a class="tt" href="https://www.tiktok.com/@anhtrong.daygino" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.6 2h-3.4v13.4a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9.2a6.4 6.4 0 1 0 5.4 6.3V8.8a8 8 0 0 0 4.4 1.3V6.7a4.6 4.6 0 0 1-4.4-4.7z"/></svg><span><b>TikTok</b><small>@anhtrong.daygino</small></span></a></div>
 <small class="cr">© 2026 Anh Trọng Dạy JFT · 出典：国際交流基金「いろどり 生活の日本語」。表紙の著作権は国際交流基金に帰属します。</small>
</form>
</main>
</body></html>`,
    { status: err ? 401 : 200, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } });
}

const safeNext = n => (typeof n === 'string' && n.startsWith('/') && !n.startsWith('//') ? n : '/');

export async function handle(req, env, next) {
  const url = new URL(req.url);

  if (url.pathname === '/login' && req.method === 'POST') {
    const f = await req.formData();
    const u = String(f.get('u') || '').trim().toLowerCase();
    const p = String(f.get('p') || '');
    const dest = safeNext(f.get('next'));
    const pass = accounts(env).get(u);
    if (!pass || pass !== p) return loginPage('Sai tài khoản hoặc mật khẩu.', u, dest, url.origin);
    const exp = Date.now() + DAYS * 864e5;
    const sid = crypto.randomUUID().replace(/-/g, '').slice(0, 16);
    const did = /^[0-9a-f]{32}$/.test(getCookie(req, 'jft_dev') || '') ? getCookie(req, 'jft_dev') : crypto.randomUUID().replace(/-/g, '');   // mã thiết bị
    const devCookie = `jft_dev=${did}; Path=/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax`;
    if (batMotMay(env) && env.PHIEN && !nhieuMay(env, u)) {
      // máy khác đang mở app bằng tài khoản này → đá cả hai ra, khoá 5 phút; máy cũ đã tắt app / cùng máy → máy mới thay máy cũ
      const r = await giuPhien(env, u, sid, tenMay(req), did);
      if (r.lock) { const lp = loginPage(LOCKMSG(mins(r.lock)), u, dest, url.origin); lp.headers.append('Set-Cookie', devCookie); return lp; }
    }
    const val = `${u}|${exp}|${sid}|${await sign(env, `${u}|${exp}|${sid}|${pass}`)}`;
    const h = new Headers({ Location: dest, 'Cache-Control': 'no-store' });
    h.append('Set-Cookie', devCookie);
    h.append('Set-Cookie', `${COOKIE}=${encodeURIComponent(val)}; Path=/; Max-Age=${DAYS * 86400}; HttpOnly; Secure; SameSite=Lax`);
    h.append('Set-Cookie', `jft_user=${encodeURIComponent(u)}; Path=/; Max-Age=${DAYS * 86400}; Secure; SameSite=Lax`);
    // vé dùng 1 lần: mở app ngay sau khi đăng nhập; tải lại trang = phải đăng nhập lại
    h.append('Set-Cookie', `jft_once=1; Path=/; Max-Age=120; HttpOnly; Secure; SameSite=Lax`);
    // xoá cookie "lưu đăng nhập" cũ (chức năng đã gỡ 23/10)
    h.append('Set-Cookie', `jft_keep=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`);
    return new Response(null, { status: 303, headers: h });
  }

  if (url.pathname === '/logout') {
    const s0 = await session(req, env);
    if (s0 && env.PHIEN && batMotMay(env) && !nhieuMay(env, s0.u)) await boPhien(env, s0);
    const h = new Headers({ Location: '/login', 'Cache-Control': 'no-store' });
    h.append('Set-Cookie', `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`);
    h.append('Set-Cookie', `jft_user=; Path=/; Max-Age=0; Secure; SameSite=Lax`);
    h.append('Set-Cookie', `jft_keep=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`);
    return new Response(null, { status: 303, headers: h });
  }

  if ((url.pathname.startsWith('/app/media/cover/') || url.pathname.startsWith('/app/media/brand/') || url.pathname === '/favicon.ico') && req.method === 'GET') return next();
  if (url.pathname === '/login' && req.method === 'GET') {
    let msg = '';
    if (url.searchParams.get('kick')) {   // bị đẩy ra: nếu tài khoản đang bị khoá tạm thì báo số phút còn lại
      msg = KICK;
      const s0 = await session(req, env), lk = Number(url.searchParams.get('l') || 0);
      const t = s0 && env.PHIEN ? await trangThai(env, s0.u) : null;
      const until = Math.max(lk, t && t.lock || 0);
      if (until > Date.now()) msg = LOCKMSG(mins(until));
    }
    const lp = loginPage(msg, '', safeNext(url.searchParams.get('next')), url.origin);
    return url.searchParams.get('kick') ? new Response(lp.body, { status: 200, headers: lp.headers }) : lp;
  }
  const ses = await session(req, env);
  const user = ses && ses.u;
  if (!user) {
    const accept = req.headers.get('Accept') || '';
    if (req.method === 'GET' && accept.includes('text/html') && req.headers.get('Sec-Fetch-Dest') !== 'iframe') {
      return Response.redirect(`${url.origin}/login?next=${encodeURIComponent(url.pathname + url.search)}`, 302);
    }
    return new Response('Cần đăng nhập', { status: 401, headers: { 'Cache-Control': 'no-store' } });
  }
  const dest = req.headers.get('Sec-Fetch-Dest');
  const isDoc = req.method === 'GET' && (dest === 'document' || (!dest && (req.headers.get('Accept') || '').includes('text/html')));
  // 1 tài khoản = 1 thiết bị: kiểm tra khi mở trang, tải dữ liệu, gọi API và nhịp kiểm tra định kỳ /api/phien
  if (isDoc || url.pathname.startsWith('/app/data/') || url.pathname.startsWith('/api/') || url.pathname.startsWith('/kiemtra/ketqua')) {
    const k = await biDay(env, ses);
    if (k) {
      const q = k.lock ? `kick=2&l=${k.lock}` : 'kick=1';
      if (isDoc) return new Response(null, { status: 302, headers: { Location: '/login?' + q, 'Cache-Control': 'no-store' } });
      return new Response(JSON.stringify({ kick: 1, lock: k.lock, e: k.lock ? LOCKMSG(mins(k.lock)) : KICK }), { status: 401, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } });
    }
    // máy này còn đang mở app (nhịp /api/phien mỗi 60 giây + mỗi lần mở trang)
    if ((isDoc || url.pathname === '/api/phien') && batMotMay(env) && env.PHIEN && !nhieuMay(env, ses.u)) await baoHoatDong(env, ses);
  }
  if ((url.pathname === '/api/tiendo' || url.pathname === '/api/so') && env.PHIEN) {
    const r = await phien(env, user).fetch(url.pathname === '/api/so' ? 'https://p/so' : 'https://p/td', req.method === 'POST' ? { method: 'POST', body: await req.text() } : {});
    return new Response(r.body, { status: r.status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } });
  }
  if (url.pathname === '/api/phien') return new Response('{"ok":1}', { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
  // Trang chính của app: đã đăng nhập (cookie còn hạn 5 ngày) là vào thẳng
  if (isDoc && (url.pathname === '/' || url.pathname === '/index.html')) {
    const r = await next();
    const o = new Response(r.body, r);
    o.headers.set('Cache-Control', 'no-store');
    o.headers.append('Set-Cookie', `jft_once=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`);
    return bv(o, user);
  }

  const res = await next();
  const out = new Response(res.body, res);
  // Trang HTML + dữ liệu app: luôn hỏi lại máy chủ (có bản mới là thấy ngay); ảnh/audio vẫn lưu 1 giờ
  const fresh = url.pathname === '/' || url.pathname.endsWith('.html') || url.pathname.startsWith('/app/data/');
  out.headers.set('Cache-Control', fresh ? 'private, no-cache' : 'private, max-age=3600');
  out.headers.set('X-Robots-Tag', 'noindex');
  return bv(out, user);
}
