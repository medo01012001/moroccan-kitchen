# Sanity check: every dish clip should start with the same opener phrase, exactly once.
# usage: python check.py charId
import sys, os, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from cast import DISHES

cid = sys.argv[1]; d = os.path.join(os.path.dirname(__file__), cid)
def load(n):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(d, n + '.mp3'), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def spec(x):
    n, h = 512, 160
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::h] * np.hanning(n)
    s = np.log(np.abs(np.fft.rfft(fr))[:, 4:120] + 1e-4)
    s -= s.mean(1, keepdims=True)
    return s / (np.linalg.norm(s, axis=1, keepdims=True) + 1e-9)
specs = {n: spec(load(n)) for n, _ in DISHES if os.path.exists(os.path.join(d, n + '.mp3'))}
# template = opener region of the median-length clip, first 0.9 s
tmpl = specs['bissara'][:90]
def score_at(s, off):
    m = s[off:off + len(tmpl)]
    if len(m) < len(tmpl): return -1
    return float(np.mean(np.sum(m * tmpl, axis=1)))
for n in specs:
    s = specs[n]
    start = max(score_at(s, o) for o in range(0, 25))
    later = max([score_at(s, o) for o in range(110, max(111, len(s) - 60))] or [-1])
    flag = '  <-- ?' if start < 0.45 or later > 0.55 else ''
    print(f'{n:12s} start={start:.2f} later={later:.2f} len={len(s)/100:.1f}s{flag}')
