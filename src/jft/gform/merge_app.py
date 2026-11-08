import json, re, html, hashlib, os, sys
from PIL import Image
sys.path.insert(0, '/home/claude/anhtrong-jft-app/src/jft')
from furi import furi
exec(open('/tmp/gf/ans/fixes.py').read())

REPO = '/home/claude/anhtrong-jft-app/'
IMGDIR = REPO + 'public/app/media/jft/img/'
A = json.load(open('/tmp/gf/forms.json'))
H = lambda u: hashlib.md5(u.split('=w')[0].encode()).hexdigest()[:16]
SEC = {'V': '文字と語彙', 'K': '会話と表現', 'R': '読解'}
ORDER = ['文字と語彙', '会話と表現', '読解']
FORMS = ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11', '12']
JP = re.compile(r'[぀-ヿ㐀-鿿]')
PLACE = re.compile(r'^(Option|Tùy chọn)\s*\d*$')

def clean_opt(t):
    t = (t or '').strip()
    t = re.sub(r'^\s*([a-dA-D]|[1-4１-４])\s*[\.,．、]\s*', '', t)
    return t.strip()

def norm(s):
    s = re.sub(r'<rt>.*?</rt>|<[^>]+>', '', s or '')
    return re.sub(r'[\s　、。．.,！？!?（）()「」『』:：・\-ー―_＿]', '', s)

