/* Thanh bên xem nhanh slide (19/11/2026) — Anh Trọng Dạy JFT
   Tự chèn vào các trang slide: /tailieu/*.html và /lessons/*_Slide.html (auth.js chèn script này).
   Mở/đóng bằng tab ở mép trái hoặc phím G; Esc để đóng. Bấm ảnh nhỏ để nhảy tới slide. */
(function () {
  if (window.__snv) return; window.__snv = 1;
  var path; try { path = decodeURIComponent(location.pathname); } catch (e) { path = location.pathname; }
  if (!/\/tailieu\/[^/]+\.html?$|\/lessons\/.+_Slide\.html?$/i.test(path)) return;

  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  var LS = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };

  function init() {
    // nhận dạng kiểu slide
    var T = 'a', S = qa('section.slide');
    if (S.length < 2) { S = qa('.deck-slide'); T = 'd'; }
    if (S.length < 2) { S = qa('#st > img.s'); T = 'i'; }
    if (S.length < 2) { S = qa('#st > .w'); T = 'w'; }
    if (S.length < 2) return;
    var N = S.length;

    function cur() {
      if (T === 'd') { var m = /^#(\d+)$/.exec(location.hash); if (m) return Math.max(0, Math.min(N - 1, +m[1] - 1)); }
      for (var k = 0; k < N; k++) if (S[k].classList.contains('on')) return k;
      return 0;
    }
    function key(k) { var e = new KeyboardEvent('keydown', { key: k, bubbles: true, cancelable: true }); document.dispatchEvent(e); }
    function go(k) {
      k = Math.max(0, Math.min(N - 1, k));
      if (T === 'd') { location.hash = '#' + (k + 1); }
      else if (T === 'w' && typeof window.go === 'function') { window.go(k); }
      else if (typeof window.show === 'function') { window.show(k); }
      else { key('Home'); for (var j = 0; j < k; j++) key('ArrowRight'); } // slide bài giảng いろどり (hàm show nằm trong IIFE)
      setTimeout(mark, 30);
    }

    // kích thước gốc của slide
    function src(k) { return T === 'd' ? (q('.deck-scaler > *', S[k]) || S[k]) : S[k]; }
    var c0 = src(cur()), W = c0.offsetWidth, H = c0.offsetHeight;
    if (T === 'i') { W = S[0].naturalWidth || 1600; H = S[0].naturalHeight || 900; }
    if (!W || !H || W < 300) { W = (T === 'd' || T === 'w') ? 1920 : 1600; H = W * 9 / 16; }
    var host = (T === 'd' ? c0 : S[0]).parentElement || document.body, cs = getComputedStyle(host);
    var font = 'font-family:' + cs.fontFamily + ';font-size:' + cs.fontSize + ';line-height:' + cs.lineHeight + ';color:' + cs.color + ';font-weight:' + cs.fontWeight + ';letter-spacing:' + cs.letterSpacing + ';';

    var st = document.createElement('style');
    st.textContent =
      '#snv-tab{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:2147482000;width:24px;height:92px;border:0;border-radius:0 12px 12px 0;background:rgba(13,43,64,.62);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:.6;transition:opacity .2s,left .25s ease;padding:0;-webkit-tap-highlight-color:transparent}' +
      '#snv-tab:hover{opacity:1;background:#c42f66}#snv-tab svg{transition:transform .25s}' +
      'html.snv-open #snv-tab{left:var(--snvw);opacity:.9}html.snv-open #snv-tab svg{transform:rotate(180deg)}' +
      '#snv{--g:#ff6b9d;position:fixed;left:0;top:0;bottom:0;width:var(--snvw);z-index:2147482001;background:rgba(12,30,46,.95);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transform:translateX(-102%);transition:transform .25s ease;display:flex;flex-direction:column;box-shadow:4px 0 24px rgba(0,0,0,.35);user-select:none;-webkit-user-select:none}' +
      'html.snv-open #snv{transform:none}' +
      '#snv .snv-h{display:flex;align-items:center;gap:8px;padding:12px 10px 10px 14px;border-bottom:1px solid rgba(255,255,255,.12);color:#fff;font:700 14px/1.2 "M PLUS Rounded 1c",system-ui,sans-serif}' +
      '#snv .snv-h b{flex:1}#snv .snv-h span{font-weight:600;opacity:.75;font-size:12.5px}' +
      '#snv .snv-x{width:30px;height:30px;border:0;border-radius:8px;background:rgba(255,255,255,.1);color:#fff;cursor:pointer;font-size:16px;line-height:1}#snv .snv-x:hover{background:#c42f66}' +
      '#snv .snv-l{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:12px 12px 48px 6px;display:flex;flex-direction:column;gap:12px;scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.3) transparent}' +
      '.snv-it{display:flex;gap:6px;align-items:flex-start;cursor:pointer;border:0;background:none;padding:0;margin:0;color:#fff;text-align:left;width:100%}' +
      '.snv-n{width:26px;flex:none;text-align:right;padding-top:3px;font:600 11.5px/1 system-ui,sans-serif;opacity:.65}' +
      '.snv-b{position:relative;flex:1;min-width:0;border-radius:6px;overflow:hidden;background:#fff;box-shadow:0 0 0 1px rgba(255,255,255,.18);transition:box-shadow .15s}' +
      '.snv-it:hover .snv-b{box-shadow:0 0 0 2px rgba(255,255,255,.7)}' +
      '.snv-it.on .snv-b{box-shadow:0 0 0 3px var(--g)}.snv-it.on .snv-n{color:var(--g);opacity:1;font-weight:800}' +
      '.snv-in{position:absolute;left:0;top:0;transform-origin:0 0;pointer-events:none;overflow:hidden}' +
      '.snv-in,.snv-in *{animation:none!important;transition:none!important;cursor:default!important}' +
      '.snv-in>*{position:absolute!important;left:0!important;top:0!important;right:auto!important;bottom:auto!important;margin:0!important;transform:none!important;opacity:1!important;visibility:visible!important;max-width:none!important;max-height:none!important;min-width:0!important;min-height:0!important}' +
      '.snv-in>img{width:100%!important;height:100%!important;object-fit:contain;display:block!important}' +
      '@media print{#snv,#snv-tab{display:none!important}}';
    document.head.appendChild(st);

    var de = document.documentElement;
    function setW() { de.style.setProperty('--snvw', Math.round(Math.max(150, Math.min(250, innerWidth * 0.42))) + 'px'); }
    setW(); addEventListener('resize', setW);

    var tab = document.createElement('button');
    tab.id = 'snv-tab'; tab.type = 'button'; tab.title = 'Danh sách slide (phím G)';
    tab.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>';
    var P = document.createElement('aside');
    P.id = 'snv'; P.setAttribute('aria-label', 'Danh sách slide');
    P.innerHTML = '<div class="snv-h"><b>Các slide</b><span id="snv-k"></span><button class="snv-x" type="button" title="Đóng (Esc)">✕</button></div><div class="snv-l"></div>';
    var L = q('.snv-l', P), K = q('#snv-k', P);
    var items = [], done = [];
    for (var k = 0; k < N; k++) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'snv-it'; b.dataset.k = k;
      b.innerHTML = '<span class="snv-n">' + (k + 1) + '</span><span class="snv-b" style="aspect-ratio:' + W + '/' + H + '"></span>';
      L.appendChild(b); items.push(b);
    }
    document.body.appendChild(P); document.body.appendChild(tab);

    // dựng ảnh nhỏ: nhân bản slide, bỏ id/name/script/âm thanh để không ảnh hưởng slide thật
    function thumb(k) {
      if (done[k]) return; done[k] = 1;
      var box = q('.snv-b', items[k]), bw = box.clientWidth || 180;
      var c = src(k).cloneNode(true);
      qa('script,audio,video,iframe,object,embed,canvas', c).forEach(function (e) { e.remove(); });
      [c].concat(qa('*', c)).forEach(function (e) {
        e.removeAttribute('id'); e.removeAttribute('name'); e.removeAttribute('autofocus'); e.removeAttribute('data-build-hidden');
        if (e.hasAttribute('loading')) e.removeAttribute('loading');
        if (e.classList) e.classList.remove('hid');
      });
      if (c.classList) c.classList.add('on');
      c.style.width = W + 'px'; c.style.height = H + 'px';
      if (T !== 'i') c.style.display = getComputedStyle(src(cur())).display === 'none' ? 'block' : getComputedStyle(src(cur())).display;
      var w = document.createElement('div');
      w.className = 'snv-in';
      w.style.cssText = font + 'width:' + W + 'px;height:' + H + 'px;transform:scale(' + (bw / W) + ')';
      w.appendChild(c); box.appendChild(w);
    }
    var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { thumb(+e.target.dataset.k); io.unobserve(e.target); } });
    }, { root: L, rootMargin: '400px 0px' }) : null;

    var last = -1;
    function mark(force) {
      var c = cur(); K.textContent = (c + 1) + ' / ' + N;
      if (c === last && !force) return;
      if (items[last]) items[last].classList.remove('on');
      items[c].classList.add('on'); last = c;
      if (de.classList.contains('snv-open')) {
        var it = items[c], lt = L.getBoundingClientRect(), r = it.getBoundingClientRect();
        if (r.top < lt.top + 8 || r.bottom > lt.bottom - 8) L.scrollTop += r.top - lt.top - (lt.height - r.height) / 2;
      }
    }
    var tick = null;
    function open(on) {
      de.classList.toggle('snv-open', on); LS.set('snv-open', on ? '1' : '0');
      clearInterval(tick);
      if (on) {
        if (io) items.forEach(function (it, k) { if (!done[k]) io.observe(it); }); else items.forEach(function (it, k) { thumb(k); });
        mark(true); tick = setInterval(mark, 350);
      }
    }
    tab.onclick = function () { open(!de.classList.contains('snv-open')); };
    window.__snvToggle = function () { open(!de.classList.contains('snv-open')); };
    q('.snv-x', P).onclick = function () { open(false); };
    L.addEventListener('click', function (e) { var b = e.target.closest('.snv-it'); if (b) go(+b.dataset.k); });
    // không để thao tác trong thanh bên lọt xuống slide (bấm/lướt chuyển trang)
    ['pointerdown', 'mousedown', 'touchstart', 'touchend', 'wheel'].forEach(function (t) {
      P.addEventListener(t, function (e) { e.stopPropagation(); }, { passive: true });
      tab.addEventListener(t, function (e) { e.stopPropagation(); }, { passive: true });
    });
    P.addEventListener('click', function (e) { e.stopPropagation(); });
    tab.addEventListener('click', function (e) { e.stopPropagation(); });
    document.addEventListener('keydown', function (e) {
      if (!e.isTrusted || e.ctrlKey || e.metaKey || e.altKey) return;
      var t = e.target; if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (e.key === 'g' || e.key === 'G') { open(!de.classList.contains('snv-open')); e.preventDefault(); e.stopImmediatePropagation(); }
      else if (e.key === 'Escape' && de.classList.contains('snv-open')) { open(false); }
    }, true);
    if (LS.get('snv-open') === '1' && innerWidth >= 900) open(true); else mark(true);
  }
  function start() { setTimeout(init, 60); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
