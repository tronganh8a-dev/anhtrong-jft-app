// Đề 30 (jft-y5, trên app hiện là "Đề 4"): dựng lại bài đọc thành ảnh rõ nét (chữ lấy theo video "JFT Mock Test #10 · いろどり 初級1 第10回")
// Chạy: cd /tmp/tk && node <repo>/src/jft/youtube/make5.js  → /tmp/y5/img/y5_rN.jpg
const {chromium}=require('playwright');
const css=`body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans CJK SC',sans-serif;color:#222}
.box{width:600px;padding:22px 26px;border:2px solid #bbb;background:#fffdf7;font-size:20px;line-height:1.9}
h3{text-align:center;margin:0 0 10px;font-size:22px}
table{border-collapse:collapse;width:100%;font-size:19px;line-height:1.5} td,th{border:1px solid #888;padding:6px 10px;text-align:left;vertical-align:middle} th{background:#eef0e6;text-align:center;white-space:nowrap} td.c{text-align:center;white-space:nowrap;width:70px}
.note{margin-top:10px;font-size:18px;line-height:1.7}
.chat{background:#e9eef2;padding:16px;border-radius:6px}.m{max-width:80%;padding:9px 13px;border-radius:12px;margin:9px 0;font-size:19px;line-height:1.6}
.r{background:#9be27a;margin-left:auto}.l{background:#fff}.t{font-size:12px;color:#556;display:block;line-height:1.2}
rt{font-size:.55em}`;
const P={
r1:`<h3>みどり町　1年の　イベント</h3><table><tr><th>月</th><th>イベント</th></tr><tr><td class="c">4月</td><td>お花見（みどり公園）</td></tr><tr><td class="c">7月</td><td>夏祭り・ぼんおどり（駅前広場）</td></tr><tr><td class="c">8月</td><td>花火大会（みどり川）</td></tr><tr><td class="c">10月</td><td>スポーツ大会（市民体育館）</td></tr><tr><td class="c">12月</td><td>もちつき（公民館）</td></tr></table>`,
r3:`<h3>さくら駅北口　→　さくら病院　（平日）</h3><table><tr><th>時</th><th>分</th></tr><tr><td class="c">7時</td><td>10　　40</td></tr><tr><td class="c">8時</td><td>05　　20　　50</td></tr><tr><td class="c">9時</td><td>30</td></tr><tr><td class="c">10時</td><td>30</td></tr></table><div class="note">※ 土・日は　1時間に　1本です。<br>※ 病院まで　15分</div>`,
r5:`<h3>さくら市　国際交流センター<br>「やさしい　日本語教室」</h3><div style="margin-bottom:10px">日本語を　いっしょに　勉強しませんか。どなたでも　参加できます。</div><table><tr><th>クラス</th><td>水曜日：夜　7:00～8:30<br>土曜日：朝　10:00～11:30</td></tr><tr><th>場所</th><td>市民センター　2かい　201</td></tr><tr><th>お金</th><td>1回　200円（はじめての　人は　無料）</td></tr><tr><th>もうしこみ</th><td>電話か　メールで、前の　日までに　れんらくして　ください。</td></tr><tr><th>持ち物</th><td>教科書は　いりません。ノートと　ペンを　持って　きて　ください。</td></tr></table>`,
r7:`<h3>コピー機が　こしょう　して　います</h3>2かいの　コピー機が　動きません。業者に　電話しました。あしたの　<ruby>午後<rt>ごご</rt></ruby>　直しに　来ます。<br>それまでは　3かいの　コピー機を　使って　ください。<br>カラーコピーが　必要な　人は、そうむ部の　田中に　言って　ください。`,
r9:`<h3>こまった　ときの　電話</h3><table><tr><th>番号</th><th>どんな　とき</th></tr><tr><td class="c">119</td><td>火事・きゅうきゅう車（急な　病気や　大きい　けが）</td></tr><tr><td class="c">110</td><td>けいさつ（じこ・どろぼう）</td></tr><tr><td class="c">#7119</td><td>きゅうきゅう車を　よぶか　どうか　わからない　とき、相談できます</td></tr></table><div class="note">電話では、「何が　ありましたか」「場所は　どこですか」と　聞かれます。ゆっくり　答えましょう。</div>`,
r11:`<div class="chat"><div class="m l">山田さんに　女の子が　生まれたそうです！<span class="t">メイ 12:10</span></div><div class="m r">わあ、よかったね。みんなで　お祝いを　あげない？<span class="t">えみ 12:11</span></div><div class="m l">いいですね。いくらぐらいが　いいでしょうか。<span class="t">メイ 12:12</span></div><div class="m r">会社の　人には　だいたい　一人　1,000円ぐらいかな。5人で　5,000円の　ものを　買おう。<span class="t">えみ 12:13</span></div><div class="m l">じゃあ、わたしが　金曜日に　デパートで　買って　来ます。<span class="t">メイ 12:14</span></div></div>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1.6});
for(const k in P){require('fs').writeFileSync('/tmp/y5/_p.html',`<!doctype html><meta charset="utf-8"><style>${css}</style><div class="box">${P[k]}</div>`);
 await p.goto('file:///tmp/y5/_p.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
 const el=await p.$('.box');await el.screenshot({path:`/tmp/y5/img/y5_${k}.jpg`,type:'jpeg',quality:88});}
await b.close()})();
