"""Step 1: generation is a loop. One forward pass per new token, no cache."""
import numpy as np
from toy_model import make_weights, forward

W = make_weights()
tokens = [5, 17, 42]                      # the "prompt"
passes = tokens_processed = 0
for _ in range(5):                        # generate 5 tokens
    logits = forward(W, np.array(tokens))  # re-reads the WHOLE sequence every step
    tokens.append(int(np.argmax(logits)))  # greedy pick
    passes += 1
    tokens_processed += len(tokens) - 1
print("generated:", tokens)
print(f"forward passes: {passes}, tokens re-processed in total: {tokens_processed}")
