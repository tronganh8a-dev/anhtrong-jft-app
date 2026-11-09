const {chromium}=require('playwright');
const css=`body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans CJK SC',sans-serif;color:#222}
.box{width:600px;padding:22px 26px;border:2px solid #bbb;background:#fffdf7;font-size:20px;line-height:1.9}
h3{text-align:center;margin:0 0 8px;font-size:22px} .src{font-size:15px;float:right;color:#555}
table{border-collapse:collapse;width:100%;font-size:18px;line-height:1.5} td,th{border:1px solid #888;padding:6px 8px;text-align:left;vertical-align:middle} td:first-child{white-space:nowrap} th{background:#eef0e6;text-align:center}
.chat{background:#e9eef2;padding:16px;border-radius:6px}.m{max-width:78%;padding:9px 13px;border-radius:12px;margin:9px 0;font-size:19px;line-height:1.6}
.r{background:#9be27a;margin-left:auto}.l{background:#fff}.t{font-size:12px;color:#556;display:block;line-height:1.2}`;
const P={
r1:`<h3>新しい　仲間を　しょうかいします</h3>はじめまして。グエン・ミンです。ベトナムの　ハノイから　来ました。日本に　来て、3か月に　なります。<br>今、せいぞう部で　働いて　います。仕事は　まだ　わからない　ことが　多いですが、みなさん　親切なので、毎日　楽しいです。<br>しゅみは　サッカーです。休みの　日は　公園で　友だちと　サッカーを　します。いっしょに　やりませんか。<br>どうぞ　よろしく　お願いします。`,
r3:`<h3>今週の　天気</h3><table><tr><th>日</th><th>天気</th><th>最高気温</th><th>雨の　確率</th></tr><tr><td>月</td><td>晴れ</td><td>18度</td><td>10%</td></tr><tr><td>火</td><td>くもり</td><td>15度</td><td>40%</td></tr><tr><td>水</td><td>雨</td><td>12度</td><td>90%</td></tr><tr><td>木</td><td>雨のち晴れ</td><td>16度</td><td>60%</td></tr><tr><td>金</td><td>晴れ</td><td>20度</td><td>0%</td></tr></table>`,
r5:`<div class="chat"><div class="m r">ごめんなさい！道に　まよって、ちょっと　おくれます。<span class="t">ラン 18:33</span></div><div class="m r">今、さくら駅の　北口に　います。<span class="t">ラン 18:33</span></div><div class="m l">だいじょうぶ？　待ち合わせは　南口の　改札だよ。<span class="t">ゆか 18:34</span></div><div class="m r">え、そうですか！　じゃあ、すぐ　南口に　行きます。10分ぐらいで　着くと　思います。<span class="t">ラン 18:35</span></div><div class="m l">わかった。映画は　7時からだから、まだ　だいじょうぶ。改札の　前の　本屋で　待ってるね。<span class="t">ゆか 18:36</span></div></div>`,
r7:`<h3>さくら公民館　秋の　教室</h3><table><tr><th>教室</th><th>日時</th><th>お金</th><th>持ち物</th></tr><tr><td>ヨガ</td><td>毎週　火曜日<br>10:00〜11:00</td><td>1回 500円</td><td>タオル・水</td></tr><tr><td>料理</td><td>第1・第3　木曜日<br>18:30〜20:30</td><td>1回 800円</td><td>エプロン</td></tr><tr><td>書道</td><td>毎週　土曜日<br>14:00〜15:30</td><td>1回 600円</td><td>いりません<br>（道具は　かします）</td></tr><tr><td>合気道</td><td>毎週　日曜日<br>9:00〜10:30</td><td>1か月 2,000円</td><td>運動できる　服</td></tr></table>`,
r9:`<h3>ごみの　出し方</h3><table><tr><th>ごみ</th><th>注意</th><th>出す日</th></tr><tr><td>もえる　ごみ</td><td>紙・食べ物の　ごみ</td><td>毎日</td></tr><tr><td>ペットボトル</td><td>ふたと　ラベルを　とって、中を　あらって　ください</td><td>火・金</td></tr><tr><td>かん・びん</td><td>中を　あらって　ください</td><td>水</td></tr><tr><td>大きい　ごみ</td><td>そうむ部に　連絡して　ください</td><td>―</td></tr></table>`,
r11:`<h3>ノロウイルスに　気を　つけましょう<span class="src">―市の保健センター</span></h3>最近、ノロウイルスに　よる　食中毒が　ふえて　います。カキ　などの　貝を　生で　食べたり、よく　加熱しないで　食べたり　すると、かんせんする　ことが　あります。かんせんすると、おなかが　いたく　なったり、はいたり　します。<br><br><b>よぼうの　ために</b><br>・料理の　前と　トイレの　あとは、せっけんで　よく　手を　あらいましょう。<br>・貝は　中まで　よく　加熱して　食べましょう（85〜90度で　90秒　以上）。<br>・具合が　悪い　ときは、料理を　しないように　しましょう。`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1.6});
for(const k in P){await p.setContent(`<style>${css}</style><div class="box">${P[k]}</div>`);const el=await p.$('.box');await el.screenshot({path:`/tmp/yt/img/y1_${k}.jpg`,type:'jpeg',quality:88});}
await b.close();})();
