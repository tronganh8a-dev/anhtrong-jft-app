"""Bộ 13 (N3-13): phần 読解 có số câu không ngoặc và lựa chọn 1./2．… → trích riêng rồi ghép vào raw/e13.json."""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext import page_lines
import pymupdf as fitz
H = os.path.dirname(os.path.abspath(__file__)) + '/../'
d = fitz.open(os.environ['N3PDF'])
def plain(t): return re.sub(r'<[^>]+>', '', re.sub(r'<rt>[^<]*</rt>', '', t)).strip()
L = []
for pn in range(192, 197):
    for x in page_lines(d[pn-1]):
        p = plain(x['t'])
        if re.fullmatch(r'\d{1,2}', p) and x['x'] > 900: continue  # số trang
        L.append(dict(pn=pn, col=x['col'], x=x['x'], y=x['y'], t=x['t'].strip(), p=p))
# bắt đầu từ 問題Ⅲ (trang 192 cột phải)
st = next(i for i, l in enumerate(L) if l['p'].startswith('問題Ⅲ'))
L = L[st:]
R = json.load(open(H + 'raw/e13.json'))
R['qs'] = [q for q in R['qs'] if not (q['part'] == 'B' and q['n'] >= 19)]
R['groups'] = []
sec = None; buf = []; cur = None; qs = []
SEC = {'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5, 'Ⅵ': 6, 'Ⅶ': 7}
OPT = re.compile(r'^([1-4])\s*[\.．]?\s+(.*)$')
def flush_group():
    global buf
    if buf:
        R['groups'].append(dict(sec=sec, lines=[(l['pn'], l['col'], l['x'], l['y'], l['t']) for l in buf]))
        buf = []
for i, l in enumerate(L):
    p = l['p']
    m = re.match(r'^問題([ⅢⅣⅤⅥⅦ])', p)
    if m:
        flush_group(); sec = SEC[m.group(1)]; cur = None; skip = 2; continue
    if l['pn'] == 196 and l['col'] == 1:
        buf.append(l); continue
    if (re.search(r'(えらびなさい|選びなさい)。?$', p) and not re.match(r'^\d{2}', p)) or p.startswith('4 から最もよい') or p.startswith('3・4 から') or p.startswith('これを読んで') or p == 'よいものを一つえらびなさい。':
        continue
    if re.fullmatch(r'[（(]\s*[0-9０-９１-４]\s*[)）]', p):
        flush_group(); cur = None; continue
    mq = re.match(r'^(\d{2})(?:\s+(.*))?$', p)
    if mq and 19 <= int(mq.group(1)) <= 39 and (sec != 3 or not buf or int(mq.group(1)) >= 19):
        n = int(mq.group(1))
        if buf: flush_group()
        stem = re.sub(r'^\s*\d{2}\s*', '', l['t']) if mq.group(2) else ''
        cur = dict(part='B', sec=sec, n=n, stem=stem, opts=[], grp=len(R['groups']) - 1, pn=l['pn'])
        qs.append(cur); continue
    if cur is not None:
        # một dòng có thể chứa 2 lựa chọn
        parts = re.split(r'\s+(?=[1-4]\s*[\.．]\s*\S)', l['t'])
        if OPT.match(plain(parts[0])) or re.match(r'^[1-4][\.．]', plain(parts[0])):
            for s in parts:
                s2 = re.sub(r'^\s*[1-4]\s*[\.．]?\s*', '', s, count=1)
                cur['opts'].append(s2.strip())
            continue
        if cur['opts']:
            cur['opts'][-1] += l['t']; continue
        cur['stem'] += l['t']; continue
    buf.append(l)
flush_group()
R['qs'] += qs
json.dump(R, open(H + 'raw/e13.json', 'w'), ensure_ascii=False, indent=0)
for q in qs: print(q['n'], q['sec'], q['grp'], plain(q['stem'])[:40], [plain(o)[:18] for o in q['opts']])
for i, g in enumerate(R['groups']): print('g', i, g['sec'], len(g['lines']), plain(g['lines'][0][4])[:30])
