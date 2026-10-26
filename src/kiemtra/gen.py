import json,re,random,html
SP='/tmp/claude-0/-home-claude/53ce519d-fd2a-5897-9a15-9190297c3a0e/scratchpad/'
REPO=SP+'web/repo/'
s=open(REPO+'public/app/data/docs.js',encoding='utf-8').read();D=json.loads(s[s.index('=')+1:s.rindex(';')])
st=lambda x: re.sub('<rt>.*?</rt>|<[^>]+>','',x)
E=lambda x: html.escape(x or '',quote=False)
rnd=random.Random(44)
def mk(q,correct,dis,ex):
    o=[correct]+dis; idx=list(range(4)); rnd.shuffle(idx)
    return dict(q=q,o=[o[i] for i in idx],a=idx.index(0),ex=ex)
# ---- chữ Hán
KO={'天気':['でんき','てんぎ','てっき'],'昨日':['きの','きのお','ぎのう'],'晴れ':['ばれ','はり','はれい']}
KS=['冬','同じ','暑い','天気','晴れ','風','昨日','毎日','店','食堂']
KD={k['w']:k for k in D['kanji']['初級1'][20:40]}
kq=[]
for w in KS:
    k=KD[w]; sent=st(k['ex']['jp']).replace(w,f'<u>{w}</u>',1)
    kq.append(mk(f'<div class="sent jp">{sent}</div>',k['r'],KO.get(w,k['rd'][:3]),
       f'<b class="jp">{k["wr"]}</b> <span class="hv">{E(k["hv"])}</span> – {E(k["vi"])}. {E(k["ex"]["vi"])}'))
# ---- từ vựng: nghĩa tiếng Việt → chọn cách viết đúng
VO={'雷 / 雷が鳴る':('雷','かみなり',['かみなる','かなみり','がみなり'],'Sấm'),'静か(な)':('静か(な)','しずか(な)',['じずか(な)','しすか(な)','しづか(な)'],'Yên tĩnh')}
VS=['左に曲がる','道を渡る','信号','交差点','郵便局','駐車場','静か(な)','田舎','都会','雷 / 雷が鳴る']
VD={w['w']:w for w in D['vocab']['初級1'] if w['b'] in (4,5,6)}
vq=[]
for w in VS:
    x=VD[w]
    if w in VO: hw,r,rd,vi=VO[w]
    else: hw,r,rd,vi=w,x['r'],x['rd'][:3],x['vi']
    vq.append(mk(f'<div class="mean">「{E(vi)}」</div>',r,rd,
       f'<b class="jp">{x["wr"]}</b>{(" <span class=hv>"+E(x["hv"])+"</span>") if x.get("hv") else ""} – {E(x["vi"])} (Bài {x["b"]})'))
# ---- ngữ pháp
G=[p for p in D['gram']['初級1'] if p['bai'] in (5,6,7)]
GQ=[q for p in G for q in p['qz'][1:]]
GS=[0,2,3,4,5,7,8,9,10,15]
gq=[]
for i in GS:
    q=GQ[i]; n=len(q['o']); idx=list(range(n)); rnd.shuffle(idx)
    gq.append(dict(q=f'<div class="sent jp">{q["q"]}</div>'.replace('B：','<br>B：'),o=[q['o'][j] for j in idx],a=idx.index(q['a']),ex=q['ex']))
T=dict(id='buoi04',title='Kiểm tra Buổi 4',sub='Chữ Hán 初級1 21–40 · Từ vựng Bài 4–6 · Ngữ pháp Bài 5–7',
  secs=[dict(name='Chữ Hán',ins='Chọn cách đọc đúng của từ được gạch chân.',qs=kq),
        dict(name='Từ vựng',ins='Từ tiếng Nhật nào có nghĩa như sau? Chọn cách viết đúng.',qs=vq),
        dict(name='Ngữ pháp',ins='Chọn đáp án đúng.',qs=gq)])
import os,glob
os.makedirs(REPO+'kiemtra',exist_ok=True)
KEYD=dict(title=T['title'],secs=[dict(name=x['name'],n=len(x['qs'])) for x in T['secs']],key=[dict(a=q['a'],ex=q['ex']) for x in T['secs'] for q in x['qs']],
  qs=[re.sub('<rt>.*?</rt>|<[^>]+>','',q['q']).strip() for x in T['secs'] for q in x['qs']])
json.dump(KEYD,open(REPO+f'kiemtra/{T["id"]}.json','w'),ensure_ascii=False,indent=0)
ids=sorted(os.path.basename(p)[:-5] for p in glob.glob(REPO+'kiemtra/*.json'))
open(REPO+'kiemtra/tests.js','w').write('// SINH RA bởi scratch kt/gen.py – đáp án bài kiểm tra (KHÔNG nằm trong public/)\n'+''.join(f"import t{i} from './{x}.json';\n" for i,x in enumerate(ids))+'export default {'+','.join(f"'{x}':t{i}" for i,x in enumerate(ids))+'};\n')
PUB=dict(id=T['id'],title=T['title'],sub=T['sub'],secs=[dict(name=x['name'],ins=x['ins'],qs=[dict(q=q['q'],o=q['o']) for q in x['qs']]) for x in T['secs']])
tpl=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tpl.html')).read()
os.makedirs(REPO+'public/kiemtra',exist_ok=True)
open(REPO+'public/kiemtra/'+T['id']+'.html','w').write(tpl.replace('__TITLE__',T['title']).replace('__DATA__',json.dumps(PUB,ensure_ascii=False).replace('</','<\\/')))
print(len(KEYD['key']),'câu')
