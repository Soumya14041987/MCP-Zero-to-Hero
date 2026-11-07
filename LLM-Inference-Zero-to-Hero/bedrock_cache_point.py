"""Bedrock Converse prompt caching: a cachePoint after the static prefix.
NOT RUN in the episode container (needs AWS credentials and a model with caching). Review before use."""
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = client.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",   # VERIFY: pick a caching-enabled model in your region
    system=[{"text": "You are an ops agent. <long static instructions + tool docs here>"},
            {"cachePoint": {"type": "default"}}],               # everything above is cached
    messages=[{"role": "user", "content": [{"text": "Why is pod web-7 crash-looping?"}]}],
)
print(resp["usage"])   # look for cacheReadInputTokens / cacheWriteInputTokens
