"""Bản dùng thử TIẾNG ANH (chỉ phần Làm đề) → demo/public/en.html + demo/public/app/data/exams_en.js
Gọi từ cuối src/build_demo.py (trước khi chép sang public/_demo): run(s, D, P, FB, TT, PANEL, AD_HTML, DHV_HTML).
Link: https://jft-dungthu.tronganh8a.workers.dev/en  (worker phục vụ /_demo/en.html, không cần đăng nhập)
Dịch: src/en/tr/<id>.txt (khoá giống src/en/src/<id>.txt do extract.py sinh)."""
import json, re, os, hashlib
A = os.path.dirname(os.path.abspath(__file__)) + '/'
import importlib.util
_sp = importlib.util.spec_from_file_location('en_extract', A + 'extract.py'); X = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(X)
VN = re.compile('[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', re.I)
def expand(t): return re.sub(r'\{([^{}|]+)\|([^{}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', t)
def read_units(path):
    U, k = {}, None
    if not os.path.exists(path): return U
    for line in open(path, encoding='utf-8').read().split('\n'):
        m = re.match(r'^@(\d+\.\w+)\b', line)
        if m: k = m.group(1); U[k] = ''; continue
        if k is not None and line.strip(): U[k] = (U[k] + ' ' + line.strip()).strip()
    return U
LB = {'DỊCH': 'TRANSLATION', 'GIẢI THÍCH': 'EXPLANATION', 'TỪ VỰNG': 'VOCABULARY', 'SCRIPT (đoạn chính)': 'SCRIPT (key part)', 'SCRIPT': 'SCRIPT'}
META = {'jft-y3': ('Mock Test 1', 'With listening · いろどり Elementary 1', 'New'),
        'jft-y4': ('Mock Test 2', 'With listening · 40 questions', None),
        'jft-y5': ('Mock Test 3', 'With listening · いろどり Elementary 1', 'New'),
        'jft-ln1': ('Listening Test 1', '20 listening questions · いろどり', 'Listening'),
        'jft-ln2': ('Listening Test 2', '20 listening questions · いろどり', 'Listening'),
        'jft-vocab': ('Vocabulary & Kanji Review', 'Words and kanji that often appear on the test', None)}
def tr_exam(e, strict):
    U = read_units(A + f'tr/{e["id"]}.txt'); miss = []
    e = json.loads(json.dumps(e))
    for i, q in enumerate(e['qs']):
        src = {k: (t, c) for k, t, c in X.units(q)}
        key = lambda k: f'{i + 1}.{k}'
        if 'q' in src:
            en = U.get(key('q'))
            if en is None: miss.append(key('q'))
            else: q['t'] = re.sub(r'<span class="vi-q">.*?</span>', '<span class="vi-q">' + expand(en) + '</span>', q['t'])
        ns = X.nodes(q.get('ex') or '')
        for k, n in enumerate(ns):
            if n.startswith('<span class="lb">'):
                lab = re.sub('<[^>]+>', '', n); ns[k] = f'<span class="lb">{LB.get(lab, lab)}</span>'; continue
            if str(k) not in src:
                if n.startswith('<div class="ans">'): ns[k] = n.replace('Đáp án đúng:', 'Correct answer:', 1)
                continue
            t, c = src[str(k)]; en = U.get(key(k))
            if en is None: miss.append(key(k)); continue
            if t == 'ANS': ns[k] = '<div class="ans">Correct answer: ' + expand(en) + '</div>'
            elif t == 'TV':
                jps = [p.split(' = ', 1)[0] for p in c.split(' || ')]; ens = [x.strip() for x in en.split(' || ')]
                assert len(jps) == len(ens), f'{e["id"]} {key(k)}: số từ không khớp'
                ns[k] = '<ul>' + ''.join(f'<li><span class="jp">{expand(j)}</span> – {expand(m)}</li>' for j, m in zip(jps, ens)) + '</ul>'
            else:
                op = re.match(r'^<(div|p|span)[^>]*>', n); tag = op.group(1) if op else None
                ns[k] = (op.group(0) + expand(en) + f'</{tag}>') if op else expand(en)
        q['ex'] = ''.join(ns)
    title, sub, tag = META[e['id']]
    e.update(title=title, sub=sub, group='Free trial tests'); e.pop('tag', None)
    if tag: e['tag'] = tag
    if e['id'].startswith('jft-ln'): e['name'] = 'L' + e['id'][-1]
    NAMES = re.compile(r'Huyền|Vương|Quách|Dương|José|Phương|Anh Trọng|Đ(?=ề)')
    left = [f'{i + 1}' for i, q in enumerate(e['qs']) if VN.search(NAMES.sub('', re.sub(r'<[^>]+>', '', (q.get('t') or '') + (q.get('ex') or ''))))]
    if strict: assert not miss and not left, f'{e["id"]}: thiếu {miss[:8]} · còn chữ Việt ở câu {left[:8]}'
    return e, miss, left

