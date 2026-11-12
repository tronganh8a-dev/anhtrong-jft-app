"""Bộ 22 (N3-21): định dạng khác hẳn (trang dọc 1 cột, số câu '１．' / '1 ', lựa chọn '1. …' trên cùng dòng)
→ trích riêng thành raw/e22.json.  Chạy: N3PDF=… python3 tools/parse22.py"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext import page_lines
import pymupdf as fitz
H = os.path.dirname(os.path.abspath(__file__)) + '/../'
d = fitz.open(os.environ['N3PDF'])
Z = str.maketrans('０１２３４５６７８９', '0123456789')
def plain(t): return re.sub(r'<[^>]+>', '', re.sub(r'<rt>[^<]*</rt>', '', t)).strip()
NUM = re.compile(r'^\s*([０-９\d]{1,2})\s*([．\.、]?)\s*(.*)$')
SPLIT = re.compile(r'\s+(?=[１-４1-4]\s*[．\.、])')
def opts_of(t):
    out = []
    for s in SPLIT.split(t.strip()):
        out.append(re.sub(r'^\s*[１-４1-4]\s*[．\.、]?\s*', '', s, count=1).strip())
    return out
qs = []; groups = []; buf = []; cur = None; part = 'A'; sec = 0; exp = 1; newgrp = False
def flush():
    global buf
    if buf:
        groups.append(dict(sec=sec, lines=[(l['pn'], 0, l['x'], l['y'], l['t']) for l in buf])); buf = []
        return True
    return False
for pn in list(range(309, 315)) + list(range(316, 326)):
    if pn == 316 and part == 'A': part = 'B'; exp = 1; cur = None
    for x in page_lines(d[pn-1]):
        t = x['t'].strip(); p = plain(t)
        if not p: continue
        if x['y'] >= 780 and re.fullmatch(r'\d{1,2}', p): continue
        m = re.match(r'^問題\s*([１-７1-7])', p)
        if m:
            if part == 'B' and buf: flush()
            sec = int(m.group(1).translate(Z)); cur = None; continue
        if re.search(r'(えらびなさい|選びなさい|えらんでください)。?$', p) and len(p) < 70: continue
        if re.fullmatch(r'[（(]\s*[０-９\d]\s*[)）]', p):
            if part == 'B' and buf: flush()
            newgrp = True; continue
        mn = NUM.match(p)
        if mn:
            n = int(mn.group(1).translate(Z))
            isq = n == exp and (cur is None or len(cur['opts']) == 4)
            if part == 'A' and not mn.group(2): isq = False
            if part == 'B' and mn.group(2) and sec <= 2 and n <= 4 and cur is not None and len(cur['opts']) < 4: isq = False
            if isq:
                stem = re.sub(r'^\s*[０-９\d]{1,2}\s*[．\.、]?\s*', '', t, count=1)
                grp = None
                if part == 'B' and sec >= 3:
                    flush(); grp = len(groups) - 1
                    newgrp = False
                cur = dict(part=part, sec=sec, n=n, stem=stem, opts=[], grp=grp, pn=pn)
                qs.append(cur); exp = n + 1; continue
            if cur is not None and n == len(cur['opts']) + 1 and len(cur['opts']) < 4:
                cur['opts'] += opts_of(t); continue
        if cur is not None and len(cur['opts']) == 0:
            cur['stem'] += ('<br>' if cur['stem'] else '') + t; continue
        if cur is not None and 0 < len(cur['opts']) < 4:
            cur['opts'][-1] += t; continue
        if part == 'B' and sec >= 3:
            buf.append(dict(pn=pn, x=x['x'], y=x['y'], t=t))
if buf:
    groups[-1]['lines'] += [(l['pn'], 0, l['x'], l['y'], l['t']) for l in buf]
R = dict(name='21', qs=qs, groups=groups, ins={})
json.dump(R, open(H + 'raw/e22.json', 'w'), ensure_ascii=False, indent=0)
for q in qs: print(q['part'], q['sec'], q['n'], q['grp'], plain(q['stem'])[:50], '||', ' / '.join(plain(o)[:16] for o in q['opts']))
for i, g in enumerate(groups): print('G', i, g['sec'], len(g['lines']), plain(g['lines'][0][4])[:40])
