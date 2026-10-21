#!/usr/bin/env python3
"""v2: trích câu luyện kỹ năng (nghe/đọc) từ web bài học, giữ đúng NGỮ CẢNH từng câu:
- nhãn riêng (người / mùa / hàng bảng / câu điền) có furigana,
- audio + tranh riêng của câu, tiêu đề đoạn (会話1…), câu hỏi phụ (1. 2. …),
- bộ lựa chọn lấy từ lưới tranh / danh sách a-d GẦN NHẤT phía trước (không lấy nhầm lưới khác)."""
import re, json, os
from collections import Counter
from bs4 import BeautifulSoup, Tag
SP = '/tmp/claude-0/-home-claude/53ce519d-fd2a-5897-9a15-9190297c3a0e/scratchpad/'
SITE = SP + 'site/'
LV = [('s1', 'l%d_body.html', range(1, 19), 'audio', '初級1'),
      ('s2', 's2l%02d_body.html', range(1, 19), 'audio2', '初級2'),
      ('sc', 'scl%02d_body.html', range(1, 7), 'audio3', '初中級')]
ITEMC = ('person', 'card', 'job', 'fillrow')
NOSEG = ('jobs', 'job', 'persons', 'person', 'cards', 'card', 'ftable', 'fillrow', 'pair', 'opts', 'ans', 'vocab', 'scripts')
LET = r'([a-zA-Zア-ンＡ-Ｚ①-⑳])[\.．]'
def cls(e): return e.get('class') or []
def txt(el): return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip() if el else ''
def chtml(el, drop=('.pick', 'button.au', '.vi', 'input', 'img', 'textarea', 'details')):
    """HTML gọn (giữ ruby) của 1 phần tử, bỏ nút/ô nhập/tiếng Việt."""
    c = BeautifulSoup(str(el), 'html.parser')
    for x in c.select(','.join(drop)): x.decompose()
    root = c.find()
    h = root.decode_contents() if root else ''
    h = re.sub(r'<(?!/?(ruby|rt|rp|b)\b)[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', h).strip()
def plain(h): return re.sub(r'<rt>.*?</rt>|<[^>]+>', '', h).strip()
def jp_of(bi):
    if not bi: return '', ''
    j = bi.find(class_='jp'); v = bi.find(class_='vi')
    return (str(j.decode_contents()).strip() if j else ''), (txt(v) if v else '')
def skill_of(s):
    for k, n in [('聞く', 'listen'), ('読む', 'read'), ('話す', 'speak'), ('書く', 'write')]:
        if k in s: return n
    return 'other'
def inside(e, stop, names):
    for p in e.parents:
        if p is stop: return False
        if p.name == 'details' or any(c in names for c in cls(p)): return True
    return False
def anc(e, stop, name):
    for p in e.parents:
        if p is stop: return None
        if name in cls(p) or p.name == name: return p
    return None
def entry(el):
    """'a. 〇〇' (+ tranh) → (chữ cái, dict)."""
    jp = el.find(class_='jp') or el
    h = chtml(jp)
    m = re.match(r'\s*' + LET + r'\s*(.*)$', h, re.S)
    if not m: return None, None
    im = el.find('img')
    vi = el.find(class_='vi')
    return m.group(1), dict(img=im['src'] if im else None, cap=m.group(2).strip(), vi=txt(vi) if vi and vi is not jp else '')
SPL = re.compile(r'(?:^|(?<=[\s　>]))([a-zA-Zア-ン])[\.．:：]\s*')
def multi(h):
    """'a. X　b. Y　c. Z' trong 1 dòng → {a: X, b: Y, ...}"""
    ms = list(SPL.finditer(h))
    if len(ms) < 2: return {}
    out = {}
    for i, m in enumerate(ms):
        seg = h[m.end():(ms[i + 1].start() if i + 1 < len(ms) else len(h))]
        out[m.group(1)] = re.sub(r'[\s　・·]+$', '', seg).strip()
    return out
