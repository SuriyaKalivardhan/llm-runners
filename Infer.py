import requests

class InferenceClient:
    def __init__(self, endpoint, metricsSink = None) -> None:
        self.endpoint = endpoint

    def get(self, data = None, headers= None):
        response = requests.post(self.endpoint, json=data, headers=headers)
        return response.json()