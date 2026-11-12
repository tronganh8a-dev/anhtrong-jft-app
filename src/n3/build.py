"""Dựng dữ liệu tab JLPT N3 → public/n3/data/. Nguồn: raw/eXX.json (trích từ PDF "26 đề thi N3"),
raw/keys_raw.json (bảng đáp án trong PDF), ans/eXX.txt (đáp án đã kiểm tra + dịch + giải thích),
fix/eXX.json (sửa tay phần trích). Ảnh bài đọc dạng bảng cắt từ PDF (cần biến N3PDF) → public/n3/img/."""
import json, re, os, html, sys, glob
H=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=H+'../../public/n3/'
os.makedirs(OUT+'data',exist_ok=True); os.makedirs(OUT+'img',exist_ok=True)
NAMES=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','16b','17','18','19','20','21','22','23','25','26']
KEYS=json.load(open(H+'raw/keys_raw.json'))
# PDF có 26 bộ nhưng N3-2 trùng hệt N3-1, N3-16b trùng N3-16 → 24 đề. ORDER[k-1] = chỉ số bộ trong PDF (1–26) của Đề k.
ORDER=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26]
SEC={('A',1):('文字・語彙','漢字読み','<u>＿＿</u>の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('A',2):('文字・語彙','表記','<u>＿＿</u>の言葉を漢字で書くとき、最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('A',3):('文字・語彙','文脈規定','（　　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('A',4):('文字・語彙','言い換え類義','<u>＿＿</u>に意味が最も近いものを、1・2・3・4から一つ選びなさい。'),
     ('A',5):('文字・語彙','用法','次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('B',1):('文法','文の文法1','次の文の（　　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('B',2):('文法','文の文法2','次の文の<b>★</b>に入る最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('B',3):('文法','文章の文法','次の文章を読んで、文章全体の内容を考えて、空欄に入る最もよいものを、1・2・3・4から一つ選びなさい。'),
     ('B',4):('読解','内容理解（短文）','次の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つ選びなさい。'),
     ('B',5):('読解','内容理解（中文）','次の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つ選びなさい。'),
     ('B',6):('読解','内容理解（長文）','次の文章を読んで、質問に答えなさい。答えは、1・2・3・4から最もよいものを一つ選びなさい。'),
     ('B',7):('読解','情報検索','右のページの案内を読んで、下の質問に答えなさい。答えは、1・2・3・4から最もよいものを一つ選びなさい。')}
def strip(t): return re.sub(r'<[^>]+>','',t)
def fixopt(o): return re.sub(r'^[\s　]+|[\s　]+$','',o)
def para(lines, sec):
    if not lines: return ''
    xs=[l[2] for l in lines]
    base={}
    for l in lines: base[(l[0],l[1])]=min(base.get((l[0],l[1]),9999),l[2])
    out=''; mx=max(len(strip(l[4]).strip()) for l in lines)
    for i,l in enumerate(lines):
        t=l[4]; p=strip(t).strip()
        newp = i==0 or l[2]-base[(l[0],l[1])]>6 or re.match(r'^[（(]注|^\s*[「『◎●☆＊*・]',p)
        prev=strip(lines[i-1][4]).strip() if i else ''
        if i and len(prev)<0.72*mx: newp=True
        if newp and i: out+='<br>'
        out+=t
    if sec==3: out=re.sub(r'(?<![\d０-９年月日円時分万])\s+(1\d|2\d|3\d)\s+(?![\d年月日円時分万%])', lambda m:f' <b class="bl">{m.group(1)}</b> ', out)
    return out
def crop(pdf, lines, name):
    import pymupdf as fitz
    d=fitz.open(pdf); files=[]
    seg={}
    for l in lines: seg.setdefault((l[0],l[1]),[]).append(l[3])
    for k,(key,ys) in enumerate(sorted(seg.items())):
        pn,col=key; p=d[pn-1]; W=p.rect.width; mid=W/2
        x0,x1=(14,mid) if col==0 else (mid,W-14)
        r=fitz.Rect(x0,max(0,min(ys)-16),x1,min(p.rect.height,max(ys)+20))
        pix=p.get_pixmap(clip=r,matrix=fitz.Matrix(2.4,2.4))
        f=f'{name}_{k}.jpg'; pix.save(OUT+'img/'+f,jpg_quality=82); files.append('img/'+f)
    return files
def load_ans(i):
    f=H+f'ans/e{i:02d}.txt'
    if not os.path.exists(f): return {}
    A={}
    for line in open(f,encoding='utf-8'):
        if not line.strip() or line.startswith('#'): continue
        k,a,dv,ex=(line.rstrip('\n').split('|',3)+['','',''])[:4]
        A[k.strip()]=dict(a=int(a),d=dv.strip(),g=ex.strip())
    return A
def build(i, pdf=None):
    R=json.load(open(H+f'raw/e{i:02d}.json'))
    fx=H+f'fix/e{i:02d}.json'
    if os.path.exists(fx):
        F=json.load(open(fx))
        for q in R['qs']:
            k=f"{q['part']}{q['n']}"
            if k in F.get('q',{}): q.update(F['q'][k])
        for gi,g in F.get('g',{}).items(): R['groups'][int(gi)].update(g)
        R['qs']=[q for q in R['qs'] if f"{q['part']}{q['n']}" not in F.get('drop',[])]
    A=load_ans(i)
    kA=dict(zip(*KEYS[str(i)]['A'])); kB=dict(zip(*KEYS[str(i)]['B']))
    groups=[]
    for gi,g in enumerate(R['groups']):
        if g.get('html'): groups.append(dict(h=g['html'])); continue
        if g['sec']==7 or g.get('img'):
            f=[x for x in sorted(glob.glob(OUT+f'img/n3e{i:02d}g{gi}_*.jpg'))]
            if not f and pdf: f=crop(pdf,g['lines'],f'n3e{i:02d}g{gi}')
            else: f=['img/'+os.path.basename(x) for x in f]
            groups.append(dict(img=f))
        else: groups.append(dict(h=para(g['lines'],g['sec'])))
    qs=[]; diff=[]
    for q in R['qs']:
        k=f"{q['part']}{q['n']}"; s=SEC.get((q['part'],q['sec']))
        key=(kA if q['part']=='A' else kB).get(q['n'])
        an=A.get(k)
        a=an['a'] if an else key
        if an and key and an['a']!=key: diff.append((k,key,an['a']))
        ex=''
        if an:
            ex=f'<div class="ans">Đáp án đúng: <b>{a}</b></div>'
            if an['d']: ex+=f'<span class="lb">DỊCH</span><div>{html.escape(an["d"])}</div>'
            if an['g']: ex+=f'<span class="lb">GIẢI THÍCH</span><div>{html.escape(an["g"])}</div>'
        qs.append(dict(k=k,s=s[0] if s else '?',m=s[1] if s else '',ins=s[2] if s else '',g=q['grp'],t=q['stem'],o=[fixopt(o) for o in q['opts']],a=(a-1) if a else None,ex=ex))
    k=ORDER.index(i)+1
    E=dict(id=f'n3-{k:02d}',src=f'N3-{NAMES[i-1]}',title=f'Đề {k}',qs=qs,groups=groups)
    json.dump(E,open(OUT+f'data/de{k:02d}.json','w'),ensure_ascii=False,separators=(',',':'))
    return E,diff
if __name__=='__main__':
    pdf=os.environ.get('N3PDF')
    ids=[int(x) for x in sys.argv[1:]] or [int(re.search(r'\d+',os.path.basename(f)).group()) for f in sorted(glob.glob(H+'ans/e*.txt'))]
    idx=json.load(open(OUT+'data/index.json')) if os.path.exists(OUT+'data/index.json') else []
    idx={e['f']:e for e in idx}
    for i in ids:
        E,diff=build(i,pdf)
        n=len(E['qs']); na=sum(1 for q in E['qs'] if q['ex'])
        print(E['title'],n,'câu,',na,'có giải thích; khác đáp án gốc:',diff)
        k=ORDER.index(i)+1
        if na==n and n: idx[f'de{k:02d}.json']=dict(f=f'de{k:02d}.json',id=E['id'],title=E['title'],n=n)
    L=sorted(idx.values(),key=lambda e:e['f'])
    json.dump(L,open(OUT+'data/index.json','w'),ensure_ascii=False)