def clean_stem(t, form):
    t = (t or '').strip()
    if form == '10':
        m = JP.search(t)
        if m:
            # bỏ phần hướng dẫn tiếng Việt phía trước
            t = t[m.start():]
            t = re.sub(r'^[0-9０-９]+\s*[\.．]\s*', '', t)
        else:
            t = ''
    for _ in range(3):
        t2 = re.sub(r'^\s*[0-9０-９]+\s*([\.．。、,]+\s*|\s+)', '', t)
        t2 = re.sub(r'^\s*[\.．]+\s*', '', t2)
        if t2 == t: break
        t = t2
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'[ー―－]{3,}|[_＿]{3,}|\(\s*_+\s*\)|（\s*_+\s*）|\(\.{3,}\s*\)|\(\s*\.+\s*\)', '（　　）', t)
    t = re.sub(r'（\s*）|\(\s*\)|（　+）', '（　　）', t)
    t = re.sub(r'\(\s*（　　）\s*\)', '（　　）', t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\s*\n\s*', '\n', t).strip()
    if not JP.search(t): t = ''
    return t

def save_img(u, form):
    h = H(u)
    src = f'/tmp/gf/img/{h}.bin'
    name = f'g{form}_{h}.jpg'
    out = IMGDIR + name
    if not os.path.exists(out):
        im = Image.open(src)
        if im.mode in ('P', 'LA', 'RGBA'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
        else: im = im.convert('RGB')
        im.thumbnail((900, 1300)); im.save(out, 'JPEG', quality=82, optimize=True)
    return 'app/media/jft/img/' + name

def jp_html(t, use_furi=True):
    e = html.escape(t)
    if use_furi: e = furi(e)
    return e.replace('\n', '<br>')

existing = [e for e in json.load(open(REPO + 'src/raw/jft_exams.json')) if not e['id'].startswith('jft-g')]
seen = set()
for e in existing:
    for q in e['qs']:
        seen.add(norm(q.get('t')) + '|' + '|'.join(sorted(norm(o.get('t')) for o in q['o'])))

new_exams = []; report = []; num = 14; dup = 0; total = 0
for n in FORMS:
    qs_src = A[n]['qs']
    lines = [l for l in open(f'/tmp/gf/ans/f{n}.txt').read().strip().split('\n') if l.strip()]
    out = []; last_img = None
    for l in lines:
        idx, sec, ans, vi, ex = l.split('|', 4)
        idx = int(idx); ans = int(ans)
        q = qs_src[idx]; fx = FIX.get((n, idx), {})
        imgs = list(q['imgs'])
        if 'img_from' in fx:
            f2, i2 = fx['img_from']; imgs = list(A[f2]['qs'][i2]['imgs'])
        k = 1 if (q['qimg'] or 'img_from' in fx) else 0
        stem_imgs = imgs[:k]; opt_imgs = imgs[k:]
        if sec == 'R':
            if stem_imgs: last_img = stem_imgs
            elif len(clean_stem(q['t'], n)) < 90 and last_img and not fx.get('t'): stem_imgs = list(last_img)
        # options
        opts = []; j = 0
        for oi, o in enumerate(q['o']):
            t = clean_opt(o['t'])
            if (n, idx) in FIX and 'o' in fx and oi in fx['o']: t = fx['o'][oi]
            for a, b in fx.get('o_replace', []): t = t.replace(a, b)
            if o['img'] and j < len(opt_imgs):
                opts.append({'t': '', 'img': save_img(opt_imgs[j], n), 'k': oi}); j += 1; continue
            if not t or PLACE.match(t): continue
            opts.append({'t': t, 'k': oi})
        # vị trí đáp án sau khi bỏ phương án rỗng
        if ans not in [x['k'] for x in opts]:
            print('LỖI', n, idx, [o['t'] for o in q['o']], opts); continue
        ai = [x['k'] for x in opts].index(ans)
        # stem
        t = fx.get('t') or clean_stem(q['t'], n)
        for a, b in fx.get('t_replace', []): t = t.replace(a, b)
        t = re.sub(r'^\s*(\(?[a-c]\)|[（(][1-3１-３][）)]|[1-3１-３]\s*[\.．]|[1-3１-３]\))\s*', '', t)
        t = re.sub(r'^質問\(しつもん\)（１）（２）に答えましょう。\s*（１）', '', t)
        if not t:
            if sec == 'V' and stem_imgs: t = '絵を見て、正しいことばを選んでください。'
            elif sec == 'K': t = '（　　）に入るものを選んでください。'
            else: t = '正しいものを選んでください。'
        s = SEC[sec]
        blank = '（　　）' in t
        stem_furi = (sec != 'V') or blank
        # V không có chỗ trống (hỏi cách đọc/viết) -> để chữ thô cho underline.py gạch chân
        th = jp_html(t, stem_furi) if stem_furi else html.escape(t).replace('\n', '<br>')
        key = norm(t if not stem_imgs else t + H(stem_imgs[0])) + '|' + '|'.join(sorted(norm(o['t']) or o.get('img', '') for o in opts))
        if key in seen:
            dup += 1; report.append(f'trùng: form {n} #{idx}'); continue
        seen.add(key)
        o_out = []
        for o in opts:
            d = {'t': jp_html(o['t'], sec != 'V') if o['t'] else ''}
            if o.get('img'): d['img'] = o['img']
            o_out.append(d)
        right = opts[ai]
        ans_html = (f'<span class="jp">{jp_html(right["t"], True)}</span>' if right['t'] else f'phương án {ai + 1} (tranh)')
        exh = (f'<div class="ans">Đáp án đúng: {ans_html}</div>'
               f'<span class="lb">DỊCH</span><div>{jp_html(vi)}</div>'
               f'<span class="lb">GIẢI THÍCH</span><div>{jp_html(ex)}</div>')
        out.append(dict(s=s, ins='', gset=None, gimg=None, gau=None, t=th,
                        imgs=[save_img(u, n) for u in stem_imgs], img=None, au=None,
                        o=o_out, a=[ai], ex=exh))
    out.sort(key=lambda q: ORDER.index(q['s']))
    total += len(out)
    title = f'Đề {num}'
    new_exams.append(dict(id=f'jft-g{num}', group='Đề thi thử JFT-Basic', title=title,
                          sub='Không có phần nghe', short=title, time=max(20, round(len(out) * 1.2)), qs=out))
    report.append(f'{title} (form {n}: {A[n]["title"]}): {len(out)} câu')
    num += 1

# thay các đề cũ cùng id nếu chạy lại
ids = {e['id'] for e in new_exams}
keep = [e for e in existing if e['id'] not in ids]
pos = max(i for i, e in enumerate(keep) if e['id'].startswith('jft-f')) + 1
merged = keep[:pos] + new_exams + keep[pos:]
json.dump(merged, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=1)
print('\n'.join(report)); print('tổng', total, 'trùng bỏ', dup)
