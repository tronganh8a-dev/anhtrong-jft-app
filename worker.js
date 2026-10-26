// Workers (static assets): mọi request đi qua đăng nhập trước
// Riêng tên miền bản dùng thử (jft-dungthu.*): không đăng nhập, chỉ phục vụ thư mục public/_demo
// (bản khoá, tạo bởi src/build_demo.py) – không bao giờ trả nội dung bản đầy đủ.
import { handle } from './auth.js';
import { isPublic, kiemtraPublic, ketqua } from './kiemtra.js';
export { KiemTra } from './kiemtra.js';
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
  const out = new Response(res.body, res);
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
    return handle(req, env, () => url.pathname.startsWith('/kiemtra/ketqua') ? ketqua(req, env) : env.ASSETS.fetch(req));
  }
};
