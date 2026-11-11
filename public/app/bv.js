/* Bảo vệ nội dung (11/11/2026): watermark tên tài khoản phủ khắp màn hình + chặn sao chép/lưu/in/devtools.
   Được auth.js chèn vào mọi trang HTML của người đã đăng nhập (window.__WM = tên tài khoản). */
(function () {
  if (window.__bvOn) return; window.__bvOn = 1;
  var U = String(window.__WM || '').slice(0, 40) || 'JFT';
  var inAn = /^\/btvn\//.test(location.pathname); // bài tập về nhà: vẫn cho In (watermark in kèm)
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function stamp() { var d = new Date(); return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function svg() {
    var esc = function (s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
    var s = '<svg xmlns="http://www.w3.org/2000/svg" width="520" height="340"><g transform="rotate(-24 260 170)" font-family="Arial,sans-serif" text-anchor="middle">' +
      '<text x="260" y="150" font-size="22" font-weight="700" fill="rgba(13,43,64,.10)">' + esc(U) + '</text>' +
      '<text x="260" y="176" font-size="15" font-weight="700" fill="rgba(13,90,140,.10)">Anh Trọng Dạy JFT</text>' +
      '<text x="260" y="198" font-size="13" fill="rgba(196,47,102,.10)">' + esc(stamp()) + '</text></g></svg>';
    return 'url("data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s) + '")';
  }
  var css = '#bv-wm{position:fixed!important;inset:0!important;z-index:2147483646!important;pointer-events:none!important;background-repeat:repeat!important;opacity:1!important;display:block!important;visibility:visible!important;mix-blend-mode:multiply}' +
    'body{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}' +
    'input,textarea,[contenteditable]{-webkit-user-select:text;user-select:text}' +
    'img,video{-webkit-user-drag:none}' +
    (inAn ? '@media print{#bv-wm{position:fixed!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}' : '@media print{body *{visibility:hidden!important}body:after{content:"Tài liệu thuộc Anh Trọng Dạy JFT – không được in";visibility:visible;position:fixed;top:40%;left:0;right:0;text-align:center;font:700 24px Arial}}') +
    '#bv-black{position:fixed;inset:0;z-index:2147483647;background:#000;display:none}';
  var st = document.createElement('style'); st.id = 'bv-css'; st.textContent = css;
  var wm = document.createElement('div'); wm.id = 'bv-wm'; wm.setAttribute('aria-hidden', 'true');
  var bk = document.createElement('div'); bk.id = 'bv-black';
  function paint() { wm.style.backgroundImage = svg(); }
  function host() { var f = document.fullscreenElement || document.webkitFullscreenElement; return f && !/^(IFRAME|VIDEO|IMG|CANVAS)$/.test(f.tagName) ? f : document.body; }
  function mount() {
    if (!document.body) return;
    if (!document.getElementById('bv-css')) (document.head || document.documentElement).appendChild(st);
    var h = host();
    if (wm.parentNode !== h) h.appendChild(wm);
    if (bk.parentNode !== h) h.appendChild(bk);
    if (wm.getAttribute('style') && !/background-image/.test(wm.getAttribute('style'))) paint();
  }
  paint();
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
  setInterval(function () { paint(); mount(); }, 30000);
  // gỡ watermark bằng devtools → tự gắn lại
  new MutationObserver(function () { if (!document.body.contains(wm) || !document.getElementById('bv-css')) mount(); })
    .observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener('fullscreenchange', mount); document.addEventListener('webkitfullscreenchange', mount);

  var editable = function (e) { var t = e.target; return t && (t.isContentEditable || /^(INPUT|TEXTAREA)$/.test(t.tagName)); };
  ['contextmenu', 'dragstart', 'selectstart'].forEach(function (ev) {
    document.addEventListener(ev, function (e) { if (!editable(e)) e.preventDefault(); }, true);
  });
  ['copy', 'cut'].forEach(function (ev) {
    document.addEventListener(ev, function (e) { if (!editable(e)) { e.preventDefault(); try { e.clipboardData.setData('text/plain', 'Tài liệu thuộc Anh Trọng Dạy JFT'); } catch (_) {} } }, true);
  });
  function flash() { bk.style.display = 'block'; setTimeout(function () { bk.style.display = 'none'; }, 1500); }
  document.addEventListener('keydown', function (e) {
    var k = (e.key || '').toLowerCase(), c = e.ctrlKey || e.metaKey;
    var bad = k === 'f12' ||
      (c && ['s', 'u'].indexOf(k) >= 0) || (c && k === 'p' && !inAn) ||
      (c && e.shiftKey && ['i', 'j', 'c', 's'].indexOf(k) >= 0) ||
      (e.metaKey && e.altKey && ['i', 'j', 'c', 'u'].indexOf(k) >= 0) ||
      (c && ['c', 'x', 'a'].indexOf(k) >= 0 && !editable(e));
    if (k === 'printscreen') { flash(); try { navigator.clipboard.writeText('Tài liệu thuộc Anh Trọng Dạy JFT'); } catch (_) {} }
    if (e.metaKey && e.shiftKey && ['3', '4', '5'].indexOf(k) >= 0) flash();
    if (bad) { e.preventDefault(); e.stopPropagation(); }
  }, true);
  document.addEventListener('keyup', function (e) { if ((e.key || '').toLowerCase() === 'printscreen') flash(); }, true);
  if (!inAn) window.addEventListener('beforeprint', flash);
})();