def en_locked(e):
    t = e['title']; m = re.match(r'Đề (\d+)$', t); ln = re.match(r'Đề nghe (\d+)$', t)
    title = f'Mock Test {m.group(1)}' if m else f'Listening Test {ln.group(1)}' if ln else 'Conversation & Expression Review'
    sub = (e.get('sub') or '').replace('Có phần nghe', 'With listening').replace('Không có phần nghe', 'No listening section') \
        .replace('Tuyển tập 20 câu nghe hiểu', '20 listening questions').replace('Sát đề thi thật tháng 11 · có phần nghe', 'Close to the real November test · with listening') \
        .replace('JLPT N4 · cấp độ tầm trung · 28 câu', 'JLPT N4 level · 28 questions').replace('Hội thoại & diễn đạt', 'Conversation & expression').replace('いろどり 初級1', 'いろどり Elementary 1')
    grp = 'Listening practice' if ln else 'JFT-Basic mock tests' if m else 'Key review'
    o = {k: v for k, v in e.items() if k not in ('doc', 'tag', 'name')}
    o.update(title=title, sub=sub, group=grp)
    if ln: o['name'] = 'L' + ln.group(1)
    return o

UI = [  # (chuỗi tiếng Việt trong trang dùng thử, tiếng Anh) — chỉ phần Làm đề
    ('<html lang="vi">', '<html lang="en">'),
    ('aria-label="Điều hướng chính"', 'aria-label="Main navigation"'),
    ('<small>Học · Luyện thi JFT-Basic</small>', '<small>JFT-Basic practice tests</small>'),
    ('Làm đề<span class="jp">模擬試験</span></button>', 'Mock tests<span class="jp">模擬試験</span></button>'),
    ('<h1>Làm đề<span class="jp">模擬試験 · JFT-Basic</span></h1>', '<h1>JFT-Basic Mock Tests<span class="jp">模擬試験 · Free trial</span></h1>'),
    ('aria-label="Màn hình làm bài"', 'aria-label="Test screen"'),
    ('aria-label="Các phần thi"', 'aria-label="Sections"'), ('aria-label="Số câu"', 'aria-label="Questions"'),
    ('title="Bật/tắt tiếng Việt" aria-label="Bật/tắt tiếng Việt"', 'title="Show/hide English" aria-label="Show/hide English"'),
    ('title="Xem danh sách câu" aria-label="Danh sách câu"', 'title="Question list" aria-label="Question list"'),
    ('<button class="ex" id="cbtClose" type="button">Thoát</button>', '<button class="ex" id="cbtClose" type="button">Exit</button>'),
    ('title="Đánh dấu câu này" aria-label="Đánh dấu"', 'title="Flag this question" aria-label="Flag"'),
    ('<h3>Danh sách câu · <span id="gTitle"></span></h3>', '<h3>Questions · <span id="gTitle"></span></h3>'),
    ('Xanh: đã trả lời · Viền đỏ: đã đánh dấu. Bấm vào số để đến câu đó.', 'Blue: answered · Red border: flagged. Tap a number to go to that question.'),
    ('id="gClose" type="button" style="margin-top:12px">Đóng</button>', 'id="gClose" type="button" style="margin-top:12px">Close</button>'),
    # danh sách đề
    ("<b style=\"font-size:1.15rem\">Bộ đề mới đang được cập nhật</b><p class=\"muted\" style=\"margin-top:6px\">Đề thi thử mới (có đáp án và giải thích) sẽ sớm có mặt tại đây.</p>",
     "<b style=\"font-size:1.15rem\">New tests are coming soon</b><p class=\"muted\" style=\"margin-top:6px\">New mock tests with answers and explanations will appear here.</p>"),
    ("${e.short?'Ôn tập':'Đề thi thử'} · ${e.nq||e.qs.length} câu", "${e.short?'Review':(e.name?'Listening test':'Mock test')} · ${e.nq||e.qs.length} questions"),
    ('`<small>Đề</small><i class="nm">${esc(e.name)}</i>`:`<small>Đề</small>${no}`', '`<small>Test</small><i class="nm">${esc(e.name)}</i>`:`<small>Test</small>${no}`'),
    ('<span class="go">Bắt đầu làm bài <i>→</i></span>', '<span class="go">Start <i>→</i></span>'),
    ('Mỗi câu đều có đáp án và giải thích song ngữ Nhật – Việt. Bấm vào đề là làm luôn: chọn đáp án câu nào là hiện ngay đáp án đúng và giải thích của câu đó.',
     'Every question comes with the correct answer and a clear explanation in English. Tap a test to begin: as soon as you choose an answer, you will see whether it is right, along with the explanation.'),
    ("`${x.qs.length} câu · ${x.time} phút`", "`${x.qs.length} questions · ${x.time} min`"),
    ("▶ Làm tiếp bài đang dở · ${pr?'Luyện tập':'Thi thử'}", "▶ Continue where you left off · ${pr?'Practice':'Timed test'}"),
    ("`Làm lại từ đầu? Bài đang làm dở (${dgDone(r)}/${r.n} câu) sẽ bị xoá.`,'Làm lại'", "`Start over? Your saved progress (${dgDone(r)}/${r.n} questions) will be deleted.`,'Start over'"),
    # màn làm bài
    ("'Anh Trọng Dạy JFT · '+e.title+(pr?' · Luyện tập':'')", "'Anh Trọng Dạy JFT · '+e.title+(pr?' · Practice':'')"),
    ("$('#finBtn').textContent=pr?'Kết thúc':'Finish Section'", "$('#finBtn').textContent=pr?'Finish':'Finish Section'"),
    ("askOK('Thoát ra? Bài làm của em được lưu lại.\\nLần sau mở lại đề này, bấm \"Làm tiếp\" để làm tiếp từ câu đang dở.','Thoát')",
     "askOK('Exit now? Your answers are saved.\\nOpen this test again to continue from where you stopped.','Exit')"),
    ("askOK('Thoát bài đang làm? Kết quả sẽ không được lưu.','Thoát')", "askOK('Exit this test? Your results will not be saved.','Exit')"),
    ('aria-label="Phát">▶</button>', 'aria-label="Play">▶</button>'),
    ('alt="Hình" loading="lazy"', 'alt="Picture" loading="lazy"'),
    ('`<button class="langbtn" id="langBtn" type="button">Tiếng Việt</button><div class="langbox" id="langBox">${viTxt||\'Nghĩa các lựa chọn hiện bên dưới.\'}</div>`',
     '`<button class="langbtn" id="langBtn" type="button">English</button><div class="langbox" id="langBox">${viTxt||\'The meaning of each option is shown below it.\'}</div>`'),
    ('`<div class="qgno${m===S.i?\' cur\':\'\'}">Câu ${sec.idx.indexOf(m)+1}</div>`', '`<div class="qgno${m===S.i?\' cur\':\'\'}">Question ${sec.idx.indexOf(m)+1}</div>`'),
    ('title="Video nghe"', 'title="Listening video"'), ('alt="Hình câu hỏi"', 'alt="Question picture"'),
    ('Chọn tất cả đáp án đúng.', 'Choose all correct answers.'), ('alt="Lựa chọn ${k+1}"', 'alt="Option ${k+1}"'),
    ('type="button">Kiểm tra</button>', 'type="button">Check</button>'),
    ("'Đúng rồi!':'Chưa đúng — đáp án đúng được tô xanh.'):'Câu này chưa có đáp án.'", "'Correct!':'Not quite — the correct answer is highlighted in green.'):'No answer key for this question.'"),
    ('Nguồn: ${esc(Q.src)}', 'Source: ${esc(Q.src)}'),
    ("`<div class=\"qgno\">Câu ${sec.idx.indexOf(m)+1}</div>`", "`<div class=\"qgno\">Question ${sec.idx.indexOf(m)+1}</div>`"),
    # khung giải thích
    ('m=t.match(/^\\s*Đáp án đúng:\\s*([\\s\\S]*)$/)', 'm=t.match(/^\\s*(?:Đáp án đúng|Correct answer):\\s*([\\s\\S]*)$/)'),
    ('<small>Đáp án đúng</small>', '<small>Correct answer</small>'),
    ("/DỊCH/.test(lb)?'dich':/GIẢI THÍCH/.test(lb)?'gt':/TỪ VỰNG/.test(lb)?'tv'", "/DỊCH|TRANSLATION/.test(lb)?'dich':/GIẢI THÍCH|EXPLANATION/.test(lb)?'gt':/TỪ VỰNG|VOCABULARY/.test(lb)?'tv'"),
    ("o+=box('gt','Giải thích',b)", "o+=box('gt','Explanation',b)"),
    ("/đoạn chính/.test(s.lb)?'Script · đoạn chính':'Script · スクリプト'", "/đoạn chính|key part/.test(s.lb)?'Script · key part':'Script · スクリプト'"),
    ("o+=box('dich','Dịch',_xDich(s.nodes))", "o+=box('dich','Translation',_xDich(s.nodes))"),
    ("o+=box('tv','Từ vựng',_xTv(s.nodes))", "o+=box('tv','Vocabulary',_xTv(s.nodes))"),
    # kết thúc / nộp bài
    ("askOK('Kết thúc bài luyện và xem kết quả?','Kết thúc')", "askOK('Finish practice and see your results?','Finish')"),
    ("(un?`Còn ${un} câu chưa trả lời. `:'')+(last?'Kết thúc phần cuối và nộp bài?':'Kết thúc phần này? Bạn sẽ không quay lại phần này được.'),last?'Nộp bài':'Kết thúc'",
     "(un?`${un} question(s) not answered yet. `:'')+(last?'Finish the last section and submit?':'Finish this section? You cannot return to it.'),last?'Submit':'Finish'"),
    ('<button type="button" class="no">Huỷ</button>', '<button type="button" class="no">Cancel</button>'),
    ("o.querySelector('.ok').textContent=ok||'Đồng ý'", "o.querySelector('.ok').textContent=ok||'OK'"),
    # bài dở
    ("?'hôm nay '+hm:", "?'today '+hm:"),
    ("`Đã làm ${dgDone(x)}/${x.n} câu${sn?' · đang ở phần '+sn:''}${x.pr?'':' · còn '+fmt(x.left).replace(/^00:/,'')} · lưu lúc ${dgWhen(x.t)}`",
     "`${dgDone(x)}/${x.n} answered${sn?' · section: '+sn:''}${x.pr?'':' · '+fmt(x.left).replace(/^00:/,'')+' left'} · saved ${dgWhen(x.t)}`"),
    ("`<div>Em đang làm dở <b>${esc(EXAMS[i].title)}</b> · ${x.pr?'Luyện tập':'Thi thử'} (${dgDone(x)}/${x.n} câu). Làm tiếp nhé?</div><button class=\"go\" type=\"button\">Làm tiếp</button><button class=\"no\" type=\"button\">Để sau</button>`",
     "`<div>You have an unfinished test: <b>${esc(EXAMS[i].title)}</b> · ${x.pr?'Practice':'Timed test'} (${dgDone(x)}/${x.n} answered). Continue?</div><button class=\"go\" type=\"button\">Continue</button><button class=\"no\" type=\"button\">Later</button>`"),
    ('`<span class="tdb op">▶ Đang làm dở · ${dgDone(d)}/${d.n} câu</span>`', '`<span class="tdb op">▶ In progress · ${dgDone(d)}/${d.n} answered</span>`'),
    ('`<span class="tdb ok">✓ Đã làm ${x.n} lần · cao nhất ${x.b}%</span>`:`<span class="tdb op">Đã mở · chưa nộp bài</span>`',
     '`<span class="tdb ok">✓ Taken ${x.n}× · best ${x.b}%</span>`:`<span class="tdb op">Opened · not submitted</span>`'),
    ("const SEC_VI={'文字と語彙':'Chữ & Từ vựng','会話と表現':'Hội thoại & Diễn đạt','聴解':'Nghe hiểu','読解':'Đọc hiểu'};",
     "const SEC_VI={'文字と語彙':'Vocabulary','会話と表現':'Conversation','聴解':'Listening','読解':'Reading'};"),
    ("if(c)c.textContent=ACCOUNT.user", "if(c)c.textContent='Guest'"),
    ("h=h.replace(/\\(([^()<>]{2,40})\\)/g,(m,a)=>/^[A-ZĐÀ-Ỹ][A-ZĐÀ-Ỹ –-]+$/.test(a)&&a===a.toUpperCase()&&a!==a.toLowerCase()?`<span class=\"xhv\">${a}</span>`:m);", ""),
    # kết quả
    ('title="Câu ${n+1}"', 'title="Question ${n+1}"'),
    ('<div class="muted">Kết quả · ${esc(S.title)}</div>', '<div class="muted">Results · ${esc(S.title)}</div>'),
    ("/ ${ptot} điểm · ${ok}/${tot} câu đúng · ${pts>=200?'<b style=\"color:var(--ok)\">ĐẠT (≥200)</b>':'<b style=\"color:var(--ng)\">CHƯA ĐẠT (cần 200)</b>'}",
     "/ ${ptot} points · ${ok}/${tot} correct · ${pts>=200?'<b style=\"color:var(--ok)\">PASS (≥200)</b>':'<b style=\"color:var(--ng)\">NOT YET (200 needed)</b>'}"),
    ('<span class="muted">câu đúng · ${pct}%</span>', '<span class="muted">correct · ${pct}%</span>'),
    ('${na} câu chưa có đáp án nên không tính điểm.', '${na} question(s) have no answer key and are not scored.'),
    ('<div class="h2" style="margin-top:16px">Xem lại từng câu</div>', '<div class="h2" style="margin-top:16px">Review each question</div>'),
    ('id="resRv" type="button">Xem đáp án &amp; giải thích</button>', 'id="resRv" type="button">Answers &amp; explanations</button>'),
    ('id="resClose" type="button">Đóng</button>', 'id="resClose" type="button">Close</button>'),
    ('<footer>© 2026 Anh Trọng Dạy JFT</footer>\n</section>\n<div class="exmode"', '<footer>© 2026 Anh Trọng Dạy JFT · Japanese text: いろどり 生活の日本語 (The Japan Foundation) · Illustrations: いらすとや</footer>\n</section>\n<div class="exmode"'),
]
EN_CSS = '''<style>
/* bản tiếng Anh: chỉ có Làm đề */
.side .nav:not([data-go="exam"]),.side .grow~*,#aiFab,#aiBox,#penFab,#penBar,#soP,#dSach{display:none!important}
@media(max-width:900px){.side{display:none!important}}
</style>'''

