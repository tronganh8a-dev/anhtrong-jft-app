// Chụp từng slide (PNG) + dựng khung hình chuyển trang lật sách (JPEG) cho video ngữ pháp.
// Chạy trong thư mục có playwright (vd /tmp/tk): node render.js [/tmp/ngp]
const {chromium} = require('playwright');
const fs = require('fs');
const D = process.argv[2] || '/tmp/ngp';
const NF = 18; // 0,6 giây ở 30 fps
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + D + '/slides.html');
  await p.waitForFunction(() => document.body.dataset.ok);
  await p.waitForTimeout(600);
  fs.mkdirSync(D + '/png', {recursive: true});
  const ids = await p.$$eval('section.sl', a => a.map(x => x.id));
  for (const id of ids) await (await p.$('#' + id)).screenshot({path: `${D}/png/${id}.png`});
  // trang lật: trang cũ quay quanh mép trái, trang mới nằm dưới, có bóng
  const t = await b.newPage({viewport: {width: 1080, height: 1920}});
  await t.setContent(`<html><body style="margin:0;background:#fff;overflow:hidden">
  <div id="st" style="position:relative;width:1080px;height:1920px;perspective:5200px">
   <img id="nw" style="position:absolute;inset:0">
   <div id="sh" style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(0,0,0,0) 60%)"></div>
   <div id="pg" style="position:absolute;inset:0;transform-origin:0 50%;transform-style:preserve-3d;backface-visibility:hidden">
    <img id="od" style="position:absolute;inset:0"><div id="dk" style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(0,0,0,.45),rgba(0,0,0,0) 70%)"></div>
   </div></div></body></html>`);
  for (let i = 0; i < ids.length - 1; i++) {
    const dir = `${D}/tr/${String(i + 1).padStart(2, '0')}`;
    fs.mkdirSync(dir, {recursive: true});
    const a = fs.readFileSync(`${D}/png/${ids[i]}.png`).toString('base64');
    const n = fs.readFileSync(`${D}/png/${ids[i + 1]}.png`).toString('base64');
    await t.evaluate(([a, n]) => new Promise(r => {
      let k = 0; const od = document.getElementById('od'), nw = document.getElementById('nw');
      od.onload = nw.onload = () => (++k == 2) && r();
      od.src = 'data:image/png;base64,' + a; nw.src = 'data:image/png;base64,' + n;
    }), [a, n]);
    for (let f = 1; f <= NF; f++) {
      const x = f / NF, e = x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
      await t.evaluate(e => {
        document.getElementById('pg').style.transform = `rotateY(${-92 * e}deg)`;
        document.getElementById('dk').style.opacity = Math.min(1, e * 1.6);
        document.getElementById('sh').style.opacity = (1 - e) * .9;
        document.getElementById('pg').style.visibility = e > .985 ? 'hidden' : 'visible';
      }, e);
      await t.screenshot({path: `${dir}/f${String(f).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 92});
    }
  }
  await b.close();
  console.log('ok', ids.length);
})();
