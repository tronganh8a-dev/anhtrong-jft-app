"""Tách phần tiếng Việt của 6 đề mở (bản dùng thử) thành từng đơn vị cần dịch → src/en/src/<id>.txt
Khoá: @<câu>.<k>  (k = vị trí nút cấp 1 trong ex; 'q' = câu hỏi dịch (vi-q); 'a' = dòng đáp án có chữ Việt)
Nội dung rút gọn: <ruby>漢字<rt>かな</rt></ruby> → {漢字|かな}; dòng TV = các từ, mỗi từ 'từ Nhật = nghĩa' cách nhau ' || '."""
import json, re, os
A = os.path.dirname(os.path.abspath(__file__)) + '/'
R = A + '../../'
OPEN = ['jft-y3', 'jft-y4', 'jft-y5', 'jft-ln1', 'jft-ln2', 'jft-vocab']
D = re.compile('[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]')
def compact(h): return re.sub(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>', r'{\1|\2}', h)
def nodes(h):
    """tách ex thành các nút cấp 1 (ex là chuỗi phẳng: div/span/ul không lồng cùng loại)"""
    out, i = [], 0
    for m in re.finditer(r'<(div|span|ul|p)\b[^>]*>.*?</\1>|[^<]+', h, re.S):
        out.append(m.group(0))
    assert ''.join(out) == h, 'tách nút lỗi'
    return out
def load():
    s = open(R + 'public/app/data/exams.js', encoding='utf-8').read()
    E = json.JSONDecoder().raw_decode(s[s.index('=') + 1:])[0]
    return {e['id']: e for e in E if e['id'] in OPEN}
def units(q):
    """trả về [(khoá, kiểu, nội dung rút gọn)]"""
    U = []
    m = re.search(r'<span class="vi-q">(.*?)</span>', q.get('t') or '')
    if m: U.append(('q', 'Q', compact(m.group(1))))
    ns = nodes(q.get('ex') or ''); lab = None
    for k, n in enumerate(ns):
        if n.startswith('<span class="lb">'): lab = re.sub('<[^>]+>', '', n); continue
        if n.startswith('<div class="ans">'):
            t = n[len('<div class="ans">'):-6]
            if D.search(re.sub(r'^Đáp án đúng:\s*', '', t)): U.append((f'{k}', 'ANS', compact(re.sub(r'^Đáp án đúng:\s*', '', t))))
            continue
        if n.startswith('<div class="jp"') or not D.search(n): continue
        if n.startswith('<ul'):
            lis = re.findall(r'<li>(.*?)</li>', n, re.S)
            parts = []
            for li in lis:
                w = re.search(r'<span class="jp">(.*?)</span>', li); rest = li.replace(w.group(0), '') if w else li
                rest = re.sub(r'<b>.*?</b>', '', rest).strip(' –-')
                parts.append((compact(w.group(1)) if w else '') + ' = ' + compact(rest))
            U.append((f'{k}', 'TV', ' || '.join(parts))); continue
        inner = re.sub(r'^<(div|p|span)[^>]*>|</(div|p|span)>$', '', n)
        U.append((f'{k}', {'DỊCH': 'DICH', 'GIẢI THÍCH': 'GT'}.get(lab, 'X'), compact(inner)))
    return U
if __name__ == '__main__':
    tot = 0
    for eid, e in load().items():
        o = []
        for i, q in enumerate(e['qs']):
            for k, t, c in units(q):
                o.append(f'@{i + 1}.{k} {t}\n{c}')
        txt = '\n'.join(o) + '\n'; tot += len(txt)
        open(A + f'src/{eid}.txt', 'w', encoding='utf-8').write(txt)
        print(eid, len(e['qs']), 'câu', len(o), 'đơn vị', len(txt), 'ký tự')
    print(tot)