def entries(el):
    jp = el.find(class_='jp') or el
    h = chtml(jp)
    mm = multi(h)
    if mm:
        vi = el.find(class_='vi'); vv = multi(txt(vi)) if vi and vi is not jp else {}
        return {k: dict(img=None, cap=v, vi=vv.get(k, '')) for k, v in mm.items()}
    k, d = entry(el)
    return {k: d} if k else {}
def grid_of(root):
    g = {}
    for el in root.select('.job, .vocab .w, .opts .bi'):
        if el.find_parent('details') or el.select_one('.pick'): continue
        for k, d in entries(el).items():
            if k not in g: g[k] = d
    return g
def table_ctx(td):
    tr = td.find_parent('tr'); tb = td.find_parent('table')
    th = tr.find('th')
    row = chtml(th) if th else ''
    rowvi = txt(th.find(class_='vi')) if th else ''
    col = ''
    first = tb.find('tr')
    if first is not tr and first and not first.find('td'):
        cells = tr.find_all(['th', 'td'], recursive=False); hs = first.find_all(['th', 'td'], recursive=False)
        i = next((j for j, x in enumerate(cells) if x is td), -1)
        if 0 <= i < len(hs): col = chtml(hs[i])
    cap = td.find(class_='bi')
    capt = chtml(cap.find(class_='jp')) if cap and cap.find(class_='jp') else ''
    if not capt and 'jp' in cls(td): capt = chtml(td)
    imgs = ([i['src'] for i in th.find_all('img')] if th else []) + [i['src'] for i in td.find_all('img')]
    au = (th.find('button', class_='au') if th else None) or td.find('button', class_='au')
    lab = ' · '.join(x for x in [col, row, capt] if x)
    return lab, rowvi, imgs, au

