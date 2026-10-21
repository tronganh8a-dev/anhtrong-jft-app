import re,sys,base64,subprocess,hashlib,os
from concurrent.futures import ThreadPoolExecutor
src,dst=sys.argv[1],sys.argv[2]
s=open(src,'rb').read()
pat=re.compile(rb'data:audio/mpeg;base64,([A-Za-z0-9+/=]+)')
blobs={m.group(1) for m in pat.finditer(s)}
def conv(b):
    raw=base64.b64decode(b)
    if len(raw)<20000: return b,b
    p=subprocess.run(['ffmpeg','-v','error','-i','pipe:0','-ac','1','-ar','24000','-b:a','48k','-f','mp3','pipe:1'],input=raw,capture_output=True)
    if p.returncode or len(p.stdout)>=len(raw): return b,b
    return b,base64.b64encode(p.stdout)
with ThreadPoolExecutor(8) as ex: M=dict(ex.map(conv,blobs))
out=pat.sub(lambda m:b'data:audio/mpeg;base64,'+M[m.group(1)],s)
open(dst,'wb').write(out)
print(os.path.basename(src),len(s)//1000000,'->',len(out)//1000000,'MB',len(blobs))
