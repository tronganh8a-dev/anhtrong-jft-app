import sys, re, json, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ext import page_lines
import pymupdf as fitz
d=fitz.open(os.environ.get('N3PDF','n3.pdf'))
K=[15,31,45,60,84,100,115,128,141,156,170,185,199,213,228,240,252,265,278,292,306,326,340,355,368,381]
NAMES=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','16b','17','18','19','20','21','22','23','25','26']
RANGES=[];st=1
for k in K: RANGES.append((st,k-1)); st=k+2
RANGES[22]=(329,339)  # N3-22 (key N3-21 spans 326-328)
ROM={'Ⅰ':1,'Ⅱ':2,'Ⅲ':3,'Ⅳ':4,'Ⅴ':5,'Ⅵ':6,'Ⅶ':7,'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'ⅤＩ':6,'ⅤＩＩ':7,'VＩ':6}
QRE=re.compile(r'^[［\[「〔【｢]\s*([\d０-９]{1,2})\s*[］\]」〕】｣]\s*(.*)$')
ORE=re.compile(r'[①②③④]')
SECRE=re.compile(r'^(?:[＊*]+\s*)?問題\s*([ⅠⅡⅢⅣⅤⅥⅦIV]+|ⅤＩＩ|ⅤＩ)\s*(?:[（(]\s*\d\s*[)）])?\s*[:：]?\s*(.*)$')
def strip(t): return re.sub(r'<[^>]+>','',t)
def lines_of(a,b):
    L=[]
    for pn in range(a,b+1):
        for x in page_lines(d[pn-1]):
            t=x['t']; p=strip(t).strip()
            if x['y']>670 and re.fullmatch(r'\d{1,3}',p): continue
            if re.fullmatch(r'N3\s*-?\s*\d+b?',p) or p in ('N3',): continue
            if re.fullmatch(r'[-‐－]?\s*\d{1,2}\s*[-‐－]?\s*(N3\s*[-‐－]\s*\d+)?\s*(【読解】)?',p) or p=='【読解】': continue
            if re.match(r'^[＊*]*\s*問題\s*\d+\s*[（(]\s*\d+\s*[)）]\s*$',p): continue
            if re.match(r'^(団体名|企業名|名前)\s*[:：]?\s*$',p) or re.match(r'^(団体名|企業名)',p): continue
            if re.search(r'言語知識|語彙知識|配点',p) and len(p)<40 and not QRE.match(p): 
                L.append(dict(kind='hdr',t=t,p=p,pn=pn,col=x['col'],y=x['y'],x=x['x']));continue
            L.append(dict(kind='txt',t=t,p=p,pn=pn,col=x['col'],y=x['y'],x=x['x']))
    return L
def split_opts(t):
    parts=re.split(r'([①②③④])',t)
    out=[];cur=None
    for s in parts:
        if s in '①②③④' and s: cur=s;out.append('')
        elif cur is not None: out[-1]+=s
    return [re.sub(r'^\s+|\s+$','',o).strip('　 ') for o in out], parts[0]
def parse(ix):
    a,b=RANGES[ix]; L=lines_of(a,b)
    lastopt=False; part='A'; sec=None; qs=[]; groups=[]; buf=[]; ins={}; cur=None; maxn=0
    for ln in L:
        p=ln['p']; t=ln['t']
        if ln['kind']=='hdr':
            if '文法' in p or '読解' in p and '文字' not in p:
                if maxn>=20: part='B'
            continue
        m=SECRE.match(p)
        if m:
            r=m.group(1); sec=ROM.get(r,r)
            if part=='A' and maxn>=20 and sec==1: part='B'
            key=(part,sec)
            if buf and qs and qs[-1]['part']==part and qs[-1]['grp'] is not None: groups[qs[-1]['grp']]['html']+=buf; 
            buf=[]
            ins.setdefault(key,m.group(2)); cur=None; ln['ins']=1; continue
        mq=QRE.match(t.replace('<u>','').replace('</u>','')) if not ORE.match(p) else None
        if mq is None:
            mq2=QRE.match(p)
            if mq2 and not p.startswith(('①','②','③','④')): mq=mq2
        if mq:
            n=int(mq.group(1).translate(str.maketrans('０１２３４５６７８９','0123456789'))); rest=t[t.find(re.search(r'[］\]」〕】｣]',t).group(0))+1:].strip() if re.search(r'[］\]」〕】｣]',t) else mq.group(2)
            if part=='A' and maxn>=20 and n<=2: part='B'
            maxn=max(maxn,n) if part=='A' else maxn
            grp=None
            if part=='B' and sec and sec>=3:
                if buf or not qs or qs[-1]['grp'] is None or qs[-1]['sec']!=sec:
                    groups.append(dict(sec=sec,html=buf)); buf=[]
                grp=len(groups)-1
            cur=dict(part=part,sec=sec,n=n,stem=rest,opts=[],grp=grp,pn=ln['pn'])
            pr=strip(rest)
            if ORE.search(rest) and not (len(ORE.findall(pr))==1 and re.search(r'(か|か。|とあるが.*|ですか。?)\s*$',pr)):
                o,pre=split_opts(rest); cur['stem']=pre.strip(); cur['opts']=o
            qs.append(cur); continue
        if ORE.match(p) and cur is not None and len(cur['opts'])<4:
            o,_=split_opts(t); cur['opts']+=o; lastopt=True; continue
        if lastopt and cur is not None and len(cur['opts'])==4 and len(p)<=12 and not re.search(r'[【】]|^[-‐－]\s*\d|問題',p):
            cur['opts'][-1]+=t; lastopt=False; continue
        lastopt=False
        if cur is not None and len(cur['opts'])==0:
            cur['stem']+=('<br>' if cur['stem'] else '')+t; continue
        if cur is not None and 0<len(cur['opts'])<4 and not ORE.match(p):
            cur['opts'][-1]+=t; continue
        # instructions continuation
        if re.search(r'(選びなさい|答えなさい|選んでください)。?\s*$',p) and len(p)<45 and not buf:
            continue
        buf.append(ln)
    if buf and groups: groups[-1]['html']+=buf
    return dict(name=NAMES[ix],qs=qs,groups=[dict(sec=g['sec'],lines=[(l['pn'],l['col'],l['x'],l['y'],l['t']) for l in g['html']]) for g in groups],ins={f'{k[0]}{k[1]}':v for k,v in ins.items()})
if __name__=='__main__':
    ix=int(sys.argv[1]); R=parse(ix)
    json.dump(R,open(os.path.dirname(os.path.abspath(__file__))+f'/../raw/e{ix+1:02d}.json','w'),ensure_ascii=False,indent=0)
    for q in R['qs']:
        print(f"{q['part']}{q['sec']} [{q['n']}] g{q['grp']} | {strip(q['stem'])[:70]} || "+' / '.join(strip(o)[:25] for o in q['opts']))
    for i,g in enumerate(R['groups']):
        print('--- G',i,'sec',g['sec'],len(g['lines']),'lines:',' '.join(strip(l[4]) for l in g['lines'])[:300])
