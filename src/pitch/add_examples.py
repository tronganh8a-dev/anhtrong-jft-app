#!/usr/bin/env python3
# Thêm câu ví dụ (từ ví dụ ngữ pháp + script hội thoại + câu 漢字のことば của いろどり) và link audio vào vocab.js
import json, re, os, hashlib
H = os.path.dirname(os.path.abspath(__file__)) + '/'
P = H + '../../public/'
def load(f):
    s = open(P + 'app/data/' + f, encoding='utf-8').read()
    return s, json.loads(s[s.index('=') + 1:s.rindex(';')])
_, D = load('vocab.js'); _, G = load('grammar.js')
X = json.load(open(H + '../btvn/lessons_extra.json', encoding='utf-8'))
def plain(s): return re.sub(r'\{([^|}]+)\|[^}]+\}', r'\1', s or '')
POOL = []  # (lv, bai, jp, vi)
for g in G:
    for p in g['points']:
        for e in (p.get('examples') or []) + (p.get('more_examples') or []):
            if e.get('jp') and e.get('vi'): POOL.append((g['lv'], g['bai'], e['jp'], e['vi']))
for k, v in X.items():
    lv = '初級1' if k.startswith('s1') else '初級2'; b = int(k.split('-')[1])
    for d in v['scripts']:
        for l in d['lines']:
            if l['vi']: POOL.append((lv, b, l['jp'], l['vi']))
    for s_ in v['sen']:
        jp = re.sub(r'⟦([^|⟧]+)\|([^⟧]+)⟧', r'{\1|\2}', s_['jp']); jp = re.sub(r'^[①-⑳]\s*', '', jp)
        POOL.append((lv, b, jp, s_['vi']))
for g in G:
    for p in g['points']:
        for blk in p.get('worksheet') or []:
            for it in blk.get('items') or []:
                q = it.get('q') or ''; an = (it.get('answer') or [''])[0]
                if not an or '\n' in q or it.get('type') == 'free': continue
                an = re.split(r'[／/]', an)[0]
                q2 = re.sub(r'（[^（）]*→\s*＿＿）', an, q)
                if q2 == q: q2 = q.replace('（＿＿）', an).replace('＿＿', an)
                if '＿' in q2 or '→' in q2 or '｜' in q2: continue
                q2 = re.sub(r'^\s*\d+[\.．、]\s*', '', q2).strip()
                POOL.append((g['lv'], g['bai'], q2, ''))
POOL = [(lv, b, jp, vi, plain(jp)) for lv, b, jp, vi in POOL if 4 <= len(plain(jp)) <= 46 and '\n' not in jp and '<br' not in jp]
KJ = '一-龯々'
def clean(x):
    x = re.sub(r'[（(][^）)]*[）)]', '', x); x = re.sub(r'[～〜\s　？?！!。]', '', x)
    return re.split(r'[／/]', x)[0]
def pattern(w):
    h = clean(w['h']); p = (w.get('p') or '').strip()
    if not h: return None
    if p.startswith('V') and h.endswith('する') and len(h) > 2:
        st = h[:-2]; return re.compile(f'(?<![{KJ}]){re.escape(st)}(?=[しすさせ])')
    if p.startswith('V') or p == 'イA':
        st = h[:-1]
        if len(st) == 0: return None
        if len(st) == 1 and not re.match(f'[{KJ}]', st): return None
        return re.compile(f'(?<![{KJ}]){re.escape(st)}(?=[ぁ-ん])')
    if not re.search(f'[{KJ}ァ-ヶ]', h) and len(h) < 3: return None
    if not re.search(f'[{KJ}]', h): return re.compile(re.escape(h))
    return re.compile(f'(?<![{KJ}ァ-ヶ]){re.escape(h)}(?![{KJ}])')
EX = []; EXI = {}; hit = 0
for w in D['words']:
    w.pop('x', None)
    pat = pattern(w)
    if not pat: continue
    lvb = {(x[0], x[1]) for x in w['l']}; lvs = {x[0] for x in w['l']}
    best = None
    for lv, b, jp, vi, pl in POOL:
        if not pat.search(pl): continue
        score = (0 if vi else 1, 0 if (lv, b) in lvb else 1 if lv in lvs else 2, abs(len(pl) - 18))
        if best is None or score < best[0]: best = (score, jp, vi)
    if best:
        key = best[1]
        if key not in EXI: EXI[key] = len(EX); EX.append([best[1], best[2]])
        w['x'] = EXI[key]; hit += 1
# audio (VOICEVOX) nếu đã có file
for w in D['words']:
    k = hashlib.md5((w['h'] + '|' + w['y']).encode()).hexdigest()[:12]
    if os.path.exists(P + f'app/media/vau/{k}.mp3'): w['au'] = k
    else: w.pop('au', None)
D['ex'] = EX
open(P + 'app/data/vocab.js', 'w', encoding='utf-8').write('window.VOCAB=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';')
print('examples', hit, '/', len(D['words']), 'unique', len(EX), 'audio', sum(1 for w in D['words'] if w.get('au')))
