import json,glob,re,base64,os,sys
SRC='/mnt/user-data/uploads/Downloads/jftdump/'
pages={}
for f in sorted(glob.glob(SRC+'d*.json')):
    d=json.load(open(f))
    t=d['tag']
    if t=='f7b': t='f7'
    pages.setdefault(t,{})
    if d['pg'] not in pages[t] or len(json.dumps(d))>len(json.dumps(pages[t][d['pg']])): pages[t][d['pg']]=d
os.makedirs('img',exist_ok=True)
out={}
for t,P in pages.items():
    fb=P[0]['fb']; items=fb[1][1]
    imgs={}
    for p in P.values():
        for iid,lst in p['imgs'].items(): imgs[iid]=lst
    qs=[];sec=''
    for it in items:
        iid=str(it[0]); typ=it[3]; title=it[1] or ''; desc=it[2] or ''
        html=(it[11][1] if len(it)>11 and it[11] else '') or ''
        dhtml=(it[12][1] if len(it)>12 and it[12] else '') or ''
        if typ==8: sec=title; continue
        if typ not in (2,4): continue
        opts=[o[0] for o in it[4][0][1]]
        files=[]
        for k,du in enumerate(imgs.get(iid,[])):
            m=re.match(r'data:image/(\w+);base64,(.*)',du,re.S)
            if not m: continue
            ext={'jpeg':'jpg'}.get(m.group(1),m.group(1))
            fn=f'img/{t}_{iid}_{k}.{ext}'
            if not os.path.exists(fn): open(fn,'wb').write(base64.b64decode(m.group(2)))
            files.append(fn)
        au=re.findall(r'drive\.google\.com/(?:file/d/|open\?id=)([\w-]{20,})',title+desc+html)
        qs.append(dict(id=iid,sec=sec,typ=typ,t=title,d=desc,html=html,dhtml=dhtml,o=opts,img=files,au=au[:1]))
    out[t]=dict(title=P[0]['fb'][3] if False else P[0]['fb'][1][8],desc=fb[1][0],qs=qs)
json.dump(out,open('forms.json','w'),ensure_ascii=False,indent=1)
for t in out: print(t,out[t]['title'],len(out[t]['qs']),sum(1 for q in out[t]['qs'] if q['img']),sum(1 for q in out[t]['qs'] if q['au']))
