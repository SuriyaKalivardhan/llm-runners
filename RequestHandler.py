from openai.types.chat import ChatCompletion
from structure import RequestInput, ResponseOutput, ServiceProvider, Region
from Utilities import Utilities
import time
import logging
logging.basicConfig(level=logging.DEBUG)

class RequestHandler:
    def __init__(self, provider:ServiceProvider, region:Region = Region.Global):        
        self.provider = provider
        self.client = Utilities.getClient(provider, region)
        
    def score(self, req:RequestInput) -> ResponseOutput:
        model_version:str = Utilities.get_model_version(req.model_version, self.provider)
        start = time.time()

        response:ChatCompletion = self.client.chat.completions.create(
            model=model_version,
            messages=[
                {
                    "role": "user",
                    "content": req.Prompt,
                },
            ],
            max_tokens=req.max_token,
            stream=req.stream,
        )

        end = time.time()
        choice = response.choices[0]
        samples_str = ' '.join(choice.message.content.splitlines())
        samples_str = samples_str.replace('\t', ' ')
        result = ResponseOutput(samples_str, None, None, '%.6f'%(end-start), choice.finish_reason, response.usage.prompt_tokens, response.usage.completion_tokens, 0) #TODO: calculate edit distance
        return result