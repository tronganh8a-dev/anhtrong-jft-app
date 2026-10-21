import json,re,hashlib,os,subprocess,io,wave,sys
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
R='/tmp/claude-0/-home-claude/53ce519d-fd2a-5897-9a15-9190297c3a0e/scratchpad/web/repo/'
OUT=R+'public/app/media/vau/'; os.makedirs(OUT,exist_ok=True)
s=open(R+'public/app/data/vocab.js',encoding='utf-8').read();D=json.loads(s[s.index('=')+1:s.rindex(';')])
ort=Onnxruntime.load_once(filename='voicevox_onnxruntime-linux-x64-1.23.2/lib/libvoicevox_onnxruntime.so.1.23.2')
syn=Synthesizer(ort,OpenJtalk('open_jtalk_dic_utf_8-1.11'),cpu_num_threads=2)
m=VoiceModelFile.open('15.vvm'); syn.load_voice_model(m); SID=13
def clean(x):
    x=re.sub(r'[（(][^）)]*[）)]','',x); x=re.sub(r'[～〜\s　]','',x)
    return re.split(r'[／/]',x)[0]
def h2k(t): return ''.join(chr(ord(c)+0x60) if 'ぁ'<=c<='ゖ' else c for c in t)
def nmora(y): return len(re.sub(r'[ゃゅょぁぃぅぇぉャュョァィゥェォ]','',y))
stat={'ok':0,'kana':0,'acc':0,'skip':0}
for i,w in enumerate(D['words']):
    h,y=clean(w['h']),clean(w['y'])
    if not h or not y: stat['skip']+=1; continue
    key=hashlib.md5((w['h']+'|'+w['y']).encode()).hexdigest()[:12]
    fn=OUT+key+'.mp3'
    w['au']=key
    if os.path.exists(fn): continue
    try:
        q=syn.create_audio_query(h,SID)
        qk=''.join(mo.text for ap in q.accent_phrases for mo in ap.moras)
        if qk.replace('ー','')!=h2k(y).replace('ー','') and qk!=h2k(y):
            q=syn.create_audio_query(y,SID); stat['kana']+=1
        a=w.get('a')
        if a not in (None,'') and len(q.accent_phrases)==1:
            n=int(str(a).split(',')[0]); L=len(q.accent_phrases[0].moras)
            if n<=L: q.accent_phrases[0].accent = L if n==0 else n; stat['acc']+=1
        q.speed_scale=0.95; q.pre_phoneme_length=0.08; q.post_phoneme_length=0.12; q.output_sampling_rate=24000
        wav=syn.synthesis(q,SID)
        p=subprocess.run(['ffmpeg','-v','error','-y','-i','pipe:0','-ac','1','-b:a','40k','-f','mp3',fn],input=wav)
        stat['ok']+=1
    except Exception as e:
        stat['skip']+=1; w.pop('au',None); print('ERR',w['h'],e,file=sys.stderr)
    if i%200==0: print(i,stat,flush=True)
open(R+'public/app/data/vocab.js','w',encoding='utf-8').write('window.VOCAB='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';')
print('done',stat)
