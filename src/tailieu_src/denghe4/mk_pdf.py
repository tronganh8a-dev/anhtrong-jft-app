import json, re, html
d=json.load(open('/home/claude/anhtrong-jft-app/src/raw/jft_exams.json'))
e=next(x for x in d if x['id']=='jft-ln4')
fonts=open('/tmp/nh/fonts.css').read()
PUB='file:///home/claude/anhtrong-jft-app/public/'
SEC={'1':('もんだい1','課題理解 · Hiểu yêu cầu'),'2':('もんだい2','ポイント理解 · Nắm ý chính'),'3':('もんだい3','発話表現 · Cách nói theo tình huống'),'4':('もんだい4','即時応答 · Đáp nhanh')}
def part(ex,lb):
    m=re.search(r'<span class="lb">'+lb+r'</span><div[^>]*>(.*?)</div>',ex,re.S);return m.group(1) if m else ''
body='';cur=None
for q in e['qs']:
    m=re.search(r'ln4_(\d)(\d)',q['au']);sec,n=m.group(1),m.group(2)
    if sec!=cur:
        cur=sec;j,v=SEC[sec]
        body+=f'<div class="sec"><span class="jp">{j}</span> {v}</div>'
    qt=re.sub(r'<span class="lb">.*?</span><br>','',q['t'])
    ans=re.search(r'Đáp án đúng: <span class="jp">(.*?)</span></div>',q['ex'],re.S).group(1)
    opts=''
    if any(o.get('img') for o in q['o']):
        opts='<div class="pics">'+''.join(f'<div class="pc{" ok" if k==q["a"][0] else ""}"><img src="{PUB}{o["img"]}"><b>{k+1}</b></div>' for k,o in enumerate(q['o']))+'</div>'
    elif q['o'][0]['t'] not in ('1',):
        opts='<ol class="ops">'+''.join(f'<li class="{"ok" if k==q["a"][0] else ""}"><span class="jp">{o["t"]}</span></li>' for k,o in enumerate(q['o']))+'</ol>'
    scene=f'<img class="scene" src="{PUB}{q["img"]}">' if q.get('img') else ''
    body+=f'''<div class="q"><div class="qh"><span class="no">{n}番</span><div class="qt">{qt}</div><span class="an">Đáp án: {ans}</span></div>
{scene}{opts}
<div class="lb">SCRIPT</div><div class="sc jp">{part(q["ex"],"SCRIPT")}</div>
<div class="lb">DỊCH</div><div class="vi">{part(q["ex"],"DỊCH")}</div>
<div class="lb">GIẢI THÍCH</div><div class="gt">{part(q["ex"],"GIẢI THÍCH")}</div></div>'''
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
@page{{size:A4;margin:14mm 13mm 14mm}}
body{{font-family:'Be Vietnam Pro',Mali,sans-serif;font-family:Mali;font-weight:500;color:#0d2b40;font-size:10.5pt;line-height:1.55}}
.jp,.jp *{{font-family:'Klee One',serif;font-weight:600}}
rt{{font-size:.5em;font-family:'Klee One'}}
.cover{{display:flex;align-items:center;gap:16px;border-bottom:3px solid #c42f66;padding-bottom:10px;margin-bottom:12px}}
.cover img{{height:42px}}.cover h1{{font-size:20pt;margin:0;font-weight:700}}.cover p{{margin:2px 0 0;color:#47647a;font-size:10pt}}
.sec{{background:#0d5a8c;color:#fff;font-weight:700;font-size:13pt;padding:6px 14px;border-radius:10px;margin:16px 0 10px;break-after:avoid}}
.q{{border:1px solid #dfe7ee;border-radius:12px;padding:10px 14px;margin-bottom:12px;break-inside:auto}}.qh,.pics,.scene,.ops{{break-inside:avoid;break-after:avoid}}.lb{{break-after:avoid}}
.qh{{display:flex;align-items:flex-start;gap:10px}}.no{{background:#c42f66;color:#fff;font-weight:700;border-radius:8px;padding:2px 10px;white-space:nowrap}}
.qt{{flex:1}}.qt .vi-q{{color:#47647a;font-size:9.5pt}}.an{{background:#e6f5ee;color:#16784a;font-weight:700;border-radius:8px;padding:2px 10px;white-space:nowrap}}
.pics{{display:flex;gap:8px;margin:8px 0}}.pc{{position:relative;flex:1;border:2px solid #e3eaf1;border-radius:8px;overflow:hidden}}.pc img{{width:100%;display:block}}.pc b{{position:absolute;left:4px;top:2px;background:#0d2b40;color:#fff;border-radius:50%;width:20px;height:20px;font-size:9pt;display:flex;align-items:center;justify-content:center}}.pc.ok{{border-color:#1c9b5f}}
.scene{{width:52%;border-radius:8px;margin:8px 0;display:block}}
.ops{{margin:6px 0 6px 18px;padding:0}}.ops li.ok{{color:#16784a;font-weight:700}}
.lb{{display:inline-block;font-size:8pt;font-weight:700;letter-spacing:.5px;background:#fff3c4;color:#7a5b00;border-radius:5px;padding:1px 7px;margin-top:6px}}
.sc{{line-height:2.0;font-size:10.5pt}}.vi,.gt{{font-size:9.8pt}}
.foot{{margin-top:14px;font-size:8.5pt;color:#8aa0b2;border-top:1px solid #e3eaf1;padding-top:6px}}
</style></head><body>
<div class="cover"><img src="{PUB}app/media/brand/logo-ngang.svg"><div><h1>Đề nghe 4 · Script & Giải thích</h1><p>JLPT N4 聴解 · cấp độ tầm trung · 28 câu · đáp án, script, dịch, giải thích từng câu</p></div></div>
{body}
<div class="foot">© 2026 Anh Trọng Dạy JFT · Tài liệu dùng trong khoá học, vui lòng không chia sẻ ra ngoài. Dịch và giải thích do Anh Trọng Dạy JFT biên soạn.</div>
</body></html>'''
open('/tmp/ln4pdf/s.html','w').write(H)
