const {chromium}=require('playwright');
const css=`body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans CJK SC',sans-serif;color:#222}
.box{width:600px;padding:22px 26px;border:2px solid #bbb;background:#fffdf7;font-size:20px;line-height:1.9}
h3{text-align:center;margin:0 0 8px;font-size:22px} .src{font-size:15px;float:right;color:#555}
table{border-collapse:collapse;width:100%;font-size:18px;line-height:1.5} td,th{border:1px solid #888;padding:6px 8px;text-align:left;vertical-align:middle} td:first-child{white-space:nowrap} th{background:#eef0e6;text-align:center}
.chat{background:#e9eef2;padding:16px;border-radius:6px}.m{max-width:78%;padding:9px 13px;border-radius:12px;margin:9px 0;font-size:19px;line-height:1.6}
.r{background:#9be27a;margin-left:auto}.l{background:#fff}.t{font-size:12px;color:#556;display:block;line-height:1.2}.hd{font-size:15px;color:#444;border-bottom:1px solid #ccc;padding-bottom:6px;margin-bottom:8px}`;
const P={
r1:`<div class="chat"><div class="m l">リンさん、お久しぶりです！　元気ですか。<span class="t">アナ 10:02</span></div><div class="m l">私は　先月から　大阪の　ホテルで　働いて　います。仕事は　いそがしいですが、楽しいです。<span class="t">アナ 10:03</span></div><div class="m r">アナさん！　お久しぶりです。元気ですよ。わたしは　今も　東京の　工場で　働いて　います。<span class="t">リン 10:15</span></div><div class="m l">来月、東京に　行きます。いっしょに　ご飯を　食べませんか。<span class="t">アナ 10:16</span></div></div>`,
r3:`<div class="hd">差出人：そうむ部　｜　件名：台風に　ついて</div>みなさん<br>あした　台風が　来ます。朝から　雨と　風が　とても　強く　なるでしょう。<br>あしたは　会社を　休みに　します。家から　出ないで　ください。<br>あさって　会社が　あるか　どうかは、あしたの　夜　7時に　メールで　連絡します。`,
r5:`<div class="hd">差出人：田中　｜　件名：あしたの　工場見学</div>みなさん<br>あしたは　工場見学です。朝　8時に　会社の　門の　前に　集まって　ください。バスで　行きます。<br>工場では　写真を　とらないで　ください。昼ご飯は　工場の　食堂で　食べますから、おべんとうは　いりません。<br>会社に　もどるのは　4時ごろです。`,
r7:`<h3>茶道　体験教室</h3>日本の　お茶を　体験して　みませんか。<br>日時：6月8日（日）　①10:00〜11:00　②14:00〜15:00<br>定員：それぞれ　10人<br>お金：無料（お菓子が　つきます）<br>申し込み：6月1日までに、公民館の　受付で　名前と　電話番号を　書いて　ください。電話では　申し込めません。<br>※くつしたを　はいて　来て　ください。`,
r9:`<div class="chat"><div class="m l">アリさん、すみません。倉庫の　トイレットペーパーが　なくなりました。<span class="t">上司 13:05</span></div><div class="m l">3時までに　駅前の　ドラッグストアで　買って来て　くれる？　10こ　お願いします。<span class="t">上司 13:05</span></div><div class="m l">お金は　あとで　返します。レシートを　もらって　来て　ね。<span class="t">上司 13:06</span></div><div class="m r">わかりました。<span class="t">アリ 13:07</span></div></div>`,
r11:`<h3>よく　ねむる　ための　5つの　ポイント</h3>①毎日　同じ　時間に　起きる<br>②寝る　前の　3時間は　食べすぎない<br>③寝る　前に　ぬるい　お風呂に　入る（38〜40度）<br>④寝る　前に　スマホを　見ない<br>⑤夕方より　あとは　コーヒーを　飲まない`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1.6});
for(const k in P){await p.setContent(`<style>${css}</style><div class="box">${P[k]}</div>`);const el=await p.$('.box');await el.screenshot({path:`/tmp/yt2/img/y2_${k}.jpg`,type:'jpeg',quality:88});}
await b.close();})();
