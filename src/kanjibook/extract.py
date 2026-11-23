"""Lấy danh sách 漢字のことば của từng bài trong 3 quyển いろどり (từ web bài học public/lessons) → src/kanjibook/lessons.json"""
import re, glob, json, os
R = os.path.dirname(os.path.abspath(__file__)) + '/../../'
LV = {'sc': '初中級', 's1': '初級1', 's2': '初級2'}  # sc = 初中級 (入門 không có web bài học)
out = []
for d, lv in LV.items():
    for f in sorted(glob.glob(R + f'public/lessons/{d}/Irodori_*_Bai[0-9][0-9].html')):
        s = open(f, encoding='utf-8').read()
        i = s.find('id="kanji"')
        if i < 0: print('không có kanji:', f); continue
        j = s.find('</section>', i)
        t = s[i:j]
        bai = int(re.search(r'Bai(\d+)', f).group(1))
        title = re.search(r'<h1 class="bi"><span class="jp">(.*?)</span>', s)
        words = []
        for m in re.finditer(r'<div class="kc">(.*?)</div>\s*(?=<div class="kc">|</div>)', t, re.S):
            c = m.group(1)
            f1 = re.search(r'<span class="f1">(.*?)</span>', c, re.S).group(1)
            hv = re.search(r'<span class="hv">(.*?)</span>', c); vi = re.search(r'<span class="vi">(.*?)</span>', c)
            words.append({'w': f1, 'hv': hv.group(1) if hv else '', 'vi': vi.group(1) if vi else ''})
        out.append({'lv': lv, 'bai': bai, 'title': title.group(1) if title else '', 'words': words})
json.dump(out, open(R + 'src/kanjibook/lessons.json', 'w'), ensure_ascii=False, indent=0)
import collections
for lv in LV.values():
    L = [x for x in out if x['lv'] == lv]
    ks = collections.OrderedDict()
    for x in L:
        for w in x['words']:
            for ch in re.sub(r'<rt>.*?</rt>|<[^>]+>', '', w['w']):
                if '一' <= ch <= '鿿': ks.setdefault(ch, x['bai'])
    print(lv, len(L), 'bài', sum(len(x['words']) for x in L), 'từ', len(ks), 'chữ')
