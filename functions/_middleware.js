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
<title>Đăng nhập · Anh Trọng Dạy JFT</title><meta name="robots" content="noindex">
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;padding:16px;background:linear-gradient(135deg,#0d5a8c,#0a4670);font-family:"Segoe UI",system-ui,-apple-system,sans-serif;color:#17222c}
form{background:#fff;border-radius:18px;padding:28px;width:100%;max-width:380px;box-shadow:0 20px 50px rgba(0,0,0,.25)}
.logo{width:40px;height:40px;border-radius:10px;background:#c42f66;color:#fff;display:grid;place-items:center;font-weight:700}
h1{font-size:20px;margin:12px 0 4px}p{margin:0 0 16px;color:#5a6873;font-size:14px}
label{display:block;font-weight:600;font-size:13px;margin:12px 0 4px}
input{width:100%;border:1px solid #dbe2e7;border-radius:10px;padding:11px 12px;font:inherit;font-size:16px}
input:focus{outline:2px solid #0d5a8c;border-color:#0d5a8c}
.err{color:#b3261e;font-size:13px;min-height:18px;margin-top:10px}
button{width:100%;margin-top:6px;border:0;border-radius:10px;background:#0d5a8c;color:#fff;font:600 16px inherit;padding:12px;cursor:pointer}
small{display:block;margin-top:14px;color:#9aa6b0;font-size:12px;text-align:center}
</style></head><body>
<form method="post" action="/login"><span class="logo">AT</span><h1>Anh Trọng Dạy JFT</h1><p>Đăng nhập bằng tài khoản lớp học được cấp.</p>
<input type="hidden" name="next" value="${esc(next)}">
<label for="u">Tài khoản</label><input id="u" name="u" autocomplete="username" value="${esc(user)}" required autofocus>
<label for="p">Mật khẩu</label><input id="p" name="p" type="password" autocomplete="current-password" required>
<div class="err">${esc(err)}</div><button type="submit">Vào học</button>
<small>© 2026 Anh Trọng Dạy JFT · Tài liệu dựa trên いろどり 生活の日本語 (The Japan Foundation)</small></form></body></html>`,
    { status: err ? 401 : 200, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } });
}

const safeNext = n => (typeof n === 'string' && n.startsWith('/') && !n.startsWith('//') ? n : '/');

export async function onRequest(ctx) {
  const { request: req, env, next } = ctx;
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
