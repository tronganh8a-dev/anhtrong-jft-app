"""Gạch chân từ cần hỏi trong câu 文字と語彙 kiểu JFT (hỏi cách đọc / cách viết), như đề thi thật.
Dùng trong build_data.py: underline_exams(exams) – idempotent (bỏ qua câu đã có <u>)."""
import re
from sudachipy import dictionary, tokenizer
_T = dictionary.Dictionary().create(); _M = tokenizer.Tokenizer.SplitMode.C
k2h = lambda s: ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)
KJ = re.compile(r'[一-龯々]')
P = lambda s: re.sub(r'<rt>.*?</rt>|<[^>]+>', '', s or '')
OPT = lambda s: re.sub(r'^\s*[a-dA-D][\.\,．、]\s*', '', P(s)).strip()
BLANK = re.compile(r'_|＿|（\s*）|\(\s*\)|（　|（ー+）|\(ー+\)')
def find_target(t, r, want_kanji=True):
    toks = [(m.surface(), k2h(m.reading_form())) for m in _T.tokenize(t, _M)]
    pos = [0]
    for s, _ in toks: pos.append(pos[-1] + len(s))
    best = None
    for i in range(len(toks)):
        acc = ''
        for j in range(i, len(toks)):
            acc += toks[j][1]
            if acc == r:
                sub = t[pos[i]:pos[j + 1]]
                if (KJ.search(sub) if want_kanji else not KJ.search(sub)):
                    if best is None or len(sub) < best[1] - best[0]: best = (pos[i], pos[j + 1])
                break
            if not r.startswith(acc): break
    return best
def underline_q(q):
    if q.get('s') != '文字と語彙' or '<u>' in (q.get('t') or '') or q.get('imgs') or q.get('img'): return False
    t = q.get('t') or ''
    if '<' in t or BLANK.search(t) or not q.get('a'): return False
    opts = [OPT(o['t']) for o in q['o']]; c = opts[q['a'][0]]
    if not any(KJ.search(o) for o in opts):          # hỏi cách đọc: gạch chữ Hán có cách đọc = đáp án
        b = find_target(t, c, True)
    else:                                            # hỏi cách viết: gạch phần hiragana = cách đọc đáp án
        rd = ''.join(k2h(m.reading_form()) for m in _T.tokenize(c, _M))
        b = (t.index(rd), t.index(rd) + len(rd)) if rd in t else None
    if not b and len(t.strip()) <= 4 and KJ.search(t): b = (0, len(t))   # câu chỉ có 1 từ (vd. 9月)
    if not b: return False
    q['t'] = t[:b[0]] + '<u>' + t[b[0]:b[1]] + '</u>' + t[b[1]:]
    return True
def underline_exams(exams):
    n = 0
    for e in exams:
        for q in e['qs']: n += underline_q(q)
    return n
