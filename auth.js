// Anh Trọng Dạy JFT — đăng nhập phía máy chủ (Cloudflare Pages Functions)
// Danh sách tài khoản nằm ở biến môi trường ACCOUNTS trên Cloudflare (không nằm trong code):
//   mỗi dòng (hoặc cách nhau dấu phẩy) một tài khoản dạng  ten:matkhau
//   ví dụ:  lan:Lan2026, minh:Minh2026, hocvien:jft2026
// Muốn khoá 1 bạn: xoá dòng của bạn đó rồi Deploy lại. Đổi mật khẩu: sửa rồi Deploy lại.
// Tuỳ chọn: biến SECRET (chuỗi bất kỳ, dài) để ký cookie.

const COOKIE = 'jft_s';
const DAYS = 30;
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

async function currentUser(req, env) {
  const v = getCookie(req, COOKIE);
  if (!v) return null;
  const [u, exp, sig] = v.split('|');
  if (!u || !exp || !sig || Date.now() > Number(exp)) return null;
  const pass = accounts(env).get(u);
  if (!pass) return null; // tài khoản đã bị xoá → mất quyền ngay
  return (await sign(env, `${u}|${exp}|${pass}`)) === sig ? u : null;
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function loginPage(err = '', user = '', next = '/') {
  return new Response(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Đăng nhập · Anh Trọng Dạy JFT</title><meta name="robots" content="noindex"><meta name="theme-color" content="#0a4670">
<style>
*{box-sizing:border-box}
html,body{margin:0;min-height:100%}
body{min-height:100vh;display:grid;grid-template-columns:1.15fr 1fr;font-family:"Be Vietnam Pro","Segoe UI",system-ui,-apple-system,sans-serif;color:#17222c;background:#f3f6f8}
.jp{font-family:"Hiragino Kaku Gothic ProN","Yu Gothic","Noto Sans JP",Meiryo,sans-serif}
.side{position:relative;overflow:hidden;color:#fff;padding:48px 56px;display:flex;flex-direction:column;background:radial-gradient(900px 600px at 90% 0%,#1a78b4 0%,rgba(26,120,180,0) 60%),linear-gradient(140deg,#0b3d60 0%,#0d5a8c 55%,#0a4670 100%)}
.side::after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:44px 44px;mask-image:linear-gradient(180deg,#000,transparent 80%);pointer-events:none}
.brand{display:flex;align-items:center;gap:12px;font-weight:700;font-size:18px;position:relative;z-index:1}
.logo{width:42px;height:42px;border-radius:11px;background:#c42f66;color:#fff;display:grid;place-items:center;font-weight:800;font-size:16px;flex:none}
.side h1{position:relative;z-index:1;font-size:44px;line-height:1.12;margin:56px 0 14px;letter-spacing:-.01em;font-weight:800}
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
 .side h1{font-size:28px;margin:22px 0 8px}.side p.lead{font-size:14.5px}.chips{display:none}
 .books{height:150px;margin-top:18px;align-self:center;width:330px}
 .books img{width:96px;bottom:-44px}.books img:nth-child(2){left:70px;bottom:-34px}.books img:nth-child(3){left:140px;bottom:-34px}.books img:nth-child(4){left:210px}
 main{padding:22px 16px 32px}form{padding:26px 22px;margin-top:-8px}
}
</style></head><body>
<aside class="side">
 <div class="brand"><span class="logo">AT</span>Anh Trọng Dạy JFT</div>
 <h1>Học và Luyện thi <span>JFT-Basic</span></h1>
 <p class="lead">Học trọn bộ giáo trình <span class="jp">いろどり 生活の日本語</span>: bài giảng slide, ngữ pháp, từ vựng, luyện kỹ năng và 20 đề thi thử giống máy thi thật.</p>
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
    if (!pass || pass !== p) return loginPage('Sai tài khoản hoặc mật khẩu.', u, dest);
    const exp = Date.now() + DAYS * 864e5;
    const val = `${u}|${exp}|${await sign(env, `${u}|${exp}|${pass}`)}`;
    const h = new Headers({ Location: dest, 'Cache-Control': 'no-store' });
    h.append('Set-Cookie', `${COOKIE}=${encodeURIComponent(val)}; Path=/; Max-Age=${DAYS * 86400}; HttpOnly; Secure; SameSite=Lax`);
    h.append('Set-Cookie', `jft_user=${encodeURIComponent(u)}; Path=/; Max-Age=${DAYS * 86400}; Secure; SameSite=Lax`);
    return new Response(null, { status: 303, headers: h });
  }

  if (url.pathname === '/logout') {
    const h = new Headers({ Location: '/login', 'Cache-Control': 'no-store' });
    h.append('Set-Cookie', `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`);
    h.append('Set-Cookie', `jft_user=; Path=/; Max-Age=0; Secure; SameSite=Lax`);
    return new Response(null, { status: 303, headers: h });
  }

  if (url.pathname.startsWith('/app/media/cover/') && req.method === 'GET') return next();
  const user = await currentUser(req, env);
  if (!user) {
    if (url.pathname === '/login') return loginPage('', '', safeNext(url.searchParams.get('next')));
    const accept = req.headers.get('Accept') || '';
    if (req.method === 'GET' && accept.includes('text/html') && req.headers.get('Sec-Fetch-Dest') !== 'iframe') {
      return Response.redirect(`${url.origin}/login?next=${encodeURIComponent(url.pathname + url.search)}`, 302);
    }
    return new Response('Cần đăng nhập', { status: 401, headers: { 'Cache-Control': 'no-store' } });
  }
  if (url.pathname === '/login') return Response.redirect(url.origin + '/', 302);

  const res = await next();
  const out = new Response(res.body, res);
  out.headers.set('Cache-Control', 'private, max-age=3600');
  out.headers.set('X-Robots-Tag', 'noindex');
  return out;
}
