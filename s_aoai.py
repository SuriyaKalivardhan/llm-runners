import os
from openai import AzureOpenAI
import time

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint = "https://eng-latency.openai.azure.com/"
)


byteTimes = []
start = time.time()
stream = client.chat.completions.create(
    model="llm-runner-gpt4t-0125",
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }],
    max_tokens=100,    
    stream=True,
)
for chunk in stream:
    if not chunk.choices:
        continue
    end = time.time()
    byteTimes.append(end-start)
    start=end
    print(chunk)

print(byteTimes)