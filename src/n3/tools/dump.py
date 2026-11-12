"""In bản chữ gọn của 1 đề (bỏ furigana) kèm đáp án PDF để soạn giải thích."""
import json, re, sys, os
H=os.path.dirname(os.path.abspath(__file__))+'/../'
i=int(sys.argv[1]); R=json.load(open(H+f'raw/e{i:02d}.json')); K=json.load(open(H+'raw/keys_raw.json'))[str(i)]
kA=dict(zip(*K['A'])); kB=dict(zip(*K['B']))
def t(s): return re.sub(r'<[^>]+>','',re.sub(r'<rt>.*?</rt>','',s or '')).replace('\n',' ')
def u(s): return re.sub(r'<u>(.*?)</u>',r'[\1]',re.sub(r'<rt>.*?</rt>','',s or ''))
G=R['groups']; shown=set()
for q in R['qs']:
    g=q['grp']
    if g is not None and g not in shown:
        shown.add(g); L=G[g]['lines']
        if G[g]['sec']==7: print(f'--- [Bài đọc {g} – ẢNH, xem ảnh] ', t(' '.join(l[4] for l in L))[:600])
        else: print(f'--- [Bài đọc {g}] ', re.sub(r'<[^>]+>','',u(' '.join(l[4] for l in L))))
    k=(kA if q['part']=='A' else kB).get(q['n'])
    print(f"{q['part']}{q['n']} (PDF:{k}) {re.sub(r'<[^>]+>','',u(q['stem']))} || "+' | '.join(f'{j+1}.{t(o)}' for j,o in enumerate(q['opts'])))