def run(s, D, P, FB, TT, PANEL, AD_HTML, DHV_HTML, E_demo, strict=False):
    s0 = s
    for a, b in UI:
        assert a in s, 'EN: không thấy ' + a[:90]
        s = s.replace(a, b)
    PANEL_EN = (f'<div class="ic">🔒</div><b>Available in the full course</b><p>This free trial includes <b>6 complete tests</b> with answers and explanations. '
                'The full course unlocks every mock test and listening test. Message the teacher to join.</p>'
                f'<div class="cta"><a href="{FB}" target="_blank" rel="noopener">💬 Message on Facebook</a><a class="tt" href="{TT}" target="_blank" rel="noopener">♪ TikTok @anhtrong.daygino</a></div>')
    assert PANEL in s; s = s.replace(PANEL, PANEL_EN).replace('aria-label="Đóng">×</button>', 'aria-label="Close">×</button>')
    AD_EN = (f'<div id="dAd" class="dad"><div class="dadt"><small>Full JFT-Basic test pack</small><b>Get every mock test for <em>¥5,000</em></b>'
             '<span>28 mock tests + 4 listening tests · 1,800+ questions with answers and explanations</span></div>'
             f'<a href="{FB}" target="_blank" rel="noopener">💬 Message to buy</a></div>')
    for a, b in ((json.dumps(AD_HTML, ensure_ascii=False), json.dumps(AD_EN, ensure_ascii=False)), (json.dumps(DHV_HTML, ensure_ascii=False), '""')):
        assert a in s; s = s.replace(a, b)
    s = re.sub(r'<div class="dct">.*?</div>', f'<div class="dct"><b>Questions? Contact the teacher</b><a class="fb" href="{FB}" target="_blank" rel="noopener">Facebook</a><a class="tt" href="{TT}" target="_blank" rel="noopener">TikTok @anhtrong.daygino</a></div>', s, count=1, flags=re.S)
    s = re.sub(r'<title>[^<]*</title>', '<title>JFT-Basic Mock Tests · Free Trial · Anh Trọng</title>', s, count=1)
    s = s.replace('</head>', EN_CSS + '</head>', 1)
    # dữ liệu đề tiếng Anh
    full = X.load(); out = []; report = []
    for eid in X.OPEN:
        e, miss, left = tr_exam(full[eid], strict); out.append(e); report.append((eid, len(miss), len(left)))
    keep = [x for x in E_demo[len(X.OPEN):] if re.match(r'Đề (nghe )?\d+$', x['title']) or x['id'] == 'jft-kaiwa']
    out += [en_locked(x) for x in keep]
    js = 'window.EXAMS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';window.EXTLINKS=[];'
    open(D + 'app/data/exams_en.js', 'w', encoding='utf-8').write(js)
    v = hashlib.md5(js.encode()).hexdigest()[:8]
    s, n = re.subn(r'app/data/exams\.js(\?v=[0-9a-f]+)?', f'app/data/exams_en.js?v={v}', s); assert n == 1
    open(D + 'en.html', 'w', encoding='utf-8').write(s)
    print('EN:', report, '· khoá', len(keep), 'đề')
    return report
