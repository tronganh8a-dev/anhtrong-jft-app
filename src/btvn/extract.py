import re,html,json,glob
from html.parser import HTMLParser
O='/mnt/user-data/outputs/'
def strip_rt(x): return re.sub(r'<rt>.*?</rt>','',x)
def text(x): return html.unescape(re.sub(r'<[^>]+>','',x)).strip()
def ruby2br(x):  # <ruby>漢<rt>かん</rt></ruby> -> {漢|かん}
    x=re.sub(r'<ruby[^>]*>(.*?)<rt>(.*?)</rt></ruby>',lambda m:'{'+text(m.group(1))+'|'+text(m.group(2))+'}',x)
    return html.unescape(re.sub(r'<(?!/?(u|b)\b)[^>]+>','',x)).strip()
out={}
for f in sorted(glob.glob(O+'Irodori_Shokyu[12]_Bai[0-9][0-9].html')):
    m=re.search(r'Shokyu(\d)_Bai(\d+)',f); key=f"s{m.group(1)}-{int(m.group(2))}"
    s=open(f,encoding='utf-8').read(); s=re.sub(r'data:[^"\')]{100,}','',s); b=s[s.index('<body'):]
    # kanji
    K=[];SEN=[]
    if '<section id="kanji">' in b:
        k=b[b.index('<section id="kanji">'):]; k=k[:k.index('</section>')]
        for kc in re.finditer(r'<div class="kc"><div class="fonts"><span class="f1">(.*?)</span>.*?<span class="hv"[^>]*>(.*?)</span><span class="vi">(.*?)</span>',k,re.S):
            f1=kc.group(1); word=text(strip_rt(f1)); 
            yomi=re.sub(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>',lambda mm:mm.group(2),f1); yomi=text(yomi)
            K.append(dict(w=word,y=yomi,hv=text(kc.group(2)),vi=text(kc.group(3))))
        for sb in re.finditer(r'<div class="bi"><p class="jp">(.*?)</p><p class="vi">(.*?)</p></div>',k[k.find('class="sentences"'):k.find('class="typing"') if 'class="typing"' in k else None],re.S):
            jp=sb.group(1)
            if 'class="tg"' not in jp: continue
            tg=[(text(mm.group(1)),text(mm.group(2))) for mm in re.finditer(r'<ruby class="tg">(.*?)<rt>(.*?)</rt></ruby>',jp)]
            # mark targets with ⟦⟧ and other ruby -> {}
            jm=re.sub(r'<ruby class="tg">(.*?)<rt>(.*?)</rt></ruby>',lambda mm:'⟦'+text(mm.group(1))+'|'+text(mm.group(2))+'⟧',jp)
            jm=re.sub(r'<br\s*/?>','\n',jm)
            SEN.append(dict(jp=ruby2br(jm),vi=text(sb.group(2)),tg=tg))
    # scripts
    SC=[]
    if '<section id="script">' in b:
        sc=b[b.index('<section id="script">'):]; sc=sc[:sc.index('</section>')]
        parts=re.split(r'<div class="th3">',sc)[1:]
        for p in parts:
            title=text(strip_rt(p[:p.index('</div>')]))
            for d in re.finditer(r'<div class="sc"><div class="hd"><span class="no">(.*?)</span>.*?</div>(.*?)(?=<div class="sc">|$)',p,re.S):
                lines=[dict(s=text(l.group(1)),jp=ruby2br(l.group(2)),vi=text(l.group(3))) for l in re.finditer(r'<div class="sl"><span class="s">(.*?)</span><div class="bi"><p class="jp">(.*?)</p><p class="vi">(.*?)</p>',d.group(2),re.S)]
                if lines: SC.append(dict(sec=title,no=text(d.group(1)),lines=lines))
    out[key]=dict(kanji=K,sen=SEN,scripts=SC)
json.dump(out,open('lessons_extra.json','w'),ensure_ascii=False,indent=0)
for k in ['s1-1','s1-3','s2-16']: v=out[k]; print(k,len(v['kanji']),len(v['sen']),len(v['scripts']),v['kanji'][:2],v['sen'][:1],v['scripts'][1]['lines'][:2] if len(v['scripts'])>1 else '')
print({k:(len(v['kanji']),len(v['sen']),len(v['scripts'])) for k,v in out.items()})
