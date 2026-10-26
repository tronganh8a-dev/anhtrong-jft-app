#!/usr/bin/env python3
import json, re, os, csv, html, glob
A = os.path.dirname(os.path.abspath(__file__)) + '/'
R = A + 'raw/'; OUT = A + '../public/'; os.makedirs(OUT + 'app/data', exist_ok=True)
def js(name, var, obj):
    open(OUT + f'app/data/{name}.js', 'w', encoding='utf-8').write(f'window.{var}=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';')
def h(s): return html.escape(s or '', quote=False)

# ---------- lessons
LP = {'Shokyu1': ('s1', 'lessons/s1/'), 'Shokyu2': ('s2', 'lessons/s2/'), 'Shochukyu': ('sc', 'lessons/sc/')}
lessons = []
for ln in open(R + 'titles.txt', encoding='utf-8'):
    f, jp, vi, tp = (ln.rstrip('\n').split('|') + ['', '', '', ''])[:4]
    m = re.match(r'Irodori_(\w+?)_Bai(\d+)\.html', f)
    lv, d = LP[m.group(1)]; n = int(m.group(2))
    lessons.append(dict(lv=lv, bai=n, jp=jp, vi=vi, topic=tp, web=d + f, slide=d + f.replace('.html', '_Slide.html')))
lessons.sort(key=lambda l: (l['lv'], l['bai']))
js('lessons', 'LESSONS', lessons)

# ---------- vocab
U = json.load(open(A + 'vocab/uniq.json')); rows = json.load(open(A + 'vocab/rows.json'))
M = {}
for i in range(8):
    for r in csv.DictReader(open(A + f'vocab/out{i}.tsv', encoding='utf-8'), delimiter='\t'): M[int(r['id'])] = (r['vi'], r['hv'])
key = {(u['head'], u['yomi'], u['en']): u['id'] for u in U}
W = {}
for r in rows:
    if not r['bu']: continue
    i = key[(r['head'], r['yomi'], r['en'])]
    if i not in W:
        vi, hv = M[i]
        W[i] = dict(h=str(r['head']), y=str(r['yomi']), v=vi, hv=(hv if hv and hv != '-' else ''), e=r['en'], p=r['pos'] or '', k=bool(re.search(r'[一-鿿]', str(r['head'] or ''))), l=[])
    lk = [r['bu'], int(r['ka']), int(r['ord'] or 0)]
    if lk[:2] not in [x[:2] for x in W[i]['l']]: W[i]['l'].append(lk)
js('vocab', 'VOCAB', dict(words=list(W.values())))
print('vocab', len(W))

# ---------- skills
SK = json.load(open(R + 'skills_raw.json'))
def anm(a): return 'app/media/au/' + a.replace('audio3/', 'sc-').replace('audio2/', 's2-').replace('audio/', 's1-')
def im(x): return 'app/media/img/' + os.path.basename(x)
skills = []
for it in SK:   # trường t/label/q đã là HTML (có ruby) do skills_extract.py sinh ra
    opts = []; letters = []
    for o in it['opts']:
        t = o['t']
        if o['v'] in ('o', 'x') and len(it['opts']) == 2: t = '○ Đúng' if o['v'] == 'o' else '× Sai'
        opts.append(dict(t=t, img=im(o['img']) if o['img'] else None, vi=o.get('vi') or ''))
        letters.append(o['v'])
    a = [letters.index(x) for x in it['ans'] if x in letters]
    if not a: continue
    skills.append(dict(lv=it['lv'], bai=it['bai'], sec=it['sec'], s=('聴解' if it['sec'] == 'listen' else '読解'), src=f"{it['lvname']} Bài {it['bai']}",
                       set=it['setting'], setvi=it['setting_vi'], t=it['q'], tvi=it['qvi'], lab=it['label'] or '', labvi=it.get('labvi') or '',
                       au=anm(it['audio']) if it['audio'] else None, imgs=[im(x) for x in it['imgs']], o=opts, a=a))
js('skills', 'SKILLS', skills)
print('skills', len(skills))

# ---------- exams (luyenthitokutei.com)
SECMAP = {'BG': '文字と語彙', 'KH': '会話と表現', 'CK': '聴解', 'DK': '読解'}
ORDER = ['文字と語彙', '会話と表現', '聴解', '読解']
LT = json.load(open(R + 'lt_exams.json')) if os.path.exists(R + 'lt_exams.json') else {}   # 22/10: đã xoá bộ đề cũ, chờ đề mới
def cl(x): return (str(x) if x is not None else '').replace('\r', '').strip()
HIDE_EXAMS = set()   # số đề muốn tạm ẩn
exams = []
for n in sorted(LT, key=int):
    if int(n) in HIDE_EXAMS: continue
    rows = LT[n]['data'][1:]
    g = dict(t='', d='', img='', au='')
    qs = []
    for r in rows:
        r = list(r) + [''] * (17 - len(r))
        if cl(r[2]):
            g = dict(t=cl(r[2]), d=cl(r[3]), img=cl(r[4]), au=cl(r[5]))
        opts = [cl(x) for x in r[9:13]]
        opts = [o for o in opts if o]
        if len(opts) < 2: continue
        ans = cl(r[13]).upper()
        a = ['ABCD'.index(ans)] if ans in ('A', 'B', 'C', 'D') and 'ABCD'.index(ans) < len(opts) else None
        sec = SECMAP.get(cl(r[14]), '')
        pt = r[15] if isinstance(r[15], (int, float)) else None
        qs.append(dict(s=sec, ins=g['t'], gset=g['d'], gimg=g['img'] or None, gau=g['au'] or None, t=cl(r[6]), img=cl(r[7]) or None, au=cl(r[8]) or None,
                       o=[dict(t=o) for o in opts], a=a, pt=pt, ex=cl(r[16])))
    # keep JFT section order
    qs.sort(key=lambda q: ORDER.index(q['s']) if q['s'] in ORDER else 9)
    exams.append(dict(id='lt' + n, group='Đề thi thử JFT-Basic', title=f'Đề {int(n)}', sub='', time=60,
                      hasListen=any(q['s'] == '聴解' for q in qs), qs=qs))
# 22/10: bộ đề mới (Google Form của trung tâm) có đáp án + giải thích song ngữ — sinh bởi scratchpad/newex/merge.py
if os.path.exists(R + 'jft_exams.json'):
    exams = [e for e in json.load(open(R + 'jft_exams.json')) if e['id'] not in {f'jft-f{n}' for n in HIDE_EXAMS}]
    import sys; sys.path.insert(0, A + 'jft'); from underline import underline_exams
    print('gạch chân từ hỏi đọc/viết:', underline_exams(exams))
js('exams', 'EXAMS', exams)
open(OUT + 'app/data/exams.js', 'a', encoding='utf-8').write('window.EXTLINKS=[];')
print('exams', len(exams), sum(len(e['qs']) for e in exams), sum(1 for e in exams for q in e['qs'] if not q['a']))

# ---------- grammar
GR = []
ORDL = ['入門', '初級1', '初級2', '初中級']
for f in sorted(glob.glob(A + 'gram/out/*.json')):
    try: GR.append(json.load(open(f, encoding='utf-8')))
    except Exception as e: print('bad', f, e)
GR.sort(key=lambda g: (ORDL.index(g['lv']) if g['lv'] in ORDL else 9, g['bai']))
js('grammar', 'GRAMMAR', GR)
print('grammar lessons', len(GR), 'points', sum(len(g['points']) for g in GR))

# trọng âm từ vựng
import subprocess, sys
subprocess.run([sys.executable, A + 'pitch/add_pitch.py'], check=True)
subprocess.run([sys.executable, A + 'pitch/add_examples.py'], check=True)
subprocess.run([sys.executable, A + 'build_videos.py'], check=True)
