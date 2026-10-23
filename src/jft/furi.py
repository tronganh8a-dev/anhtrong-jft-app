"""Thêm furigana (ruby) cho chữ Hán trong chuỗi tiếng Nhật — SudachiPy + bảng sửa tay."""
import re, json, os, html
from sudachipy import dictionary, tokenizer
_T = dictionary.Dictionary().create(); _M = tokenizer.Tokenizer.SplitMode.C
H = os.path.dirname(os.path.abspath(__file__)) + '/'
FIX = json.load(open(H + 'furi_fix.json')) if os.path.exists(H + 'furi_fix.json') else {}   # "surface|reading_sai": "reading_đúng"  hoặc "surface": "reading"
KANJI = r'[㐀-鿿々〆ヶ]'
def k2h(s): return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)
USED = {}
def ruby_word(surf, read):
    """surf có kanji; read = hiragana. Tách okurigana bằng regex."""
    parts = re.findall(KANJI + r'+|[^㐀-鿿々〆ヶ]+', surf)
    pat = ''.join('(.+?)' if re.match(KANJI, p) else '(' + re.escape(k2h(p)) + ')' for p in parts)
    m = re.fullmatch(pat, read)
    if not m: return f'<ruby>{surf}<rt>{read}</rt></ruby>'
    return ''.join(f'<ruby>{p}<rt>{g}</rt></ruby>' if re.match(KANJI, p) else p for p, g in zip(parts, m.groups()))
def furi_run(s):
    out = []
    toks = list(_T.tokenize(s, _M))
    for i, t in enumerate(toks):
        surf = t.surface()
        if not re.search(KANJI, surf): out.append(surf); continue
        read = k2h(t.reading_form())
        prev = toks[i - 1].surface() if i else ''
        nxt = toks[i + 1].surface() if i + 1 < len(toks) else ''
        if re.search(r'[0-9０-９]$', prev) and re.match(r'(日|分|人|本|階|杯|匹|泊|足|個|歳|才)', surf):
            out.append(surf); continue
        if surf == '何':
            read = 'なん' if re.match(r'(で|だ|と|の(?!ん)|時|人|回|日|歳|分|本|枚|階|番|曜|年|月|個|名|語|円|線|度|か月|ヶ月|週|色|号|点|倍|ページ)', nxt) else 'なに'
            out.append(ruby_word(surf, read)); continue
        key = f'{surf}|{read}'
        if prev + '>' + key in FIX: read = FIX[prev + '>' + key]
        elif key in FIX: read = FIX[key]
        elif surf in FIX: read = FIX[surf]
        u = USED.setdefault(f'{surf}|{read}', [])
        if len(u) < 3: u.append([prev, s[max(0, s.find(surf) - 10): s.find(surf) + len(surf) + 8]])
        if not read or read == surf: out.append(surf); continue
        out.append(ruby_word(surf, read))
    return ''.join(out)
JRUN = re.compile(r'[぀-ヿ㐀-鿿々〆ヶー〜～・0-9０-９、。！？!?「」『』（）()・…]+')
def furi(text_escaped):
    """Nhận chuỗi đã html-escape (không có thẻ), trả về HTML có ruby cho các đoạn tiếng Nhật chứa kanji."""
    return JRUN.sub(lambda m: furi_run(m.group(0)) if re.search(KANJI, m.group(0)) else m.group(0), text_escaped)
