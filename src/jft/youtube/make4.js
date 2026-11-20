// Đề 29 (jft-y4): dựng lại bài đọc thành ảnh rõ nét (chữ lấy theo video đề, sửa vài lỗi chính tả rõ ràng)
// Chạy: cd /tmp/tk && node <repo>/src/jft/youtube/make4.js  → /tmp/y4/img/y4_rN.jpg  (cần /tmp/y4/img/y4_r2p.png, y4_r7m.png, y4_r8i.png — ảnh minh hoạ cắt từ video)
const {chromium}=require('playwright');
const css=`body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans CJK SC',sans-serif;color:#222}
.box{width:640px;padding:22px 26px;border:2px solid #bbb;background:#fffdf7;font-size:20px;line-height:1.9}
.u{text-decoration:underline;font-weight:700}
.dlg{display:grid;grid-template-columns:auto 1fr;column-gap:10px;row-gap:4px}.dlg b{white-space:nowrap}
.bub{background:#f6c94a;border-radius:50%;padding:46px 54px;font-size:21px;line-height:1.9;text-align:center}
.mail{border:1px dashed #555;padding:16px 20px;background:#fff}.mail .sb{font-size:20px;font-weight:700;text-decoration:underline;margin-bottom:6px}
.mails{display:flex;gap:18px}.ph{flex:1;border:6px solid #9aa3ab;border-radius:16px;padding:12px 16px;background:#fff;font-size:18px;line-height:1.8}
.ph .sb{border-bottom:1px solid #888;padding-bottom:4px;margin-bottom:6px}
.row{display:flex;gap:16px;align-items:flex-start}.row img{border:1px solid #ccc}
.card{display:flex;gap:16px;border:1px solid #aaa;border-radius:10px;padding:14px 16px;background:#fff}.card .t{flex:1;line-height:2;white-space:nowrap}.card .t span{border-bottom:1px solid #444}
.r{font-size:15px;color:#333;line-height:1.6}
rt{font-size:.55em}
.lf{display:flex;width:760px;border:1px solid #bbb;font-size:17px}
.lf .l{background:#f39a33;color:#fff;padding:14px 14px;width:250px;line-height:1.9}.lf .l h4{margin:0 0 8px;font-size:28px;letter-spacing:2px}
.lf .l div{white-space:nowrap}.lf .l small{font-size:13px}
.lf .m{flex:1;background:#fdf6ea;padding:12px 14px;position:relative}
.st{display:inline-block;width:34px;height:34px;border:1.5px solid #888;background:#fff;text-align:center;line-height:32px;font-weight:700;margin:0 2px}
.grid{display:grid;grid-template-columns:150px 1fr 120px;gap:10px;align-items:center;margin-top:6px}
.food{text-align:center;font-weight:700}.food .st{margin:4px 3px}
.min{display:flex;flex-direction:column;align-items:center;gap:4px;font-weight:700}
.eat{width:120px;height:120px;border-radius:50%;border:1.5px solid #888;background:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;text-align:center}
.stage{height:150px;border:1.5px solid #888;background:#fff;writing-mode:vertical-rl;display:flex;align-items:center;justify-content:center;font-weight:700;letter-spacing:4px}
.sch{margin-top:10px;line-height:1.7}`;
const P={
r1:`<div class="u">カーラさんは、1989年にフランスで生まれました。</div>子供の時、お父さんに日本の絵本をもらってから、日本にきょうみを持ちました。高校の時、家族と日本に旅行に行ってから、もっと日本が好きになりました。高校を卒業するまで、一人で日本語を勉強しました。大学に入学して、日本語と日本の文化をせんこうしました。2014年に日本の大学院に留学して、日本に住んでいます。`,
r2:`<div class="row"><div class="dlg" style="flex:1"><b>中村さん：</b><span>ルパさん、キムさん、京都ははじめてですか。</span><b>ルパ　　：</b><span>私ははじめてです。どうぞよろしくお願いいたします。</span><b>キム　　：</b><span>私は二回目です。去年の秋、妹と二人で来ました。でも、春もいいですね。</span><b>中村さん：</b><span>ええ。京都はいつ来ても楽しめますよ。</span><b>キム　　：</b><span>中村さんは何回目ですか。</span><b>中村さん：</b><span>私はたぶん7回目です。京都は何を食べてもおいしいし、どこに行っても日本的なふんいきがあるし、いいですよ。</span></div><img src="file:///tmp/y4/img/y4_r2p.png" width="170"></div>`,
r3:`<div class="bub">私は去年の父の日に父に青いシャツをあげました。<br>青は父が好きな色です。<br>今年は青いネクタイをあげます。</div>`,
r4:`<div class="mail"><div class="sb">件名：日本まつりのボランティア</div>ふじいのりかさま<br>はじめまして。私はフリオ・ゴンサレスといいます。日本まつりのボランティアをしたいと思います。私は日本語と日本文化にとてもきょうみがあります。かんじはあまり読めませんが、かんたんな日本語だったら、話せます。頑張りますので、よろしくお願いします。<div style="text-align:right">フリオ・ゴンサレス</div></div>`,
r5:`メロスはおこりました。悪いおうさまをゆるせないと思いました。メロスはむずかしいことがわかりません。メロスはむらで楽しく生活をしていました。しかし、メロスは悪いことをゆるせません。メロスはむらからシラクスと言う町に来ました。メロスにはお父さんもお母さんもいません。奥さんもいません。16才の妹と二人で生活をしています。妹はもうすぐ結婚します。メロスは結婚式のよういのために買い物をしに町に来たのです。町を歩いていると、メロスは町がおかしいと思いました。前に来た時より、町がとてもしずかなのです。そこで、メロスは町の人に聞きました。`,
r6:`<div class="mails"><div class="ph"><div class="sb">件名：おくれます</div>すみません。<br><span style="text-decoration:underline">バスの　じこで、30分ぐらい</span>　おくれます。<br>じゃあ、また　あとで。</div><div class="ph"><div class="sb">件名：Re：おくれます</div>わかりました。<br>きを　つけて　来て　ください。</div></div>`,
r7:`<div class="card"><div class="t"><span>レストラン「ハンナ」</span><br><span>「ハンナ」は　洋食の　レストランです。</span><br><span>料理が　安くて　おいしいので、よく　行きます。</span><br><span>この　店で　私が　いつも　食べるのは、</span><br><span>テリヤキビーフです。</span><br><span>肉と　ソースが　とても　おいしいです。</span><br>よかったら、行ってみて　ください。</div><div><div class="r">URL：http://www.hannah.xx<br>TEL：0XX-1234-5678</div><img src="file:///tmp/y4/img/y4_r7m.png" width="230"></div></div>`,
r8:`<div class="row"><div class="dlg" style="flex:1;font-size:19px"><b>いしかわ：</b><span>はじめまして。いしかわいちろうです。<br>いちろうは　1番目の　男の子と　いう　意味です。</span><b>ケイト　：</b><span>いしかわさんは　何人きょうだいですか。</span><b>いしかわ：</b><span>いもうとが　2人　います。<br>上の　いもうとは　<ruby>大阪<rt>おおさか</rt></ruby>に　住んでいます。<br>下の　いもうとは　さいたまと　いう　ところに　います。</span><b>ケイト　：</b><span>そうですか。</span></div><img src="file:///tmp/y4/img/y4_r8i.png" width="200"></div>`,
r9:`<div class="dlg"><b>男：</b><span>夏休みはどこへ行くんですか。</span><b>女：</b><span>北海道へ行きたいです。</span><b>男：</b><span>いいですね。ひこうきですか。</span><b>女：</b><span>ええ。さいしょはふねかバスで行こうと思ったんです。でも、時間がかかりすぎますから……。むこうに着いたら、車を借りるつもりです。</span></div>`,
r10:`<div class="lf"><div class="l"><h4>YOOKOSO!</h4><div>① 韓国料理 <small>（チヂミ）</small></div><div>② ロシア料理 <small>（ピロシキ）</small></div><div>③ メキシコ料理 <small>（タコス）</small></div><div>④ ドイツ料理 <small>（ソーセージ）</small></div><div>⑤ マレーシア料理 <small>（ムルタバ）</small></div><div>⑥ スペイン民芸品 <small>（ししゅう）</small></div><div>⑦ 日本民芸品 <small>（こけし）</small></div><div>⑧ フィリピン民芸品 <small>（アクセサリー）</small></div></div>
<div class="m"><div class="food"><ruby>世界<rt>せかい</rt></ruby>の<ruby>料理<rt>りょうり</rt></ruby><br><span class="st">5</span><span class="st">4</span><span class="st">3</span><span class="st">2</span><span class="st">1</span></div>
<div class="grid"><div class="min"><span><ruby>世界<rt>せかい</rt></ruby>の<ruby>民芸品<rt>みんげいひん</rt></ruby></span><span class="st">6</span><span class="st">7</span><span class="st">8</span></div><div style="display:flex;justify-content:center"><div class="eat"><ruby>食事<rt>しょくじ</rt></ruby><br>コーナー</div></div><div class="stage">ステージ</div></div>
<div class="sch"><b>★ ステージ</b>（世界の　うたと　おどり）<br>10：00～10：30　タイのダンス<br>11：00～11：30　フランスの　うた<br>14：00～14：30　日本語ミニレッスン</div></div></div>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1.6});
for(const k in P){const bare=k==='r3'||k==='r6'||k==='r10';const wide=['r7','r2','r8'].includes(k)?' style="width:760px"':'';require('fs').writeFileSync('/tmp/y4/_p.html',`<!doctype html><meta charset="utf-8"><style>${css}</style><div class="box"${bare?' style="border:0;background:#fff;width:auto;display:inline-block"':wide}>${P[k]}</div>`);await p.goto('file:///tmp/y4/_p.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
 const el=await p.$('.box');await el.screenshot({path:`/tmp/y4/img/y4_${k}.jpg`,type:'jpeg',quality:88});}
await b.close();})();
