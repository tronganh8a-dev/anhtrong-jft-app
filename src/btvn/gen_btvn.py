#!/usr/bin/env python3
# Bài tập về nhà 25 buổi — dữ liệu từ いろどり (irodori.jpf.go.jp): từ vựng, 漢字のことば, 文法ワークシート, 聴解スクリプト
import json, re, random, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'
DD = B + '../../public/app/data/'
def load(f):
    s = open(DD + f, encoding='utf-8').read()
    return json.loads(s[s.index('=') + 1:s.index(';window.EXTLINKS') if 'EXTLINKS' in s else s.rindex(';')])
V = load('vocab.js')['words']; G = load('grammar.js'); SK = load('skills.js'); L = load('lessons.js')
X = json.load(open(B + 'lessons_extra.json', encoding='utf-8'))
LVJ = {'s1': '初級1', 's2': '初級2'}

def plain(s): return re.sub(r'\{([^|}]+)\|[^}]+\}', r'\1', s)
def kana(s): return re.sub(r'\{[^|}]+\|([^}]+)\}', r'\1', s)
def norm(s): return re.sub(r'[\s　。、．，,.!！?？「」『』（）()]', '', s)

def vocab(lv, b):
    out = [w for w in V if any(x[0] == LVJ[lv] and x[1] == b for x in w['l'])]
    out.sort(key=lambda w: [x[2] for x in w['l'] if x[0] == LVJ[lv] and x[1] == b][0]); return out
def gram(lv, b): return next((g for g in G if g['lv'] == LVJ[lv] and g['bai'] == b), None)

