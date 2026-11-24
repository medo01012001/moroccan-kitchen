# Split a long TTS wav into one clip per sentence.
# Picks cut points among silences with dynamic programming: long silences are preferred,
# and each clip's length should match its sentence's text length.
# usage: python split.py raw.wav castIndex
import sys, wave, os, subprocess, math
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from cast import CAST, DISHES, lines

src, ci = sys.argv[1], int(sys.argv[2])
c = CAST[ci]; cid = c[0]
texts = lines(c)
names = ['thanks', 'wrong', 'angry'] + [d for d, _ in DISHES]
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
hi = int(sys.argv[4]) if len(sys.argv) > 4 else len(names)
texts, names = texts[lo:hi], names[lo:hi]
N = len(names)

with wave.open(src, 'rb') as w:
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

hop = int(sr * 0.01)
F = len(x) // hop
db = 20 * np.log10(np.sqrt(np.mean(x[:F * hop].reshape(F, hop) ** 2, axis=1) + 1e-12))
silent = db < -40
voiced = np.where(~silent)[0]
S, E = voiced[0], voiced[-1] + 1

gaps, i = [], S
while i < E:
    if silent[i]:
        j = i
        while j < E and silent[j]: j += 1
        if j - i >= 15: gaps.append((i, j))     # >=150 ms
        i = j
    else: i += 1
M = len(gaps)
if M < N - 1: sys.exit(f'only {M} gaps')
if N == 1: gaps = []

# expected speech length per sentence from character counts
chars = np.array([len(t.replace(' ', '')) + 3 for t in texts], float)
gap_total_guess = 0  # speech only
speech_total = (E - S) - sum(b - a for a, b in gaps) * 0.6
exp = chars / chars.sum() * speech_total

def seg_cost(k, a, b):
    d = max(1, b - a)
    # remove internal silence from duration estimate
    return 6 * math.log(d / exp[k] / 1.25) ** 2

INF = 1e18
# dp[k][j]: best cost with first k+1 segments placed, k-th cut at gap j
starts = [g[1] for g in gaps]; ends = [g[0] for g in gaps]
glen = [ (g[1] - g[0]) / 100 for g in gaps ]
dp = np.full((max(1, N - 1), max(1, M)), INF); back = np.zeros((N - 1, M), int)
for j in range(M if N > 1 else 0):
    dp[0][j] = seg_cost(0, S, ends[j]) - 4 * min(glen[j], 1.5)
for k in range(1, N - 1):
    for j in range(k, M):
        best, arg = INF, -1
        for p in range(k - 1, j):
            if dp[k - 1][p] >= INF: continue
            v = dp[k - 1][p] + seg_cost(k, starts[p], ends[j])
            if v < best: best, arg = v, p
        dp[k][j] = best - 4 * min(glen[j], 1.5); back[k][j] = arg
if N == 1:
    cuts = []
else:
  tot = [dp[N - 2][j] + seg_cost(N - 1, starts[j], E) for j in range(M)]
  j = int(np.argmin(tot)); cuts = []
  for k in range(N - 2, -1, -1):
      cuts.append(j); j = back[k][j]
  cuts = cuts[::-1]

bounds = [S] + [v for jj in cuts for v in (ends[jj], starts[jj])] + [E]
out_dir = os.path.join(os.path.dirname(__file__), cid)
os.makedirs(out_dir, exist_ok=True)
report = []
for k in range(N):
    a, b = bounds[2 * k], bounds[2 * k + 1]
    a = max(0, a - 6); b = min(F, b + 10)
    seg = x[a * hop:b * hop]
    tmp = os.path.join(out_dir, names[k] + '.wav')
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-ac', '1', '-b:a', '48k', tmp[:-4] + '.mp3'], check=True)
    os.remove(tmp)
    report.append(f'{len(seg)/sr:.1f}/{exp[k]/100:.1f}')
print('cut gaps(ms):', min([glen[j] for j in cuts] or [0]) * 1000, '| clip/expected:', ' '.join(report))
