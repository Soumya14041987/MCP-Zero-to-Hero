"""Tiny decoder-only transformer in NumPy (random weights). Shared by the demos.
It is a TOY: it shows the mechanics of inference, not real model quality."""
import numpy as np

D, H, VOCAB, LAYERS = 64, 4, 100, 2
HD = D // H

def make_weights(seed=0):
    r = np.random.default_rng(seed)
    w = lambda *s: (r.standard_normal(s) / np.sqrt(s[0])).astype(np.float32)
    return {"emb": w(VOCAB, D), "out": w(D, VOCAB),
            "layers": [{k: w(D, D) for k in ("q", "k", "v", "o")} | {"up": w(D, 4 * D), "down": w(4 * D, D)}
                       for _ in range(LAYERS)]}

def softmax(x):
    e = np.exp(x - x.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)

def attend(q, K, V):
    """q: (t,D) new queries; K,V: (T,D) all keys/values so far. Causal over the last t rows."""
    t, T = q.shape[0], K.shape[0]
    qh = q.reshape(t, H, HD).transpose(1, 0, 2)
    Kh = K.reshape(T, H, HD).transpose(1, 0, 2)
    Vh = V.reshape(T, H, HD).transpose(1, 0, 2)
    s = qh @ Kh.transpose(0, 2, 1) / np.sqrt(HD)
    mask = np.arange(T)[None, :] > (np.arange(t)[:, None] + T - t)
    s = np.where(mask[None], -1e9, s)
    return (softmax(s) @ Vh).transpose(1, 0, 2).reshape(t, D)

def forward(W, tokens, cache=None):
    """Run `tokens` through the model. With a cache, only the new tokens are computed."""
    x = W["emb"][tokens]
    for i, L in enumerate(W["layers"]):
        q, k, v = x @ L["q"], x @ L["k"], x @ L["v"]
        if cache is not None:
            ck, cv = cache.get(i, (np.zeros((0, D), np.float32),) * 2)
            k, v = np.vstack([ck, k]), np.vstack([cv, v])
            cache[i] = (k, v)
        x = x + attend(q, k, v) @ L["o"]
        x = x + np.maximum(x @ L["up"], 0) @ L["down"]
    return x[-1] @ W["out"]          # logits for the next token
