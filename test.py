from openai import OpenAI
from openai.types import CreateEmbeddingResponse, Embedding

client = OpenAI()

response:CreateEmbeddingResponse = client.embeddings.create(input="Hello world in the this world", model="text-embedding-3-small")
print(response.data[0])
#print(response.data)
