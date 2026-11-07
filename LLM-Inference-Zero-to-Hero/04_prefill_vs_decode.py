"""Step 4: why decode is slow. Measure one weight matrix serving 1 vs many tokens."""
import time, numpy as np

d = 4096
Wt = np.random.default_rng(0).standard_normal((d, d)).astype(np.float32)   # 64 MiB of weights

def secs(rows, reps=20):
    x = np.random.default_rng(1).standard_normal((rows, d)).astype(np.float32)
    x @ Wt                                                                   # warm up
    t = time.perf_counter()
    for _ in range(reps):
        x @ Wt
    return (time.perf_counter() - t) / reps

base = secs(1)
print("rows(tokens)  ms/call  ms per token  FLOPs per weight byte")
for rows in (1, 8, 64, 512):
    s = secs(rows)
    print(f"{rows:>11} {s*1e3:8.2f} {s/rows*1e3:12.4f} {2*rows*d*d/(d*d*4):12.1f}")
print(f"1 token costs {base*1e3:.2f} ms; the weights are read once per call either way.")
