from Infer import InferenceClient
def test_infer():
    client:InferenceClient = InferenceClient("http://localhost:8000/v1/completions") # https://api.openai.com/v1/completions
    data = {
        "model": "text-davinci-003", # Or any other available model
        "prompt": "Translate the following English text to French: '{}'",
        "temperature": 0.5,
        "max_tokens": 100,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_OPENAI_API_KEY"
    }
    response = client.get(data, headers)
    assert response is not None