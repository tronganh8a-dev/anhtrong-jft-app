T=open('/home/claude/anhtrong-jft-app/public/tailieu/Buoi10_KinhNgu.html').read()
import re
HEAD=T[:T.index('</style>')]+'''
.kg{display:grid;gap:26px;flex:1;align-content:center}.kg.c2{grid-template-columns:repeat(2,1fr)}.kg.c3{grid-template-columns:repeat(3,1fr)}.kg.c4{grid-template-columns:repeat(4,1fr)}.kg.c5{grid-template-columns:repeat(5,1fr)}
.kc{background:#fff;border-radius:22px;padding:22px 20px 18px;box-shadow:0 8px 24px #0d2b4012;text-align:center;border-top:8px solid #0d5a8c}.kc:nth-child(2){border-color:#c42f66}.kc:nth-child(3){border-color:#f2a93b}.kc:nth-child(4){border-color:#5a9e2f}.kc:nth-child(5){border-color:#7a4fb5}
.kc .k{font-family:"Klee One",serif;font-size:150px;line-height:1.05;color:#0d2b40}.kc .hv{font-size:30px;font-weight:700;color:#c42f66;letter-spacing:1px}.kc .rd{font-size:28px;margin-top:4px}.kc .mn{font-size:24px;color:#47647a;margin-top:2px}.kc .vd{font-size:28px;margin-top:12px;background:#f6f8fb;border-radius:12px;padding:8px}.kc .vd rt{font-size:.45em}
.pb{margin-top:22px;background:#fff8e6;border-left:8px solid #f2a93b;border-radius:14px;padding:16px 26px;font-size:27px;line-height:1.55}.pb b{color:#c42f66}.pb .jp{font-size:30px}
.src{font-size:22px;color:#6b8296;margin-left:12px;font-weight:600}.q u{text-decoration:none;border-bottom:4px solid #c42f66}
.st{visibility:hidden;opacity:0;transform:translateY(8px);transition:opacity .35s,transform .35s}.st.sh{visibility:visible;opacity:1;transform:none}.kc{cursor:pointer}
#ann{position:fixed;inset:0;z-index:8;pointer-events:none}.ntx,.nmm{position:absolute;pointer-events:auto;outline:none;font-family:"Klee One","M PLUS Rounded 1c",Quicksand,sans-serif;font-weight:600}
.ntx{color:#e0245e;font-size:34px;min-width:20px;padding:2px 6px;border:2px dashed transparent}.ntx:focus{border-color:#e0245e88}
.nmm{background:#fff3a6;color:#0d2b40;font-size:26px;min-width:180px;min-height:70px;padding:14px 16px 12px;border-radius:6px;box-shadow:0 8px 20px #0d2b4040;transform:rotate(-1.5deg)}.nmm .gr{position:absolute;left:0;right:0;top:0;height:12px;cursor:move;background:#f2d95c;border-radius:6px 6px 0 0}.nmm .tx{outline:none;min-height:40px}.nmm .xx{position:absolute;right:4px;top:-2px;font-size:16px;cursor:pointer;color:#8a6d1a}
body.m-text #pen,body.m-memo #pen{pointer-events:auto;cursor:text}body.m-memo #pen{cursor:copy}
#bar button.on{background:#c42f66}#bar button{white-space:nowrap}
.sum{width:100%;border-collapse:collapse;font-size:26px}.sum td{padding:9px 16px;border-bottom:1px solid #dbe4ec}.sum td.k{font-family:"Klee One",serif;font-size:38px;white-space:nowrap}.sum tr:nth-child(odd) td{background:#fff}
</style></head><body><div id="stage">'''
LOGO=re.search(r'<img class="lg" src="([^"]+)"',T).group(1)