# ---------- distractors for kanji readings (JFT style)
DAK = dict(zip('かきくけこさしすせそたちつてとはひふへほ', 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'))
UND = {v: k for k, v in DAK.items()}
def perturb(y, rnd):
    c = set()
    for i, ch in enumerate(y):
        if ch in DAK: c.add(y[:i] + DAK[ch] + y[i + 1:])
        if ch in UND: c.add(y[:i] + UND[ch] + y[i + 1:])
        if ch == 'っ': c.add(y[:i] + y[i + 1:])
        if ch in 'うい' and i > 0: c.add(y[:i] + y[i + 1:])
        if ch in 'ょゅゃ': c.add(y[:i] + {'ょ': 'よ', 'ゅ': 'ゆ', 'ゃ': 'や'}[ch] + y[i + 1:])
    for i, ch in enumerate(y[:-1]):
        if ch in 'こそとのほもよろごぞどぼ' and y[i + 1] not in 'うー': c.add(y[:i + 1] + 'う' + y[i + 1:])
        if ch in 'かきくけこさしすせそたちてと' and y[i + 1] in 'かきくけこさしすせそたちつてとぱぴぷぺぽ': c.add(y[:i + 1] + 'っ' + y[i + 1:])
    c.discard(y); c = sorted(c); rnd.shuffle(c); return c

def mcq(q, opts, a, ex='', tag=''):
    return dict(t='mcq', q=q, o=opts, a=a, ex=ex, tag=tag)
def shuf(rnd, correct, wrong):
    o = [correct] + wrong; rnd.shuffle(o); return o, o.index(correct)

# ---------- section builders
def sec_vocab(rnd, pairs, n_each=5, title='Từ vựng', jp='語彙'):
    items = []; pool = []
    for lv, b in pairs: pool += vocab(lv, b)
    for lv, b in pairs:
        ws = [w for w in vocab(lv, b) if len(w['v']) < 40]
        rnd.shuffle(ws)
        for w in ws[:n_each]:
            cands = [x['v'] for x in pool if x['v'] != w['v'] and x['h'] != w['h'] and ('.' in x['v']) == ('.' in w['v']) and abs(len(x['v']) - len(w['v'])) <= 12]
            rnd.shuffle(cands); wrong = list(dict.fromkeys(cands))[:3]
            if len(wrong) < 3:
                more = [x['v'] for x in pool if x['v'] != w['v'] and x['v'] not in wrong and x['h'] != w['h']]; rnd.shuffle(more); wrong += list(dict.fromkeys(more))[:3 - len(wrong)]
            o, a = shuf(rnd, w['v'], wrong)
            q = (f'{{{w["h"]}|{w["y"]}}}' if w['k'] and w['h'] != w['y'] else w['h'])
            items.append(mcq(q, o, a, f'{w["h"]}（{w["y"]}）' + (f' · {w["hv"]}' if w.get('hv') else '') + f' — {w["v"]}', 'jpq'))
    return dict(id='voc', title=title, jp=jp, ins='Chọn nghĩa tiếng Việt đúng của từ.', ins_jp='ことばの意味を選んでください。', items=items)

def sec_kanji_read(rnd, keys, n=8, title='Chữ Hán — cách đọc', jp='漢字の読み'):
    cand = []
    for k in keys:
        for s in X[k]['sen']:
            for w, y in s['tg']: cand.append((s, w, y))
    rnd.shuffle(cand); items = []; seen = set(); used_s = set()
    for s, w, y in cand:
        if w in seen or id(s) in used_s: continue
        ds = perturb(y, rnd)[:2]
        if len(ds) < 2: continue
        seen.add(w); used_s.add(id(s))
        # sentence: target underlined without reading, other targets shown with reading
        def rep(m):
            tw, ty = m.group(1), m.group(2)
            return f'<u>{tw}</u>' if tw == w else f'{{{tw}|{ty}}}'
        q = re.sub(r'⟦([^|⟧]+)\|([^⟧]+)⟧', rep, re.sub(r'^[①-⑳]\s*', '', s['jp']), count=0)
        o, a = shuf(rnd, y, ds)
        items.append(mcq(q, o, a, f'{w} = {y}. {s["vi"]}', 'jpq'))
        if len(items) == n: break
    return dict(id='kr', title=title, jp=jp, ins='Chọn cách đọc đúng của từ gạch chân.', ins_jp='＿＿のことばの読み方を選んでください。', items=items)

def sec_kanji_write(rnd, keys, n=6, title='Chữ Hán — mặt chữ', jp='漢字の表記'):
    pool = [kw for k in keys for kw in X[k]['kanji']]
    allk = [kw for k in X for kw in X[k]['kanji']]
    rnd.shuffle(pool); items = []
    for kw in pool[:n]:
        same = [x['w'] for x in allk if x['w'] != kw['w'] and len(x['w']) == len(kw['w']) and x['y'] != kw['y']]
        rnd.shuffle(same); wrong = list(dict.fromkeys(same))[:2]
        if len(wrong) < 2: continue
        o, a = shuf(rnd, kw['w'], wrong)
        items.append(mcq(f'<span class="kana">{kw["y"]}</span><span class="hint">（{kw["vi"]}）</span>', o, a, f'{kw["w"]}（{kw["y"]}）· {kw["hv"]} — {kw["vi"]}', 'jpo'))
    return dict(id='kw', title=title, jp=jp, ins='Chọn cách viết bằng chữ Hán đúng.', ins_jp='正しい漢字を選んでください。', items=items)

def sec_ws(rnd, pairs, n=6):
    cand = []
    for lv, b in pairs:
        g = gram(lv, b)
        if not g: continue
        for p in g['points']:
            for blk in p.get('worksheet', []):
                for it in blk.get('items', []):
                    q = it['q']
                    if it['type'] == 'choice' and q.count('＿＿') == 1 and len(it.get('choices', [])) >= 2 and it.get('answer'):
                        cand.append(('c', p, blk, it))
                    elif it['type'] == 'fill' and q.count('＿＿') == 1 and it.get('answer') and len(plain(it['answer'][0])) <= 22:
                        cand.append(('f', p, blk, it))
    rnd.shuffle(cand)
    # spread across points
    items = []; used = set()
    for kind, p, blk, it in cand:
        key = (p['pattern'], blk['ins_jp'])
        if key in used and len(cand) > n * 2: continue
        used.add(key)
        q = re.sub(r'^\s*\d+[\.．、]\s*', '', it['q'])
        if kind == 'c':
            ch = it['choices']; ans = plain(it['answer'][0])
            ai = next((i for i, c in enumerate(ch) if norm(plain(c)) == norm(ans) or norm(kana(c)) == norm(kana(it['answer'][0]))), None)
            if ai is None: continue
            items.append(dict(t='mcq', q=q, o=ch, a=ai, ex=f'Mẫu: {p["pattern"]} — {p.get("meaning_vi","")}', ins=blk.get('ins_vi', ''), tag='jpq jpo', img=it.get('img')))
        else:
            acc = []
            for a_ in it['answer']:
                for part in re.split(r'[／/]', a_):
                    for v in (plain(part), kana(part)):
                        v = v.strip()
                        if v and v not in acc: acc.append(v)
            items.append(dict(t='fill', q=q, ans=acc, show=plain(it['answer'][0]), ex=f'Mẫu: {p["pattern"]} — {p.get("meaning_vi","")}', ins=blk.get('ins_vi', ''), ex_q=blk.get('example'), img=it.get('img')))
        if len(items) == n: break
    return dict(id='ws', title='Ngữ pháp — bài tập ワークシート', jp='文法ワークシート', ins='Điền vào chỗ trống ＿＿ hoặc chọn đáp án đúng (bài tập chính thức của いろどり).', ins_jp='＿＿に入ることばを書きましょう／選びましょう。', items=items)

def sec_quiz(rnd, pairs, n_each=3, lvname=None, title='Ngữ pháp — trắc nghiệm kiểu JFT', total=None):
    cand = []
    for lv, b in pairs:
        g = next((x for x in G if x['lv'] == (lvname or LVJ[lv]) and x['bai'] == b), None)
        if not g: continue
        qs = [(p, q) for p in g['points'] for q in p.get('quiz', [])]
        rnd.shuffle(qs); cand.append(qs)
    items = []
    if total:
        flat = [x for qs in cand for x in qs]; rnd.shuffle(flat); sel = flat[:total]
    else:
        sel = [x for qs in cand for x in qs[:n_each]]
    for p, q in sel:
        o, a = shuf(rnd, q['o'][q['a']], [x for i, x in enumerate(q['o']) if i != q['a']])
        items.append(mcq(q['q'], o, a, q.get('ex_vi', ''), 'jpq jpo'))
    return dict(id='qz', title=title, jp='文法・JFT形式', ins='Chọn từ / cụm từ đúng điền vào （　）. Câu hỏi do Anh Trọng Dạy JFT soạn theo mẫu của bài.', ins_jp='（　）に入れるのに一番いいものを選んでください。', items=items)

def dialogues(keys):
    out = []
    for k in keys:
        for d in X[k]['scripts']:
            ls = [dict(l, s={'Ａ': 'A', 'Ｂ': 'B'}.get(l['s'], l['s'])) for l in d['lines'] if l['s'] in ('A', 'B', 'Ａ', 'Ｂ')]
            if len(ls) >= 2: out.append((k, d, ls))
    return out

def sec_kaiwa(rnd, keys, n_pick=3, n_tr=3, title='Hội thoại', jp='会話'):
    ds = dialogues(keys); rnd.shuffle(ds); items = []
    allB = [(k, l) for k, d, ls in ds for l in ls]
    for k, d, ls in ds:
        idx = [i for i, l in enumerate(ls) if i > 0 and 4 <= len(plain(l['jp'])) <= 40]
        if not idx: continue
        i = rnd.choice(idx); tgt = ls[i]
        wrong = [l['jp'] for kk, l in allB if plain(l['jp']) != plain(tgt['jp']) and l not in ls and 4 <= len(plain(l['jp'])) <= 40]
        rnd.shuffle(wrong); wrong = list(dict.fromkeys(wrong))[:2]
        if len(wrong) < 2: continue
        ctx = ls[max(0, i - 2):i]
        q = '<br>'.join(f'{l["s"]}：{l["jp"]}' for l in ctx) + f'<br>{tgt["s"]}：（　　　　）'
        o, a = shuf(rnd, tgt['jp'], wrong)
        items.append(dict(t='mcq', q=q, o=o, a=a, ex=f'{tgt["s"]}：{plain(tgt["jp"])} — {tgt["vi"]}', tag='jpq jpo', ins=f'{d["sec"]}'))
        if len(items) == n_pick: break
    pick = [l for k, d, ls in ds for l in ls if 6 <= len(plain(l['jp'])) <= 24 and l['vi']]
    rnd.shuffle(pick); seenv = set()
    for l in pick:
        if l['vi'] in seenv: continue
        seenv.add(l['vi'])
        items.append(dict(t='write', q=l['vi'], model=l['jp'], ex='Câu trong hội thoại của bài (聴解スクリプト).'))
        if sum(1 for x in items if x['t'] == 'write') == n_tr: break
    return dict(id='kw2', title=title, jp=jp, ins='Phần 1: chọn câu phù hợp điền vào hội thoại. Phần 2: dịch câu tiếng Việt sang tiếng Nhật rồi đọc to 3 lần.', ins_jp='会話を完成させましょう。／日本語で言いましょう。', items=items)

def sec_meaning_lines(rnd, keys, n=10, title='Đọc hiểu câu — chọn nghĩa', jp='文の意味'):
    lines = [l for k in keys for d in X[k]['scripts'] for l in d['lines'] if l['vi'] and 8 <= len(plain(l['jp'])) <= 60]
    rnd.shuffle(lines); items = []; used = set()
    for l in lines:
        if l['vi'] in used: continue
        wrong = [x['vi'] for x in rnd.sample(lines, min(12, len(lines))) if x['vi'] != l['vi']][:2]
        if len(wrong) < 2: continue
        used.add(l['vi']); o, a = shuf(rnd, l['vi'], wrong)
        items.append(mcq(l['jp'], o, a, plain(l['jp']), 'jpq'))
        if len(items) == n: break
    return dict(id='ml', title=title, jp=jp, ins='Đọc câu tiếng Nhật và chọn nghĩa đúng.', ins_jp='文を読んで、意味を選んでください。', items=items)

def sec_app(lines): return dict(id='app', title='Làm trên app', jp='アプリで', ins='Đánh dấu khi đã làm xong.', items=[dict(t='check', q=x) for x in lines])

# ---------- schedule (khớp Lộ trình 25 buổi)
TOPIC = [('s1', 1, '今の私', 'Tôi hiện tại'), ('s1', 3, '季節と天気', 'Mùa và thời tiết'), ('s1', 5, '私の町', 'Thị trấn của tôi'),
         ('s1', 7, 'いっしょに出かける', 'Cùng nhau đi chơi'), ('s1', 9, '日本語学習', 'Học tiếng Nhật'), ('s1', 11, 'おいしい料理', 'Món ăn ngon'),
         ('s1', 13, '仕事の連絡', 'Liên lạc trong công việc'), ('s1', 15, '健康な生活', 'Sống khoẻ'), ('s1', 17, '交際', 'Giao tiếp, quan hệ'),
         ('s2', 1, '私の周りの人たち', 'Những người quanh tôi'), ('s2', 3, 'レストランで', 'Ở nhà hàng'), ('s2', 5, '旅行に行こう', 'Cùng đi du lịch'),
         ('s2', 7, '地域のイベント', 'Sự kiện địa phương'), ('s2', 9, '年中行事とマナー', 'Lễ hội trong năm và phép lịch sự'), ('s2', 11, '上手な買い物', 'Mua sắm khéo'),
         ('s2', 13, 'さまざまなサービス', 'Các loại dịch vụ'), ('s2', 15, '自然と環境', 'Thiên nhiên và môi trường'), ('s2', 17, '私の人生', 'Cuộc đời tôi')]
HW_EXAM = {1: 'Đề 01 — bài kiểm tra đầu vào (chế độ thi 60 phút, ghi điểm từng phần)', 9: 'Đề 02 — mốc cuối 初級1 (chế độ thi 60 phút)',
           **{s: f'Đề {s - 7:02d} — chế độ thi 60 phút, ghi điểm từng phần' for s in range(10, 18)}, 18: 'Làm lại các câu sai của Đề 01–10'}
def skc(lv, b, sec): return sum(1 for q in SK if q['lv'] == lv and q['bai'] == b and q['sec'] == sec)
def lesson_title(lv, b): return next(l for l in L if l['lv'] == lv and l['bai'] == b)

ALLK = [k for k in X]
ALLP = [(lv, b) for lv in ('s1', 's2') for b in range(1, 19)]
sessions = []
for i, (lv, a, tj, tv) in enumerate(TOPIC):
    no = i + 1; rnd = random.Random(1000 + no); pairs = [(lv, a), (lv, a + 1)]; keys = [f'{lv}-{a}', f'{lv}-{a + 1}']
    secs = []
    if no == 1: secs.append(dict(sec_quiz(rnd, [('s1', b) for b in range(3, 19)], lvname='入門', total=8, title='Ôn tập 入門 — trắc nghiệm'), id='ny'))
    secs += [sec_vocab(rnd, pairs), sec_kanji_read(rnd, keys), sec_kanji_write(rnd, keys), sec_ws(rnd, pairs), sec_quiz(rnd, pairs), sec_kaiwa(rnd, keys)]
    nl = sum(skc(lv, x, 'listen') for x in (a, a + 1)); nr = sum(skc(lv, x, 'read') for x in (a, a + 1))
    app = [f'Từ vựng Bài {a}–{a + 1}: thẻ ghi nhớ + trắc nghiệm đến khi đạt 90%', f'Web bài học Bài {a}–{a + 1}: làm các Can-do Đọc / Viết']
    if nl or nr: app.append(f'Luyện kỹ năng Bài {a}–{a + 1}: {nl} câu nghe' + (f', {nr} câu đọc' if nr else ''))
    if no in HW_EXAM: app.append(HW_EXAM[no])
    secs.append(sec_app(app))
    la, lb = lesson_title(lv, a), lesson_title(lv, a + 1)
    sessions.append(dict(no=no, kind='lesson', lvj=LVJ[lv], bai=f'Bài {a}–{a + 1}', tj=tj, tv=tv,
                         sub=[f'Bài {a} {la["jp"]}', f'Bài {a + 1} {lb["jp"]}'], secs=secs))

def ex_sess(no, tj, tv, secs, sub):
    sessions.append(dict(no=no, kind='exam', lvj='Luyện đề', bai='初級1–2', tj=tj, tv=tv, sub=sub, secs=secs))
r = random.Random(19); ex_sess(19, '文字と語彙', 'Chữ và từ vựng', [
    sec_kanji_read(r, ALLK, 20), sec_kanji_write(r, ALLK, 10), sec_vocab(r, r.sample(ALLP, 12), 2),
    sec_app(['Đề 12 — chế độ thi 60 phút, ghi điểm từng phần', 'Bảng lỗi 文字と語彙 của Đề 01–10: chép lại 10 từ hay sai'])], ['Tổng ôn từ vựng và chữ Hán 初級1–2'])
r = random.Random(20); ex_sess(20, '会話と表現', 'Hội thoại và cách diễn đạt', [
    sec_quiz(r, ALLP, total=20), sec_kaiwa(r, ALLK, 8, 4),
    sec_app(['Đề 14 — chế độ thi 60 phút', 'Đóng vai 6 tình huống công việc: 初級1 Bài 13–14, 初級2 Bài 13–14'])], ['Tổng ôn mẫu câu giao tiếp 初級1–2'])
r = random.Random(21)
lis_keys = ['s2-7', 's2-9', 's2-16', 's1-13', 's1-15']
ex_sess(21, '聴解', 'Nghe hiểu', [
    sec_meaning_lines(r, lis_keys, 12, 'Hiểu câu trong bài nghe — chọn nghĩa', '聴解スクリプト'), sec_kaiwa(r, lis_keys, 5, 3),
    sec_app(['Luyện kỹ năng phần Nghe: 初級2 Bài 7, 9, 16 (nghe tối đa 2 lần mỗi câu)', 'Shadowing: nghe và nói đuổi 3 đoạn hội thoại trong web bài học 初級2 Bài 9, 16', 'Đề 16 — chế độ thi 60 phút'])], ['Câu trong script bài nghe 初級1–2'])
r = random.Random(22)
rd_keys = ['s1-4', 's1-11', 's2-9', 's2-12', 's2-16', 's2-10']
ex_sess(22, '読解', 'Đọc hiểu', [
    sec_meaning_lines(r, rd_keys, 12), sec_kanji_read(r, rd_keys, 10),
    sec_app(['Luyện kỹ năng phần Đọc: 初級1 Bài 4, 11 · 初級2 Bài 9, 12', 'Đề 18 — chế độ thi 60 phút'])], ['Đọc hiểu câu và chữ Hán trong bài đọc'])
r = random.Random(23)
ex_sess(23, '文法の総復習', 'Tổng ôn ngữ pháp 3 chuyên đề', [
    dict(sec_quiz(r, [('s2', 5), ('s2', 7), ('s2', 13), ('s2', 16), ('s2', 18)], total=10, title='Chuyên đề 1 — các thể động từ (可能・受身・意向・命令)'), id='q1'),
    dict(sec_quiz(r, [('s1', 17), ('s1', 18), ('s2', 18)], total=8, title='Chuyên đề 2 — cho / nhận (あげる・くれる・もらう)'), id='q2'),
    dict(sec_quiz(r, [('s2', 3), ('s2', 7), ('s2', 13), ('s2', 16), ('s2', 4)], total=10, title='Chuyên đề 3 — điều kiện, lý do (たら・ても・なら・ので)'), id='q3'),
    sec_ws(r, [('s2', 5), ('s2', 7), ('s2', 13), ('s2', 16), ('s2', 18)], 8),
    sec_app(['Làm lại câu sai Đề 11–18', 'Ghi 3 chuyên đề hay sai nhất vào bảng lỗi cá nhân'])], ['Thể động từ · cho nhận · điều kiện'])
r = random.Random(24)
ex_sess(24, '総合ミニテスト', 'Kiểm tra tổng hợp', [
    sec_vocab(r, r.sample(ALLP, 8), 1), sec_kanji_read(r, ALLK, 8), sec_kanji_write(r, ALLK, 6), sec_quiz(r, ALLP, total=12), sec_kaiwa(r, ALLK, 4, 2),
    sec_app(['Ôn theo kế hoạch cá nhân; làm lại câu sai Đề 11–19'])], ['40 câu tổng hợp 初級1–2'])
r = random.Random(25)
ex_sess(25, '試験前チェック', 'Khởi động trước ngày thi', [
    sec_kanji_read(r, ALLK, 8), sec_quiz(r, ALLP, total=8), sec_vocab(r, r.sample(ALLP, 4), 1),
    sec_app(['Mang giấy tờ tuỳ thân theo hướng dẫn của kỳ thi; đến sớm', 'Xem lại bảng lỗi cá nhân — không học nội dung mới', 'Ngủ đủ giấc trước ngày thi'])], ['Làm nhẹ 20 câu, xem lại bảng lỗi'])

for s in sessions:
    n = 0
    for sec in s['secs']:
        for it in sec['items']:
            if it['t'] != 'check': n += 1; it['n'] = n
    s['total'] = n
json.dump(sessions, open(B + 'sessions.json', 'w'), ensure_ascii=False)
for s in sessions: print(s['no'], s['total'], [ (x['id'], len(x['items'])) for x in s['secs']])
