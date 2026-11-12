"""Đề 28 (12/11/2026): đề tổng hợp sát đề thi thật tháng 11 — ghép câu có sẵn trong ngân hàng đề của app
(giữ nguyên ảnh, audio, đáp án, giải thích của câu gốc). Chủ đề theo phản hồi học viên đi thi:
động đất / sơ tán, rủ đi chơi, thông báo ngày giờ, phiếu giảm giá, đọc kanji, にぎやかで / そうです / すぎて.
Chạy: python3 src/jft/tonghop/build_t1.py  rồi  python3 src/build_data.py"""
import json, copy, os
P = os.path.join(os.path.dirname(__file__), '..', '..', 'raw', 'jft_exams.json')
d = json.load(open(P, encoding='utf-8'))
ex = {e['id']: e for e in d}
PICK = {
 '文字と語彙': [('g16',7),('f6',8),('f2',6),('f8',9),('f9',4),('y2',3),('y3',3),('f8',6),('f10',2),('g17',10),('f3',9),('f1',7)],
 '会話と表現': [('f5',16),('g24',17),('f10',23),('f2',15),('y3',20),('f1',21),('f7',19),('f3',16),('y2',16),('y2',19),('f4',20),('y2',13)],
 '聴解': [('f3',34),('f10',30),('f13',33),('f13',34),('f3',32),('f8',31),('f8',32),('f6',35),('f3',40),('f9',26),('f13',31),('f1',35)],
 '読解': [('f7',37),('f6',48),('f7',46),('f9',40),('f10',49),('f10',50),('g18',39),('f2',39),('g24',36),('g24',37),('f10',39),('g16',31)],
}
qs = []
for s, L in PICK.items():
    for e, n in L:
        q = copy.deepcopy(ex['jft-' + e]['qs'][n - 1]); assert q['s'] == s, (e, n)
        q['src'] = f"{ex['jft-'+e]['title']} · câu {n}"
        q['t'] = (q.get('t') or '').replace('泊まりした', '泊まりました')  # sửa lỗi gõ ở câu gốc
        qs.append(q)
new = {'id': 'jft-t1', 'group': 'Đề thi thử JFT-Basic', 'title': 'Đề 28',
       'sub': 'Sát đề thi thật tháng 11 · có phần nghe', 'time': 60, 'tag': 'Sát đề thật', 'qs': qs}
d = [e for e in d if e['id'] != 'jft-t1']
i = next(k for k, e in enumerate(d) if e['id'] == 'jft-y3')
d.insert(i + 1, new)
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Đề 28:', len(qs), 'câu')
