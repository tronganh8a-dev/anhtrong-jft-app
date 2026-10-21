#!/usr/bin/env python3
# Dựng lại public/index.html từ index_tpl.html (bản online: đăng nhập do máy chủ lo)
import os
A=os.path.dirname(os.path.abspath(__file__))+'/'
t=open(A+'index_tpl.html',encoding='utf-8').read()
t=t.replace("""+'</div>').join('')}
$('#examList')""","""+'</div>').join('')}
$('#examList')""")
t=t.replace('__USER__','hocvien').replace('__HASH__','')
s=t
reps=[("const ACCOUNT={user:'","const ACCOUNT={user:decodeURIComponent((document.cookie.match(/(?:^|; )jft_user=([^;]*)/)||[0,''])[1])||'"),
("if(store.get('atjft_ok')===ACCOUNT.hash)unlock();","unlock();"),
("$('#logout').onclick=()=>{store.del('atjft_ok');location.reload()};","$('#logout').onclick=()=>{location.href='/logout'};"),
("thư mục <b>APP HỌC JFT</b> phải nằm trong <b>WEB HỌC JFT</b>, cạnh thư mục <b>HỌC </b>","anh/chị tải lại trang hoặc đăng nhập lại")]
for a,b in reps:
    assert a in s,a; s=s.replace(a,b)
s=s.replace('<body class="locked">','<body>')
open(A+'../public/index.html','w',encoding='utf-8').write(s)
print('ok index')
