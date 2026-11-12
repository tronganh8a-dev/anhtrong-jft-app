import pymupdf as fitz, re, json
d=fitz.open('n3.pdf')
K=[15,31,45,60,84,100,115,128,141,156,170,185,199,213,228,240,252,265,278,292,306,326,340,355,368,381]
def keypage(pn):
    toks=re.findall(r'[\[［]?\s*(\d+)\s*[\]］]|(?<![\d\[［x点])\b([1-5１-５])\b(?![x\dｘ点（(])',d[pn-1].get_text())
    # simpler: walk tokens line-wise
    labels=[];vals=[];out={}
    for line in d[pn-1].get_text().split('\n'):
        for m in re.finditer(r'[\[［]?\s*(\d{1,2})\s*[\]］]',line): labels.append(int(m.group(1)))
        s=line.strip()
        if re.fullmatch(r'[1-5１-５]',s): vals.append(int(s.translate(str.maketrans('１２３４５','12345'))))
        elif re.fullmatch(r'([1-5]\s+)+[1-5]',s): vals+= [int(x) for x in s.split()]
    return labels,vals
res={}
for i,k in enumerate(K):
    A=keypage(k); B=keypage(k+1)
    res[i+1]=dict(A=A,B=B)
    print(i+1,len(A[0]),len(A[1]),'|',len(B[0]),len(B[1]))
json.dump(res,open('keys_raw.json','w'))
