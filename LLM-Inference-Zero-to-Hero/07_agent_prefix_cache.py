"""Step 7: an AI agent re-sends its whole history every turn. Count prefill tokens."""
SYSTEM, TOOLS = 800, 1500                    # system prompt + tool schemas (tokens)
TURN_NEW = 350                               # new tokens per step (tool call + tool result)
STEPS = 12

history = SYSTEM + TOOLS
no_cache = cached_hits = 0
for step in range(STEPS):
    no_cache += history                       # no caching: whole prompt prefilled again
    cached_hits += history if step else 0     # cache: everything seen last turn is a hit
    history += TURN_NEW
fresh = no_cache - cached_hits
print(f"prompt tokens sent over {STEPS} steps : {no_cache}")
print(f"prefilled fresh with prefix caching   : {fresh}  ({100*fresh/no_cache:.0f}% of the work)")
