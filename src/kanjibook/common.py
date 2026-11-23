"""Phần dùng chung cho bộ 3 sách いろどり (Chữ Hán · Từ vựng · Ngữ pháp): dữ liệu, chữ ruby, bìa, chân trang, font."""
import json, re, os, html, base64, collections
A = os.path.dirname(os.path.abspath(__file__)) + '/'
R = A + '../../'
FS = '/tmp/fs/node_modules/@fontsource/'
e = html.escape
isk = lambda c: '一' <= c <= '鿿' or c == '々'
plain = lambda t: re.sub(r'<rt>.*?</rt>|<[^>]+>', '', re.sub(r'\{([^{}|]+)\|[^{}]*\}', r'\1', t))

def load(name):
    s = open(R + f'public/app/data/{name}.js', encoding='utf-8').read()
    return json.JSONDecoder().raw_decode(s[s.index('=') + 1:].lstrip())[0]

def J(t):
    """{漢字|かな} → ruby · [[..]] gạch chân · ((..)) ô trống"""
    t = e(t).replace('&lt;br&gt;', '<br>')
    t = re.sub(r'\(\((.*?)\)\)', r'<span class="blank">\1</span>', t)
    t = re.sub(r'\[\[(.*?)\]\]', r'<u class="tg">\1</u>', t)
    return re.sub(r'\{([^{}|]+)\|([^{}]*)\}', lambda m: f'<ruby>{m.group(1)}<rt>{m.group(2)}</rt></ruby>' if m.group(2) else m.group(1), t)

def b64(f):
    ext = 'png' if f.endswith('.png') else 'jpeg'
    return f'data:image/{ext};base64,' + base64.b64encode(open(f, 'rb').read()).decode()

def kanji_all():
    """toàn bộ chữ Hán của 3 quyển theo thứ tự xuất hiện (nền bìa)"""
    D = load('docs'); LS = json.load(open(A + 'lessons.json'))
    seen = collections.OrderedDict()
    for w in D['kanji']['入門']:
        for c in plain(w['wr'] if 'wr' in w else w['w']):
            if isk(c): seen.setdefault(c, '入門')
    for x in LS:
        if x['lv'] in ('初級1', '初級2'):
            for w in x['words']:
                for c in plain(w['w']):
                    if isk(c): seen.setdefault(c, x['lv'])
    return seen

LOGO = re.sub(r'<\?xml[^>]*>', '', open(R + 'public/app/media/brand/logo-ngang.svg', encoding='utf-8').read())
COV = {k: b64(R + f'public/app/media/cover/{f}') for k, f in (('入門', 'nyumon.jpg'), ('初級1', 's1.jpg'), ('初級2', 's2.jpg'))}

def cover(big, title, num, unit, theme):
    """big: 2 chữ lớn (viết dọc) · title: tên tiếng Việt · num/unit: con số trên dải màu · theme: lớp màu nhấn"""
    grid = ''.join(f'<i>{c}</i>' for c in kanji_all())
    return f'''<section class="pg cover {theme}">
<div class="paper"></div><div class="kgrid">{grid}</div><div class="fade"></div>
<div class="hero"><div class="kan">{big[0]}<br>{big[1]}</div><div class="seal"><span>い<br>ろ<br>ど<br>り</span></div></div>
<div class="tblock"><h1><em>{e(title)}</em></h1><div class="lv jp">入門 · 初級1 · 初級2</div></div>
<div class="obi"><div class="o o1"><img src="{COV['入門']}"></div><div class="o o2"><img src="{COV['初級1']}"></div><div class="o o3"><img src="{COV['初級2']}"></div>
<div class="osum"><b>{num}</b><span class="jp">{unit}</span></div></div>
<div class="cbot"><div class="lg">{LOGO}</div></div></section>'''

def foot(lab, n):
    return f'<div class="ft"><span class="fl">{lab}</span><span class="pn">{n}</span><span class="fb">Anh Trọng Dạy JFT</span></div>'

def head(lv, bai, title, title_vi, topic):
    return (f'<div class="uh"><div class="un"><small>{lv}</small><b>{bai}</b><span>Bài</span></div>'
            f'<div class="ut"><div class="tp">{J(topic)}</div><h2 class="jp">{J(title)}</h2><p>{e(title_vi)}</p></div></div>')

FONTS = ''.join(f'<link rel="stylesheet" href="file://{FS}{f}">' for f in [
    'klee-one/400.css', 'klee-one/600.css', 'quicksand/400.css', 'quicksand/500.css', 'quicksand/600.css', 'quicksand/700.css',
    'yuji-syuku/400.css', 'shippori-mincho-b1/500.css', 'shippori-mincho-b1/700.css', 'shippori-mincho-b1/800.css'])

def write(path, body, extra_css=''):
    css = open(A + 'book.css', encoding='utf-8').read() + extra_css
    open(path, 'w', encoding='utf-8').write(f'<!doctype html><html lang="vi"><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body>{body}</body></html>')
