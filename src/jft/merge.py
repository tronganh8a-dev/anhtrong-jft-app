#!/usr/bin/env python3
"""Ghép forms.json + ans/*.json -> repo/src/raw/jft_exams.json (dữ liệu đề cho app)."""
import json, os, re, html, glob
H = os.path.dirname(os.path.abspath(__file__)) + '/'
REPO = H + '../web/repo/'
F = json.load(open(H + 'forms.json'))
SECMAP = {'文字語彙': '文字と語彙', '会話表現': '会話と表現', '聴解': '聴解', '読解': '読解'}
ORDER = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f13', 'vocab', 'kaiwa']
E = lambda s: html.escape(s or '', quote=False)

def load_ans(tag):
    out = {}
    for f in sorted(glob.glob(H + f'ans/{tag}.json')) + sorted(glob.glob(H + f'ans/{tag}_*.json')):
        for a in json.load(open(f)):
            out[int(a['n'])] = a
    return out

def txt(t):
    t = re.sub(r'https?://\S+', '', t or '').strip()
    t = re.sub(r'^\s*\d+\s*[\.．]\s*', '', t)  # "25. ..." -> bỏ số thứ tự (app tự đánh số)
    return '<br>'.join(E(x.strip()) for x in t.split('\n') if x.strip())

def ex_html(q, a, opts):
    if not a: return ''
    h = f'<div class="ans">Đáp án đúng: {E(opts[a["a"]])}</div>'
    if a.get('script'):
        h += '<span class="lb">NỘI DUNG BÀI NGHE · スクリプト</span><div class="scr">' + ''.join(
            f'<p class="jp">{E(l.get("jp",""))}</p>' + (f'<p class="v">{E(l.get("vi",""))}</p>' if l.get('vi') else '') for l in a['script']) + '</div>'
    if a.get('trans_vi'):
        h += f'<span class="lb">DỊCH</span><div>{E(a["trans_vi"])}</div>'
    h += f'<span class="lb">GIẢI THÍCH</span><div>{E(a.get("why_vi",""))}</div>'
    if a.get('why_jp'):
        h += f'<div class="jp" style="margin-top:6px;color:#5a4a1a">{E(a["why_jp"])}</div>'
    voc = [v for v in (a.get('vocab') or []) if isinstance(v, list) and len(v) >= 2]
    if voc:
        h += '<span class="lb">TỪ VỰNG</span><ul>' + ''.join(
            f'<li><span class="jp">{E(v[0])}</span>' + (f'（{E(v[1])}）' if len(v) > 1 and v[1] and v[1] != v[0] else '') +
            (f' <b>{E(v[2])}</b>' if len(v) > 2 and v[2] else '') + (f' – {E(v[3])}' if len(v) > 3 else '') + '</li>' for v in voc) + '</ul>'
    return h

OV = json.load(open(H + 'overrides.json')) if os.path.exists(H + 'overrides.json') else {}
exams = []
stats = {}
for tag in ORDER:
    f = F[tag]; A = load_ans(tag)
    qs = []; low = []
    for i, q in enumerate(f['qs']):
        n = i + 1; a = A.get(n)
        sec = SECMAP.get(q['sec'], '文字と語彙' if tag == 'vocab' else '会話と表現')
        opts = [o for o in q['o']]
        ov = OV.get(tag, {}).get(str(n))
        if ov:
            for k, v in ov.get('opt_fix', {}).items(): opts[int(k)] = v
            a = dict(a or {}, **{k: v for k, v in ov.items() if k != 'opt_fix'})
        # bỏ lựa chọn rỗng / chữ giữ chỗ của Google Form ("Tùy chọn 2") nếu không phải đáp án
        ai = a.get('a') if a else None
        drop = [j for j, o in enumerate(opts) if (not o.strip() or re.fullmatch(r'(Tùy chọn|Option|オプション)\s*\d+', o.strip())) and j != ai]
        if drop:
            keepi = [j for j in range(len(opts)) if j not in drop]
            if a and isinstance(ai, int): a = dict(a, a=keepi.index(ai))
            opts = [opts[j] for j in keepi]
        # gộp lựa chọn trùng nhau
        if len(set(opts)) < len(opts):
            keep = []; remap = {}
            for j, o in enumerate(opts):
                if o in keep: remap[j] = keep.index(o)
                else: remap[j] = len(keep); keep.append(o)
            if a and isinstance(a.get('a'), int): a = dict(a, a=remap[a['a']])
            opts = keep
        t = txt(q['t']); d = txt(q['d'])
        if a and a.get('q_jp'):
            t = f'<span class="jp">{E(a["q_jp"])}</span><br><span class="vi-q">{t}</span>' if t else E(a['q_jp'])
        item = dict(s=sec, ins='', gset=d or None, gimg=None, gau=None, t=t,
                    imgs=['app/media/jft/img/' + os.path.splitext(os.path.basename(p))[0] + '.jpg' for p in q['img']],
                    img=None, au=('app/media/jft/au/' + q['au'][0] + '.mp3') if q['au'] and os.path.exists(REPO + 'public/app/media/jft/au/' + q['au'][0] + '.mp3') else None,
                    o=[{'t': E(o)} for o in opts], a=[a['a']] if a and isinstance(a.get('a'), int) and 0 <= a['a'] < len(opts) else None,
                    ex=ex_html(q, a, opts))
        if q['au'] and not item['au']:
            item['ins'] = '⚠ Lỗi audio: file nghe gốc của câu này đang bị khoá quyền truy cập, sẽ cập nhật sau.'
            item['ex'] = '<div class="ans" style="color:#a15c00">⚠ Lỗi audio: file nghe gốc bị khoá, sẽ cập nhật sau.</div>' + item['ex']
        if a and a.get('conf') in ('low',) or (a and a.get('note')): low.append(n)
        qs.append(item)
    m = re.search(r'(\d+)\D*$', f['title'])
    if tag in ('vocab', 'kaiwa'):
        e = dict(id='jft-' + tag, group='Ôn tập trọng tâm', title=('Ôn tập từ vựng & Hán tự' if tag == 'vocab' else 'Ôn tập Kaiwa hyōgen'),
                 short=('語彙・漢字' if tag == 'vocab' else '会話表現'), sub=('Từ vựng – Hán tự hay ra thi' if tag == 'vocab' else 'Hội thoại & diễn đạt'), time=45, qs=qs)
    else:
        e = dict(id='jft-' + tag, group='Đề thi thử JFT-Basic', title=f'Đề {int(m.group(1))}', sub='', time=60, qs=qs)
    exams.append(e)
    stats[tag] = dict(n=len(qs), answered=sum(1 for x in qs if x['a'] is not None), flag=low)
json.dump(exams, open(REPO + 'src/raw/jft_exams.json', 'w'), ensure_ascii=False, indent=0)
for k, v in stats.items(): print(k, v)
