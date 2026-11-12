"""Trích text trang PDF đề N3: tách 2 cột, gắn furigana (ruby) và gạch chân (<u>)."""
import pymupdf as fitz, re, json, sys, html
KAN=re.compile(r'[㐀-鿿々〆ヶ]')
def page_lines(p):
    W=p.rect.width; mid=W/2 if W>700 else W*2   # trang dọc (A4 đứng) = 1 cột
    D=p.get_text('rawdict')
    chars=[]
    for b in D['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                for c in s['chars']:
                    if not c['c'].strip(): 
                        chars.append(dict(c=' ',x0=c['bbox'][0],x1=c['bbox'][2],y0=c['bbox'][1],y1=c['bbox'][3],sz=s['size'],sp=1)); continue
                    chars.append(dict(c=c['c'],x0=c['bbox'][0],x1=c['bbox'][2],y0=c['bbox'][1],y1=c['bbox'][3],sz=s['size'],sp=0))
    ul=[];vt=[]
    for d0 in p.get_drawings():
        r=d0['rect']
        if r.height<=2.5 and r.width>6: ul.append((r.x0,r.x1,r.y0))
        if r.width<=2.5 and r.height>8: vt.append((r.x0,r.y0,r.y1))
        for it in d0['items']:
            if it[0]=='l':
                a,b=it[1],it[2]
                if abs(a.y-b.y)<1 and abs(a.x-b.x)>6: ul.append((min(a.x,b.x),max(a.x,b.x),a.y))
                if abs(a.x-b.x)<1 and abs(a.y-b.y)>8: vt.append((a.x,min(a.y,b.y),max(a.y,b.y)))
            if it[0]=='re':
                q=it[1]
                if q.height>8 and q.width>8:   # khung chữ nhật: 4 cạnh không phải gạch chân
                    vt.append((q.x0,q.y0,q.y1)); vt.append((q.x1,q.y0,q.y1))
    def boxedge(x0,x1,y): return any((abs(vx-x0)<3 or abs(vx-x1)<3) and vy0-3<=y<=vy1+3 for vx,vy0,vy1 in vt)
    ul=[u for u in ul if not boxedge(*u)]
    main=[c for c in chars if c['sz']>=8]; rub=[c for c in chars if c['sz']<8 and not c['sp']]
    out=[]
    for col in (0,1):
        M=[c for c in main if ((c['x0']+c['x1'])/2<mid)==(col==0)]
        R=[c for c in rub if ((c['x0']+c['x1'])/2<mid)==(col==0)]
        # group into lines by vertical center
        M.sort(key=lambda c:((c['y0']+c['y1'])/2,c['x0']))
        lines=[]
        for c in M:
            cy=(c['y0']+c['y1'])/2
            for L in lines:
                if abs(L['cy']-cy)<max(3,c['sz']*0.45): L['cs'].append(c); break
            else: lines.append(dict(cy=cy,cs=[c]))
        lines.sort(key=lambda L:L['cy'])
        for L in lines:
            L['cs'].sort(key=lambda c:c['x0']); L['top']=min(c['y0'] for c in L['cs']); L['bot']=max(c['y1'] for c in L['cs'])
            for c in L['cs']: c['rt']=None; c['u']=False
        # ruby: group ruby chars into runs, attach to line below
        R.sort(key=lambda c:(round((c['y0']+c['y1'])/2),c['x0']))
        runs=[]
        for c in R:
            if runs and abs((runs[-1][-1]['y0']+runs[-1][-1]['y1'])/2-(c['y0']+c['y1'])/2)<1.5 and c['x0']-runs[-1][-1]['x1']<4: runs[-1].append(c)
            else: runs.append([c])
        for run in runs:
            ry=max(c['y1'] for c in run); x0=run[0]['x0']; x1=run[-1]['x1']
            cand=[L for L in lines if -2<L['top']-ry<14]
            if not cand: continue
            L=min(cand,key=lambda L:L['top']-ry)
            ks=[c for c in L['cs'] if (c['x0']+c['x1'])/2>=x0-4 and (c['x0']+c['x1'])/2<=x1+4 and KAN.match(c['c'])]
            if not ks:
                # widen
                cx=(x0+x1)/2; ks=sorted([c for c in L['cs'] if KAN.match(c['c'])],key=lambda c:abs((c['x0']+c['x1'])/2-cx))[:1]
                if not ks or abs((ks[0]['x0']+ks[0]['x1'])/2-cx)>12: continue
            txt=''.join(c['c'] for c in run)
            ks[0]['rt']=(txt,len(ks))
            for c in ks[1:]: c['rt']=('',0)
        for (ux0,ux1,uy) in ul:
            if not ((ux0+ux1)/2<mid)==(col==0): continue
            hit=False
            for L in lines:
                if -1<=uy-L['bot']<=6:
                    if not any(c['x1']>ux0+2 and c['x0']<ux1-2 for c in L['cs']):
                        L['cs'].append(dict(c='＿＿',x0=ux0,x1=ux1,y0=L['top'],y1=L['bot'],sz=12,sp=0,rt=None,u=False)); hit=True
                    break
        for L in lines: L['cs'].sort(key=lambda c:c['x0'])
        for (ux0,ux1,uy) in ul:
            for L in lines:
                if 0<=uy-L['bot']<=5.5 or (L['top']<uy<=L['bot']+5.5 and uy-L['bot']>-2):
                    for c in L['cs']:
                        if (c['x0']+c['x1'])/2>ux0 and (c['x0']+c['x1'])/2<ux1: c['u']=True
                    break
        for L in lines:
            s='';cs=L['cs'];i=0;u=False;prevx=None
            while i<len(cs):
                c=cs[i]
                if prevx is not None and c['x0']-prevx>c['sz']*1.2: s+='　' if not c['sp'] else ''
                if c['u'] and not u: s+='<u>'; u=True
                if not c['u'] and u: s+='</u>'; u=False
                if c['rt'] and c['rt'][1]:
                    n=c['rt'][1]; base=''.join(x['c'] for x in cs[i:i+n]); s+=f'<ruby>{html.escape(base)}<rt>{html.escape(c["rt"][0])}</rt></ruby>'; prevx=cs[i+n-1]['x1']; i+=n; continue
                s+=html.escape(c['c']) if not c['sp'] else ' '; prevx=c['x1']; i+=1
            if u: s+='</u>'
            s=re.sub(r' {2,}',' ',s).strip()
            if s: out.append(dict(col=col,y=round(L['top'],1),x=round(cs[0]['x0'],1),sz=round(max(c['sz'] for c in cs),1),t=s))
    return out
if __name__=='__main__':
    d=fitz.open(sys.argv[1]); a,b=int(sys.argv[2]),int(sys.argv[3])
    for i in range(a-1,b):
        for L in page_lines(d[i]): print(f"p{i+1}c{L['col']} {L['y']:6} {L['x']:6} | {L['t']}")
