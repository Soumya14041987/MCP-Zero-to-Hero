"""Step 6: speculative decoding. An agent's tool-call JSON is very predictable, so a cheap
draft model is often right. The target model still decides (toy distribution check)."""
import numpy as np

rng = np.random.default_rng(3)
p = np.array([0.55, 0.25, 0.15, 0.05])      # target model: next-token probabilities
q = np.array([0.40, 0.40, 0.10, 0.10])      # cheap draft model

def speculative_sample():
    x = rng.choice(4, p=q)                          # draft proposes
    if rng.random() < min(1.0, p[x] / q[x]):        # target accepts with min(1, p/q)
        return x, True
    resid = np.maximum(p - q, 0); resid /= resid.sum()
    return rng.choice(4, p=resid), False            # on reject: sample the residual

out = [speculative_sample() for _ in range(200_000)]
emp = np.bincount([t for t, _ in out], minlength=4) / len(out)
print("target   :", p)
print("spec out :", emp.round(3))
print(f"draft tokens accepted: {np.mean([a for _, a in out]):.1%}")
