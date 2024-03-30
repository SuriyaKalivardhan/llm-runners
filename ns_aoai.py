import os
from openai import AzureOpenAI
import time

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint = "https://eng-latency.openai.azure.com/"
)


start = time.time()
response = client.completions.create(
    model="llm-runner-gpt4t-0125",
    prompt="Say this is test",
    max_tokens=100)
end=time.time()
print(response)
print(end-start)