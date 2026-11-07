# LLM Inference: Zero to Hero (Part 1), explained with an AI agent

Running example: an ops agent asking "why is pod web-7 crash-looping?". Each file is one step of that agent's loop.
Tested on Python 3.13, numpy 2.5.3, CPU only. Output: run-output.txt. Run: `cd LLM-Inference-Zero-to-Hero && python3 00_agent_loop.py` (then 01 ... 07).

| File | Step |
|---|---|
| 00_agent_loop.py | an agent is a loop of inference calls (scripted stub model) |
| 01_generation_loop.py | one forward pass per token (toy NumPy transformer, random weights) |
| 02_kv_cache.py | KV cache gives identical output with far less work |
| 03_kv_memory.py | KV cache memory, GQA vs MHA |
| 04_prefill_vs_decode.py | why decode is bandwidth-bound (CPU measurement) |
| 05_paged_blocks.py | slab vs paged allocation (simulation, not vLLM) |
| 06_speculative.py | speculative decoding keeps the target distribution (toy) |
| 07_agent_prefix_cache.py | prefix caching arithmetic for an agent |
| bedrock_cache_point.py | Bedrock Converse cachePoint. NOT RUN: needs AWS credentials; verify model ID |

Limits: toy model, no GPU. Timings vary per run. Llama 3 8B shape in 03 is from memory; verify against its config.json.
