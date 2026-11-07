"""Step 3: what the KV cache costs in memory.
bytes/token = 2 (K and V) x layers x kv_heads x head_dim x bytes_per_value"""

def kv_bytes_per_token(layers, kv_heads, head_dim, dtype_bytes=2):
    return 2 * layers * kv_heads * head_dim * dtype_bytes

# Llama-3-8B-style shape: 32 layers, 8 KV heads (GQA), head_dim 128, fp16.
# VERIFY against the model's config.json before publishing.
gqa = kv_bytes_per_token(32, 8, 128)
mha = kv_bytes_per_token(32, 32, 128)      # same model if every query head had its own K/V
print(f"GQA : {gqa/1024:.0f} KiB per token   MHA: {mha/1024:.0f} KiB per token")
print("agent context  concurrent agents  GQA GiB   MHA GiB")
for ctx, batch in [(8192, 1), (8192, 16), (32768, 16), (131072, 4)]:
    g = gqa * ctx * batch / 2**30
    m = mha * ctx * batch / 2**30
    print(f"{ctx:>13} {batch:>17} {g:8.1f} {m:9.1f}")
