"""Dựng public/n3/data/vocab.json từ vocab/mimikara.tsv + giải thích vocab/gt/*.txt
Mỗi dòng giải thích: số | nội dung (¶ = xuống dòng; 'Nhãn: ...' ở đầu dòng được in đậm)."""
import json, glob, os
H=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=H+'../../public/n3/data/vocab.json'
X={}
for f in sorted(glob.glob(H+'vocab/gt/*.txt')):
    for line in open(f,encoding='utf-8'):
        if not line.strip() or line.startswith('#'): continue
        n,t=line.rstrip('\n').split('|',1); X[int(n)]=t.strip()
V=[]
for line in open(H+'vocab/mimikara.tsv',encoding='utf-8'):
    c=line.rstrip('\n').split('\t')
    if len(c)<5: continue
    n,k,h,r,m=c[:5]; w=dict(n=int(n),k=k,h=h,r=r or k,m=m)
    if int(n) in X: w['x']=X[int(n)]
    V.append(w)
json.dump(V,open(OUT,'w'),ensure_ascii=False,separators=(',',':'))
print(len(V),'từ,',sum(1 for w in V if 'x' in w),'có giải thích')
