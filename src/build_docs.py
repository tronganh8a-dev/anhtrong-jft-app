#!/usr/bin/env python3
"""Tab Tài liệu: từ vựng / chữ Hán / ngữ pháp (tài liệu lớp cô Quỳnh) -> public/app/data/docs.js
Nguồn: src/docs/*_src.json (trích từ PDF) + src/docs/ans/*.json (phần soạn: giải thích, Hán Việt, bài tập).
Ảnh từ vựng: public/app/media/doc/<md5>.jpg"""
import json, os, re, glob, html, sys
A = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, A + 'jft'); from furi import furi, ruby_word, KANJI, k2h
D = A + 'docs/'
E = lambda s: html.escape(s or '', quote=False)
FE = lambda s: furi(E(s)).replace('\n', '<br>')
LV = ['入門', '初級1', '初級2']
def load(prefix):
    out = {}
    for f in sorted(glob.glob(D + f'ans/{prefix}.json') + glob.glob(D + f'ans/{prefix}_*.json')):
        for x in json.load(open(f, encoding='utf-8')): out[x.get('i', x.get('n'))] = x
    return out
def wr(w, r):
    if not re.search(KANJI, w or ''): return E(w)
    if r and re.fullmatch(r'[぀-ヿー・\s0-9０-９,，.]+', r):
        h = ruby_word(E(w), k2h(r.replace(' ', '')))
        if h.count('<ruby>') >= 1 and not h.startswith(f'<ruby>{E(w)}<rt>') or not re.search('[぀-ゟ]', w): return h
    return FE(w)
# ---- từ vựng
src = A + '../public/app/data/vocab.js'; s = open(src, encoding='utf-8').read(); VOC = json.loads(s[s.index('=') + 1:s.rindex(';')])
vidx = {(w['h'], w['y']): w for w in VOC['words']}; hidx = {}
for w in VOC['words']: hidx.setdefault(w['h'], w)
vocab = {k: [] for k in LV}; V = json.load(open(D + 'vocab_src.json', encoding='utf-8'))
cnt = {k: 0 for k in LV}
for lv in LV:
    ans = load(f'vocab_{LV.index(lv)}')
    for n, v in enumerate(V):   # i trong gói = chỉ số toàn danh sách
        if v['lv'] != lv: continue
        a = ans.get(n, {})
        w = a.get('w') or v['w']; r = a.get('r', v['r']) ; vi = a.get('vi') or v['vi']
        m = vidx.get((w, r)) or (hidx.get(w) if re.search(KANJI, w) else None)
        it = dict(b=v['bai'], w=E(w), wr=wr(w, r), r=r, vi=vi, hv=a.get('hv') or (m or {}).get('hv', ''), pos=a.get('pos', ''))
        if v.get('img'): it['img'] = v['img'] + '.jpg'
        if m and m.get('au'): it['au'] = m['au']
        if m and 'x' in m and m['x'] < len(VOC['ex']): it['ex'] = VOC['ex'][m['x']]
        vocab[lv].append(it); cnt[lv] += bool(a)
print('vocab', {k: len(v) for k, v in vocab.items()}, 'đã soạn', cnt)
# ---- chữ Hán
K = json.load(open(D + 'kanji_src.json', encoding='utf-8')); kanji = {}
for lv in LV:
    ans = load(f'kanji_{LV.index(lv)}'); out = []
    for i, k in enumerate(K[lv]):
        a = ans.get(i, {}); w = a.get('w') or k['w']; r = a.get('r') or k['r']
        it = dict(w=E(w), r=r, wr=wr(w, r), vi=a.get('vi') or k['vi'], hv=a.get('hv', ''), chars=a.get('chars', []), tip=a.get('tip_vi', ''))
        if a.get('ex'): it['ex'] = dict(jp=FE(a['ex'].get('jp', '')), vi=a['ex'].get('vi', ''))
        out.append(it)
    kanji[lv] = out
    print('kanji', lv, len(out), 'đã soạn', len(ans))
# ---- ngữ pháp
G = json.load(open(D + 'gram_src.json', encoding='utf-8')); ga = load('gram'); gram = {k: [] for k in LV}
# sửa câu quiz theo đợt kiểm định (ans/quizfix_*.json: id "n-k")
for f in sorted(glob.glob(D + 'ans/quizfix_*.json')):
    for fx in json.load(open(f, encoding='utf-8')):
        n, k = map(int, fx['id'].split('-'))
        if n in ga and k < len(ga[n].get('quiz', [])): ga[n]['quiz'][k].update(fx.get('fix') or {})
for g in G:
    a = ga.get(g['n'], {})
    bai = (g.get('irodori') or g.get('irodori_guess') or [g['lv'], 0])[1]
    ex = a.get('example') or {'jp': g['example'], 'vi': ''}
    it = dict(n=g['n'], bai=bai, p=FE(a.get('pattern') or g['pattern'] or g['meaning']), m=a.get('meaning_vi') or g['meaning'],
              st=[FE(x) for x in a.get('structure', [])], xp=[FE(x) for x in a.get('explain_vi', [])],
              ex=dict(jp=FE(ex.get('jp', '')), vi=ex.get('vi', ''), self=bool(ex.get('self'))) if ex.get('jp') else None,
              exs=[dict(jp=FE(x['jp']), vi=x.get('vi', '')) for x in a.get('examples', [])],
              qz=[dict(q=FE(q['q']), o=[FE(o) for o in q['o']], a=q['a'], ex=FE(q.get('ex_vi', ''))) for q in a.get('quiz', []) if isinstance(q.get('a'), int) and 0 <= q['a'] < len(q['o'])])
    gram[g['lv']].append(it)
print('gram', {k: len(v) for k, v in gram.items()}, 'đã soạn', len(ga))
# đáp án nhiễu soạn riêng (ans/dist_*.json): rd = cách đọc sai na ná, wk = cách viết sai na ná
DI = {}
for f in sorted(glob.glob(D + 'ans/dist_*.json')):
    for x in json.load(open(f, encoding='utf-8')): DI[x['id']] = x
nd = 0
for kind, src in (('k', kanji), ('v', vocab)):
    for lv in LV:
        for i, it in enumerate(src[lv]):
            x = DI.get(f'{kind}|{lv}|{i}')
            if not x: continue
            rd = [r for r in dict.fromkeys(x.get('rd') or []) if r and r != it['r']][:3]
            if len(rd) == 3: it['rd'] = rd; nd += 1
            wk = [E(w) for w in dict.fromkeys(x.get('wk') or []) if w and E(w) != it['w']][:3]
            if kind == 'k' and len(wk) == 3: it['wk'] = wk
print('đáp án nhiễu', nd, '/', len(DI))
open(A + '../public/app/data/docs.js', 'w', encoding='utf-8').write('window.DOCS=' + json.dumps(dict(vocab=vocab, kanji=kanji, gram=gram), ensure_ascii=False, separators=(',', ':')) + ';')
print('docs.js', os.path.getsize(A + '../public/app/data/docs.js') // 1024, 'KB')
