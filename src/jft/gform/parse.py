import re, json, html as H, hashlib, os, subprocess
forms = ['1','2','3','4','5','6','7','9','10','11','12']
ALL = {}
for n in forms:
    t = open(f'html/f{n}.html').read()
    d = json.loads(re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*?);</script>', t, re.S).group(1))
    title = d[1][8] or d[3]
    extra = ''.join(open(f'html/f{n}_p{k}.html').read() for k in (1,2)) if n=='10' else ''
    parts = (t+extra).split('data-params="%.@.[')
    chunks = {}
    for p in parts[1:]:
        m = re.match(r'(\d+)', p)
        if not m: continue
        imgs = [H.unescape(u) for u in re.findall(r'<img[^>]+src="(https://docs\.google\.com/forms-images-rt/[^"]+)"', p)]
        chunks[m.group(1)] = imgs
    qs = []
    sec = None
    for it in d[1][1]:
        typ = it[3]
        iid = str(it[0])
        if typ == 8:
            sec = {'t': it[1], 'd': it[2]}; continue
        if typ in (6, 11, 0):
            qs.append({'k': 'info', 'typ': typ, 't': it[1], 'd': it[2], 'imgs': chunks.get(iid, []), 'hasimg': bool(len(it) > 6 and it[6])})
            continue
        if typ not in (2, 3): continue
        opts = []
        for o in it[4][0][1] or []:
            opts.append({'t': o[0], 'img': bool(len(o) > 5 and o[5])})
        qimg = bool(len(it) > 9 and it[9])
        qs.append({'k': 'q', 't': it[1] or '', 'd': it[2] or '', 'o': opts, 'qimg': qimg, 'imgs': chunks.get(iid, []), 'sec': sec})
    ALL[n] = {'title': title, 'qs': qs}
json.dump(ALL, open('forms.json', 'w'), ensure_ascii=False, indent=1)
for n, f in ALL.items():
    qq = [q for q in f['qs'] if q['k'] == 'q']
    need = sum((1 if q['qimg'] else 0) + sum(o['img'] for o in q['o']) for q in qq) + sum(1 for q in f['qs'] if q['k']=='info' and q['hasimg'])
    have = sum(len(q['imgs']) for q in f['qs'])
    print(n, f['title'], len(qq), 'imgneed', need, 'have', have)