items = []
for lv, pat, rng, ad, lvname in LV:
    for n in rng:
        f = SITE + (pat % n)
        if not os.path.exists(f): continue
        soup = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
        for act in soup.select('section.act'):
            head = act.select_one('.acthead')
            atitle = txt(head.select_one('.jp')) if head else ''
            sk = skill_of(txt(head.select_one('.skill')) if head else '')
            agrid = grid_of(act)
            for task in act.select('.task'):
                tgrid = grid_of(task)
                set_jp, set_vi = jp_of(task.select_one('.setting'))
                timgs = [im['src'] for im in task.find_all('img') if not im.find_parent(class_='sub') and not inside(im, task, NOSEG)]
                allimgs = [im['src'] for im in task.find_all('img') if not inside(im, task, ('ans', 'jobs', 'job', 'scripts'))]
                cards = {}
                for cd in task.select('.card'):
                    no = plain(chtml(cd.select_one('.no'))) if cd.select_one('.no') else ''
                    im = cd.find('img')
                    if no and im:
                        no = no.replace(' ', ''); cards[no] = im['src']
                        nm = re.sub(r'^[①-⑳\d]+', '', no)
                        if nm: cards[nm] = im['src']
                for sub in task.select('.sub'):
                    c = sub.select_one('.c') or sub
                    firstbi = c.find(class_='bi')
                    q_jp, q_vi = jp_of(firstbi)
                    st = dict(head='', au=None, q2=('', ''), imgs=[], grid={})
                    for e in c.descendants:
                        if not isinstance(e, Tag): continue
                        if e.name == 'details' or inside(e, c, ('ans',)): continue
                        ec = cls(e)
                        if 'th3' in ec and not anc(e, c, 'pair'):
                            st['head'] = chtml(e); st['imgs'] = []; st['q2'] = ('', '')
                        elif e.name == 'button' and 'au' in ec and not inside(e, c, ('person', 'card', 'fillrow', 'ftable', 'pair')):
                            st['au'] = e
                        elif e.name == 'img' and not inside(e, c, NOSEG):
                            st['imgs'].append(e['src'])
                        elif 'bi' in ec and e.parent is c and e is not firstbi:
                            if multi(chtml(e.find(class_='jp') or e)): st['grid'].update(entries(e))
                            else: st['q2'] = jp_of(e)
                        elif ('job' in ec and not e.select_one('.pick')) or ('w' in ec and anc(e, c, 'vocab')) or ('bi' in ec and anc(e, c, 'opts')):
                            st['grid'].update(entries(e))
                        elif 'pick' in ec:
                            pk = e
                            opts = [(b.get('data-v'), txt(b)) for b in pk.select('button.opt')]
                            if len(opts) < 2: continue
                            lab, labvi, iimgs, au = '', '', [], None
                            pair = anc(pk, c, 'pair')
                            td = anc(pk, c, 'td')
                            cont = None if td is not None else next((p for p in pk.parents if p is not c and any(x in cls(p) for x in ITEMC)), None)
                            if cont is not None and c not in cont.parents: cont = None
                            if td is not None:
                                lab, labvi, iimgs, au = table_ctx(td)
                            elif cont is not None:
                                cc = cls(cont)
                                au = cont.find('button', class_='au')
                                iimgs = [i['src'] for i in cont.find_all('img')]
                                if 'fillrow' in cc:
                                    lab = chtml(cont); labvi = txt(cont.find(class_='vi')).strip('()（） ')
                                elif 'job' in cc:
                                    lab = chtml(cont.find(class_='jp') or cont)
                                    v = cont.find(class_='vi'); labvi = txt(v) if v else ''
                                    ps = pk.find_previous_sibling()
                                    if ps is not None and ps.name == 'p': lab += ' — ' + chtml(ps, drop=('input',))
                                else:
                                    no = cont.select_one('.no')
                                    lab = chtml(no) if no else chtml(cont)
                            if pair is not None:
                                ph = pair.select_one('.th3')
                                if ph: lab = (chtml(ph) + ' — ' + lab).strip(' —')
                                iimgs = [i['src'] for i in pair.find_all('img', recursive=False)] + iimgs
                                au = au or pair.find('button', class_='au')
                            au = au or st['au']
                            pk_ = plain(lab).replace(' ', '')
                            mnum = re.match(r'^([①-⑳])', pk_)
                            cim = cards.get(pk_) or cards.get(re.sub(r'^[①-⑳\d]+', '', pk_) or '\0') or (cards.get(mnum.group(1)) if mnum else None)
                            if cim and cim not in iimgs: iimgs.append(cim)
                            if st['head']: lab = (st['head'] + ' — ' + lab).strip(' —')
                            o2 = []
                            for v, l in opts:
                                kk = l.rstrip('.．').strip()
                                g = st['grid'].get(kk) or tgrid.get(kk) or agrid.get(kk)
                                if g: o2.append(dict(v=v, t=(g['cap'] or kk + '.'), img=g['img'], vi=g['vi']))
                                else: o2.append(dict(v=v, t=l, img=None, vi=''))
                            imgs = []
                            for x in timgs + st['imgs'] + iimgs:
                                if x not in imgs: imgs.append(x)
                            if sk == 'read' and not st['imgs'] and not iimgs:
                                for x in allimgs:
                                    if x not in imgs: imgs.append(x)
                            q2 = st['q2']
                            items.append(dict(lv=lv, lvname=lvname, bai=n, act=atitle, skill=sk,
                                              setting=set_jp, setting_vi=set_vi,
                                              q=q2[0] or q_jp, qvi=q2[1] or q_vi, label=lab, labvi=labvi,
                                              audio=(f"{ad}/{au['data-t']}.mp3" if au else None),
                                              imgs=imgs[:4], opts=o2, ans=pk.get('data-ans', '').split(',')))
items = [i for i in items if i['audio'] or i['skill'] == 'read']
def bare(o): return not o['img'] and len(plain(o['t']).rstrip('.')) <= 1 and o['t'] not in ('〇', '○', '×')
items = [i for i in items if not all(bare(o) for o in i['opts'])]
for i in items: i['sec'] = 'listen' if i['audio'] else 'read'
print(len(items), Counter((i['lv'], i['sec']) for i in items))
json.dump(items, open(SP + 'app/raw/skills_raw2.json', 'w'), ensure_ascii=False, indent=0)
