// HTML → PDF A4 có chân trang (tên lớp + số trang). Dùng: node handout_pdf.js in.html out.pdf "Lớp cơ bản JFT · Buổi 3"
const {chromium} = require('playwright');
(async () => {
  const [inp, out, label] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + inp, {waitUntil: 'load'}); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  await p.pdf({path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font-family:sans-serif;font-size:7.5px;color:#6b8296;padding:0 13mm;display:flex;justify-content:space-between"><span>Anh Trọng Dạy JFT · ${label || ''}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
    margin: {top: '14mm', bottom: '16mm', left: '13mm', right: '13mm'}});
  await b.close();
})();
