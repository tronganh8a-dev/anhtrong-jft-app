const {chromium}=require('playwright');
const css=`body{margin:0;background:#fff;font-family:'Noto Sans CJK JP','Noto Sans CJK SC',sans-serif;color:#222}
.box{width:600px;padding:22px 26px;border:2px solid #bbb;background:#fffdf7;font-size:20px;line-height:1.9}
h3{text-align:center;margin:0 0 8px;font-size:22px} .src{font-size:15px;float:right;color:#555}
table{border-collapse:collapse;width:100%;font-size:18px;line-height:1.5} td,th{border:1px solid #888;padding:6px 8px;text-align:left;vertical-align:middle} td:first-child,th:first-child{white-space:nowrap} th{background:#eef0e6;text-align:center}
.chat{background:#e9eef2;padding:16px;border-radius:6px}.m{max-width:78%;padding:9px 13px;border-radius:12px;margin:9px 0;font-size:19px;line-height:1.6}
.r{background:#9be27a;margin-left:auto}.l{background:#fff}.t{font-size:12px;color:#556;display:block;line-height:1.2}.hd{font-size:15px;color:#444;border-bottom:1px solid #ccc;padding-bottom:6px;margin-bottom:8px}`;
const P={
r1:`<table><tr><th>名前</th><td>ソカ</td></tr><tr><th>国</th><td>カンボジア（プノンペン）</td></tr><tr><th>日本に　来た　とき</th><td>去年の　4月</td></tr><tr><th>仕事</th><td>介護（老人ホーム）</td></tr><tr><th>すきな　こと</th><td>歌を　歌う　こと、料理</td></tr><tr><th>ひとこと</th><td>日本の　歌を　たくさん　おぼえたいです！</td></tr></table>`,
r3:`<div class="chat"><div class="m l">外、すごい　雨ですよ！<span class="t">山本 17:40</span></div><div class="m r">え、本当ですか。かさを　持って　来ませんでした……。<span class="t">リン 17:41</span></div><div class="m l">受付に　かさが　ありますよ。会社の　かさは　だれでも　使えます。<span class="t">山本 17:42</span></div><div class="m l">あした　受付に　返して　くださいね。<span class="t">山本 17:42</span></div><div class="m r">ありがとうございます！<span class="t">リン 17:43</span></div></div>`,
r5:`<h3>国際フェスティバル　スタッフ　予定（10日）</h3><table><tr><th>名前</th><th>仕事</th><th>時間</th></tr><tr><td>ミン</td><td>受付</td><td>9:30〜12:00</td></tr><tr><td>アナ</td><td>食べ物の　店</td><td>11:00〜15:00</td></tr><tr><td>ロン</td><td>ステージの　準備</td><td>8:30〜10:00</td></tr><tr><td>ソカ</td><td>かたづけ</td><td>15:00〜17:00</td></tr></table><div style="margin-top:10px">※イベントは　10時から　15時まで。スタッフは　仕事が　始まる　15分前に　ホールに　来て　ください。</div>`,
r7:`<div class="hd">差出人：長谷川　｜　件名：来週の　バーベキュー</div>みなさん<br>来週　土曜日の　バーベキューの　準備に　ついてです。<br>・肉と　野菜：楊さんが　買って　行きます。<br>・飲み物：マルコさんに　お願いしました。ビールと　お茶です。<br>・おにぎり：私（長谷川）が　作って　行きます。<br>・デザート：ノイさんが　バナナを　持って　来ます。<br>コップや　お皿は　バーベキュー場に　ありますから、持って　来なくても　だいじょうぶです。<br>集合は　10時に　みどり公園の　入口です。雨の　ときは　中止です。前の　日の　夜8時に　メールで　連絡します。`,
r9:`<h3>休暇届の　書き方</h3>①いちばん　上の「所属」に、チームの　名前を　書きます。<br>②その　下の「氏名」に　名前を　書いて、名前の　横に　ハンコを　おします。<br>③「期間」に　休む　日を　書きます。<br>④「理由」に　休む　理由を　書きます。<br>⑤休む　日の　1週間前までに、総務の　田中さんに　出して　ください。<br>　急に　病気で　休む　ときは、朝　8時までに　電話で　連絡して　ください。`,
r11:`<div class="chat"><div class="m l">最近、体が　重くて……。何か　運動して　る？<span class="t">ホセ 20:30</span></div><div class="m r">わたしは　週に　2回　ジムに　行って、毎朝　30分　歩いて　るよ。<span class="t">リン 20:32</span></div><div class="m r">それと、夜は　ご飯を　食べすぎないように　して　る。<span class="t">リン 20:32</span></div><div class="m l">すごいね。ぼくも　いっしょに　ジムに　行っても　いい？<span class="t">ホセ 20:33</span></div><div class="m r">もちろん！　今度の　土曜日、行こう。<span class="t">リン 20:34</span></div></div>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1.6});
for(const k in P){await p.setContent(`<style>${css}</style><div class="box">${P[k]}</div>`);const el=await p.$('.box');await el.screenshot({path:`/tmp/yt3/img/y3_${k}.jpg`,type:'jpeg',quality:88});}
await b.close();})();
