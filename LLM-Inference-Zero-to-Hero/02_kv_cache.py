"""Step 2: the KV cache. Same answer, far less work."""
import time, numpy as np
from toy_model import make_weights, forward

W = make_weights()
prompt, N = [i % 100 for i in range(200)], 100   # 200-token prompt, 100 new tokens

def run(use_cache):
    toks, cache, done, t0 = list(prompt), ({} if use_cache else None), 0, time.perf_counter()
    for step in range(N):
        feed = toks if (not use_cache or step == 0) else toks[-1:]   # prefill once, then 1 token
        logits = forward(W, np.array(feed), cache)
        done += len(feed)
        toks.append(int(np.argmax(logits)))
    return toks, done, time.perf_counter() - t0

a, work_a, t_a = run(False)
b, work_b, t_b = run(True)
print("identical output:", a == b)
print(f"no cache : {work_a:6d} token-passes, {t_a:.2f}s")
print(f"KV cache : {work_b:6d} token-passes, {t_b:.2f}s")
