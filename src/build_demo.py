#!/usr/bin/env python3
# Dựng bản DÙNG THỬ (không đăng nhập): mỗi phần chỉ 2 mục → ../demo/public
import os, json, shutil
A = os.path.dirname(os.path.abspath(__file__)) + '/'
P = A + '../public/'; D = A + '../demo/public/'
if os.path.exists(D): shutil.rmtree(D)
os.makedirs(D + 'app/data'); os.makedirs(D + 'lessons/s1')
def load(f):
    s = open(P + 'app/data/' + f, encoding='utf-8').read()
    return s[s.index('=') + 1:s.index(';window.EXTLINKS') if 'EXTLINKS' in s else s.rindex(';')]
def save(f, var, obj, extra=''):
    open(D + 'app/data/' + f, 'w', encoding='utf-8').write(f'window.{var}=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';' + extra)
L = [l for l in json.loads(load('lessons.js')) if l['lv'] == 's1' and l['bai'] in (1, 2)]
save('lessons.js', 'LESSONS', L)
for l in L:
    for k in ('web', 'slide'): shutil.copy(P + l[k], D + l[k])
save('exams.js', 'EXAMS', json.loads(load('exams.js'))[:2], 'window.EXTLINKS=[];')
G = [g for g in json.loads(load('grammar.js')) if g['lv'] == '初級1' and g['bai'] in (1, 2)]
save('grammar.js', 'GRAMMAR', G)
S = [q for q in json.loads(load('skills.js')) if q['lv'] == 's1' and q['bai'] in (2, 3)]
save('skills.js', 'SKILLS', S)
W = []
for w in json.loads(load('vocab.js'))['words']:
    l = [x for x in w['l'] if x[0] == '初級1' and x[1] in (1, 2)]
    if l: W.append({**w, 'l': l})
save('vocab.js', 'VOCAB', {'words': W, 'ex': json.loads(load('vocab.js')).get('ex', [])})
save('videos.js', 'VIDEOS', [{**v, 'docs': []} for v in json.loads(load('videos.js'))[:1]])
DD = json.loads(load('docs.js'))
save('docs.js', 'DOCS', dict(vocab={k: [w for w in v if w['b'] in (sorted({x['b'] for x in v})[:2])] if k == '入門' else [] for k, v in DD['vocab'].items()},
     kanji={k: (v[:20] if k == '入門' else []) for k, v in DD['kanji'].items()}, gram={k: (v[:2] if k == '入門' else []) for k, v in DD['gram'].items()}))
H = json.loads(load('hw.js'))[:2]
save('hw.js', 'HW', H)
os.makedirs(D + 'btvn/pdf', exist_ok=True)
for h in H:
    shutil.copy(P + h['html'], D + h['html']); shutil.copy(P + h['pdf'], D + h['pdf'])
os.makedirs(D + 'app/media/vau', exist_ok=True)
for w in W:
    if w.get('au') and os.path.exists(P + f"app/media/vau/{w['au']}.mp3"): shutil.copy(P + f"app/media/vau/{w['au']}.mp3", D + f"app/media/vau/{w['au']}.mp3")
# media chỉ những file dùng trong dữ liệu thử
blob = ''.join(open(D + 'app/data/' + f, encoding='utf-8').read() for f in os.listdir(D + 'app/data'))
n = 0
for root, _, fs in os.walk(P + 'app/media'):
    for f in fs:
        rel = os.path.relpath(os.path.join(root, f), P)
        if rel in blob or f in blob or ('gimg' in rel and '"'+os.path.splitext(f)[0]+'"' in blob):
            os.makedirs(os.path.dirname(D + rel), exist_ok=True); shutil.copy(P + rel, D + rel); n += 1
s = open(P + 'index.html', encoding='utf-8').read()
reps = [("$('#logout').onclick=()=>{location.href='/logout'};", "$('#logout').style.display='none';"),
        ('<main>', '<main><div style="background:#fff3b0;border:1px solid #f1c48b;color:#5a4300;border-radius:12px;padding:10px 14px;margin:0 0 14px;font-size:14px"><b>BẢN DÙNG THỬ</b> · Mỗi phần mở 2 mục (2 bài học, 2 đề, 2 bài ngữ pháp, 1 video bài giảng, tài liệu Nhập môn mẫu, từ vựng 2 bài, 2 buổi bài tập về nhà). Liên hệ <b>Anh Trọng Dạy JFT</b> để học bản đầy đủ: 42 bài, 11 đề có giải thích, video bài giảng, 3.800+ từ.</div>'),
        ('<title>', '<title>Dùng thử · ')]
for a, b in reps:
    assert s.count(a) >= 1, a; s = s.replace(a, b, 1)
open(D + 'index.html', 'w', encoding='utf-8').write(s)
print('demo:', len(L), 'bài', 2, 'đề', len(G), 'ngữ pháp', len(S), 'câu kỹ năng', len(W), 'từ', n, 'media')
