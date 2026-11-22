"""Ghép video ngữ pháp: mỗi slide 1 file (ảnh đứng yên đúng thời lượng lời đọc ước tính), mỗi lần lật trang 1 file,
nối bằng concat (-c copy), thêm tiếng lật trang (-c:v copy). Ra: <D>/NguPhapJFT_10phut.mp4 + <D>/script.txt (có mốc giờ).
Thời lượng: tham số --dur dur.json (danh sách giây, khi đã có giọng thật) — nếu không có thì ước tính theo số chữ."""
import json, re, os, subprocess, sys, wave
import numpy as np
D = '/tmp/ngp'
FPS, TR = 30, 0.6
S = json.load(open(f'{D}/script.json'))
N = len(S)
if '--dur' in sys.argv:
    DUR = json.load(open(sys.argv[sys.argv.index('--dur') + 1]))
else:
    def est(t):
        vn = len(re.findall(r'[A-Za-zÀ-ỹđĐ]+', t)); jp = len(re.findall(r'[぀-ヿ一-鿿]', t))
        return round(vn / 3.1 + jp / 6 + 1.5, 2)
    DUR = [est(x['say']) for x in S]
    DUR[-1] += 1.5
ENC = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-g', '60', '-an']

def run(cmd, out):
    tmp = out[:-4] + '.part.mp4'
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + cmd + [tmp])
    if r.returncode: raise SystemExit('lỗi ffmpeg: ' + out)
    os.replace(tmp, out)

os.makedirs(f'{D}/seg', exist_ok=True)
jobs = []
for i in range(N):
    out = f'{D}/seg/s{i + 1:02d}.mp4'
    jobs.append((['-framerate', str(FPS), '-i', f'{D}/png/s{i + 1}.png',
                  '-vf', f'format=yuv420p,loop=-1:1,trim=duration={DUR[i]}'] + ENC, out))
    if i < N - 1:
        jobs.append((['-framerate', str(FPS), '-i', f'{D}/tr/{i + 1:02d}/f%02d.jpg', '-vf', 'format=yuv420p'] + ENC,
                     f'{D}/seg/t{i + 1:02d}.mp4'))
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(2) as ex:
    list(ex.map(lambda j: run(*j), jobs))
order = []
for i in range(N):
    order.append(f'{D}/seg/s{i + 1:02d}.mp4')
    if i < N - 1: order.append(f'{D}/seg/t{i + 1:02d}.mp4')
open(f'{D}/seg/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in order))
run(['-f', 'concat', '-safe', '0', '-i', f'{D}/seg/list.txt', '-c', 'copy'], f'{D}/v_noaudio.mp4')

# tiếng lật trang (tự tổng hợp: tiếng giấy sột soạt + tiếng phạch khi trang nằm xuống)
SR = 44100
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for k in range(len(x)): s = (1 - a) * x[k] + a * s; y[k] = s
    return y
rng = np.random.default_rng(7)
n = int(.5 * SR); t = np.arange(n) / SR
w = rng.standard_normal(n)
band = lp(w, 5200) - lp(w, 700)
env = np.clip(t / .09, 0, 1) * np.exp(-np.clip(t - .09, 0, None) / .11)
flut = 1 + .55 * lp(rng.standard_normal(n), 35) / .05
swish = band * env * np.clip(flut, .2, 2)
th = lp(rng.standard_normal(n), 260) * np.exp(-np.clip(t - .33, 0, None) / .03) * (t > .33)
flip = swish / np.abs(swish).max() * .5 + th / (np.abs(th).max() + 1e-9) * .35
flip *= 10 ** (-13 / 20) / np.abs(flip).max()
total = sum(DUR) + TR * (N - 1)
aud = np.zeros(int((total + .5) * SR))
starts, tt = [], 0.0
for i in range(N):
    starts.append(tt); tt += DUR[i]
    if i < N - 1:
        k = int((tt - .02) * SR); aud[k:k + n] += flip[:len(aud) - k]
        tt += TR
pcm = (np.clip(aud, -1, 1) * 32767).astype('<i2')
with wave.open(f'{D}/sfx.wav', 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
run(['-i', f'{D}/v_noaudio.mp4', '-i', f'{D}/sfx.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
     '-ar', '48000', '-ac', '2', '-shortest', '-movflags', '+faststart'], f'{D}/NguPhapJFT_10phut.mp4')

G = ['Trợ từ', 'Danh từ · Tính từ', 'Các thể động từ', 'Nhờ vả · Xin phép · Cấm', 'Mong muốn · Rủ rê · Khuyên',
     'Sở thích · Kinh nghiệm · Khả năng', 'Trạng thái · Thay đổi', 'Thời gian · Trình tự', 'Lý do · Điều kiện',
     'So sánh · Mức độ', 'Phỏng đoán · Nghe nói', 'Cho · Nhận']
ts = lambda x: f'{int(x // 60):02d}:{int(x % 60):02d}'
lines = []
for i, x in enumerate(S):
    name = {'title': 'Mở đầu', 'map': '12 nhóm', 'outro': 'Kết'}.get(x['kind']) or f"Nhóm {x['g']} · {G[x['g'] - 1]}"
    lines.append(f"[{ts(starts[i])}] Slide {i + 1} – {name}\n{x['say']}\n")
open(f'{D}/script.txt', 'w').write('\n'.join(lines))
json.dump({'dur': DUR, 'start': starts}, open(f'{D}/timing.json', 'w'))
print('ok', round(total, 1), 'giây')
