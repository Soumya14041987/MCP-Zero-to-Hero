"""Step 5: 1000 agent sessions, each with a different history length.
Paged KV cache vs one big slab per session (simulation, not vLLM itself)."""
import numpy as np

MAX_LEN, BLOCK = 4096, 16
lens = np.random.default_rng(7).integers(50, 1200, size=1000)   # tokens each request really used

slab = len(lens) * MAX_LEN                                       # reserve max length for everyone
paged = sum(-(-n // BLOCK) * BLOCK for n in lens)                # round up to whole blocks
used = int(lens.sum())
print(f"tokens actually used : {used}")
print(f"slab reserved        : {slab}  -> {100*(slab-used)/slab:.1f}% wasted")
print(f"paged reserved       : {paged}  -> {100*(paged-used)/paged:.1f}% wasted")
print(f"same GPU memory fits {slab/paged:.1f}x more concurrent requests with paging")
