"""Step 0: an AI agent is a loop of inference calls. The model is a SCRIPTED STUB here,
so we can count exactly what each call has to read (tokens = whitespace words, approximate)."""
SYSTEM = "You are an ops agent. Tools: kubectl_logs, kubectl_describe, search_runbook. " * 12
SCRIPT = [  # (what the model says, what the tool returns)
    ('CALL kubectl_describe pod web-7', "State: CrashLoopBackOff, Exit Code 137, Reason: OOMKilled " * 6),
    ('CALL kubectl_logs pod web-7',     "java.lang.OutOfMemoryError: Java heap space " * 10),
    ('CALL search_runbook OOMKilled',   "Raise the memory limit or reduce the heap size. " * 8),
    ('ANSWER web-7 is OOMKilled, raise the memory limit', ""),
]
tok = lambda s: len(s.split())
prompt = "User: why is pod web-7 crash-looping? " + SYSTEM
for n, (reply, tool_out) in enumerate(SCRIPT, 1):
    print(f"inference call {n}: reads {tok(prompt):4d} tokens, writes {tok(reply):2d} tokens")
    prompt += f"\nAssistant: {reply}\nTool: {tool_out}"      # the whole history goes back in
