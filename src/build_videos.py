#!/usr/bin/env python3
"""src/raw/videos.json -> public/app/data/videos.js (tab Video bài giảng).
Thêm video: thêm 1 dòng vào videos.json (yt = mã video YouTube, docs = link tài liệu), chạy lại file này."""
import json, os, re
A = os.path.dirname(os.path.abspath(__file__)) + '/'
V = json.load(open(A + 'raw/videos.json', encoding='utf-8'))
for v in V:
    v['yt'] = v.get('yt') or ''   # để trống = video sắp có (vẫn hiện slide / tài liệu)
    m = re.search(r'(?:youtu\.be/|v=|embed/|shorts/)([\w-]{11})', v['yt'])
    if m: v['yt'] = m.group(1)
    assert v['yt'] == '' or re.fullmatch(r'[\w-]{11}', v['yt']), v
open(A + '../public/app/data/videos.js', 'w', encoding='utf-8').write('window.VIDEOS=' + json.dumps(V, ensure_ascii=False, separators=(',', ':')) + ';')
print('videos', len(V))
