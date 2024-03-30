from openai import OpenAI
import time
client = OpenAI()
byteTimes = []
start = time.time()
stream = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
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