// Workers (static assets): mọi request đi qua đăng nhập trước
// Riêng tên miền bản dùng thử (jft-dungthu.*): không đăng nhập, chỉ phục vụ thư mục public/_demo
// (bản khoá, tạo bởi src/build_demo.py) – không bao giờ trả nội dung bản đầy đủ.
import { handle, currentUser } from './auth.js';
export { Phien } from './auth.js';
import { hoi } from './hoidap.js';
import { isPublic, kiemtraPublic, ketqua } from './kiemtra.js';
export { KiemTra } from './kiemtra.js';
import DALLOW from './demo_allow.js';
const DALLOWF = new Set(DALLOW.f);
// 19/11: file nội dung (bài học, tài liệu, BTVN, media) của phần mở trong bản dùng thử lấy thẳng từ bản chính, chỉ đúng danh sách do build_demo.py sinh ra
const demoOK = p => { let d; try { d = decodeURIComponent(p).replace(/^\/+/, ''); } catch (e) { return false; } if (d.includes('..')) return false;
  return DALLOWF.has(d) || DALLOWF.has(d + '.html') || DALLOW.p.some(x => d.startsWith(x)); };
const isDemo = h => /^jft-dungthu\./i.test(h);
async function demo(req, env) {
  const url = new URL(req.url);
  if (url.pathname === '/login' || url.pathname === '/logout') return Response.redirect(url.origin + '/', 302);
  let p = url.pathname.endsWith('/') ? url.pathname : url.pathname;
  let res;
  for (let i = 0; i < 4; i++) {
    const u = new URL(url); u.pathname = '/_demo' + p;
    res = await env.ASSETS.fetch(new Request(u, { method: req.method, headers: req.headers }));
    const loc = res.headers.get('Location');
    if (res.status >= 300 && res.status < 400 && loc) {
      const nl = new URL(loc, u);
      if (nl.pathname.startsWith('/_demo')) { p = nl.pathname.slice(6) || '/'; continue; }
    }
    break;
  }
  if (res.status === 404 && (demoOK(p) || p === '/app/slidenav.js')) {
    let q = p;
    for (let i = 0; i < 4; i++) {
      const u = new URL(url); u.pathname = q;
      res = await env.ASSETS.fetch(new Request(u, { method: req.method, headers: req.headers }));
      const loc = res.headers.get('Location');
      if (res.status >= 300 && res.status < 400 && loc) { const nl = new URL(loc, u); if (demoOK(nl.pathname)) { q = nl.pathname; continue; } }
      break;
    }
    if (res.status >= 300 && res.status < 400) res = new Response('Not found', { status: 404 });
  }
  let out = new Response(res.body, res);
  // thanh xem nhanh slide (app/slidenav.js) cho trang slide của bản dùng thử
  if (/text\/html/i.test(res.headers.get('Content-Type') || '') && /^\/(tailieu|lessons)\//.test(p))
    out = new HTMLRewriter().on('head', { element(e) { e.prepend('<script src="/app/slidenav.js?v=1"></script>', { html: true }); } }).transform(out);
  const fresh = p === '/' || p.endsWith('.html') || p.startsWith('/app/data/') || !/\.[a-z0-9]+$/i.test(p);
  out.headers.set('Cache-Control', fresh ? 'no-cache' : 'public, max-age=3600');
  out.headers.set('X-Robots-Tag', 'noindex');
  return out;
}
export default {
  fetch(req, env) {
    const url = new URL(req.url);
    if (isDemo(url.hostname)) return demo(req, env);
    // bài kiểm tra: link làm bài + nộp bài công khai; trang kết quả cần đăng nhập (giáo viên)
    if (isPublic(url.pathname)) return kiemtraPublic(req, env);
    return handle(req, env, async () => url.pathname === '/api/hoi' ? hoi(req, env, await currentUser(req, env)) : url.pathname.startsWith('/kiemtra/ketqua') ? ketqua(req, env) : env.ASSETS.fetch(req));
  }
};
