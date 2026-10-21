#!/usr/bin/env python3
# Thêm trọng âm (pitch accent) vào public/app/data/vocab.js
# Nguồn: Kanjium accents.txt (mifunetoshiro/kanjium, CC BY-SA 4.0) — lưu bản rút gọn ở accents_sub.tsv
import json, re, os, collections, sys
H = os.path.dirname(os.path.abspath(__file__)) + '/'
VJ = H + '../../public/app/data/vocab.js'
SRC = sys.argv[1] if len(sys.argv) > 1 else H + 'accents_sub.tsv'
FULL = SRC != H + 'accents_sub.tsv'
A = collections.defaultdict(list); BYR = collections.defaultdict(set)
for ln in open(SRC, encoding='utf-8'):
    p = ln.rstrip('\n').split('\t')
    if len(p) < 3: continue
    w, r, a = p[0], p[1] or p[0], p[2]
    A[(w, r)].append(a); BYR[r].add(a)
def k2h(t): return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in t)
def clean(x):
    x = re.sub(r'[（(][^）)]*[）)]', '', x); x = re.sub(r'[～〜\s　？?！!。]', '', x)
    return re.split(r'[／/]', x)[0]
def look(h, y):
    for key in [(h, y), (h, k2h(y)), (y, y), (k2h(y), k2h(y))]:
        if key in A: return A[key][0], key
    if FULL and y in BYR and len(BYR[y]) == 1: return next(iter(BYR[y])), (None, y)
    return None, None
s = open(VJ, encoding='utf-8').read(); D = json.loads(s[s.index('=') + 1:s.rindex(';')])
used = set(); hit = 0
for w in D['words']:
    h, y = clean(w['h']), clean(w['y']); w.pop('a', None); w.pop('e', None)
    a, key = look(h, y)
    if a is None and h.endswith('する') and y.endswith('する') and len(h) > 2:
        a0, key = look(h[:-2], y[:-2])
        if a0 is not None: a = a0.split(',')[0]
    if a is not None:
        w['a'] = a; hit += 1
        if key and key[0]: used.add(key)
open(VJ, 'w', encoding='utf-8').write('window.VOCAB=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';')
if SRC != H + 'accents_sub.tsv':
    with open(H + 'accents_sub.tsv', 'w', encoding='utf-8') as f:
        for (w_, r_) in sorted(used):
            for a in A[(w_, r_)]: f.write(f'{w_}\t{r_}\t{a}\n')
        # giữ cả mục chỉ-theo-cách-đọc
        for w in D['words']:
            y = clean(w['y'])
            if y in BYR and len(BYR[y]) == 1 and (y, y) not in used:
                f.write(f'{y}\t{y}\t{next(iter(BYR[y]))}\n')
print('pitch', hit, '/', len(D['words']))
