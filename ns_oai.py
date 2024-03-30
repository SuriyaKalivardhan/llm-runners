from openai import OpenAI
import time
client = OpenAI()
start = time.time()
completion = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        },
    ],
)
end = time.time()
print(completion)
print(end-start)