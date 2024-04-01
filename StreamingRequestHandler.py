from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai import Stream
from structure import RequestInput, ResponseOutput, ServiceProvider, Region
from Utilities import Utilities
import time
import logging
import tiktoken
logging.basicConfig(level=logging.DEBUG)

class StreamingRequestHandler:
    def __init__(self, provider:ServiceProvider, region:Region = Region.Global):        
        self.provider = provider
        self.client = Utilities.getClient(provider, region)
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
    def score(self, req:RequestInput) -> ResponseOutput:
        model_version:str = Utilities.get_model_version(req.model_version, self.provider)
        samples = []
        finish_reason:str = None
        byteTimes = []

        start = start_for_ttlt = time.time()        
        response:Stream[ChatCompletionChunk] = self.client.chat.completions.create(
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

        for chunk in response:
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            if choice.delta.content is None:
                finish_reason = choice.finish_reason
                break
            elif choice.delta.role is None:
                end = time.time()
                samples.append(choice.delta.content)            
                byteTimes.append(end-start)
                start=end

        ttft = byteTimes[0]
        ttbt = byteTimes[1:]
        ttlt = end-start_for_ttlt

        prompt_encoded = self.encoder.encode(req.Prompt)
        result = ResponseOutput(samples, ttft, ttbt, ttlt, finish_reason, len(prompt_encoded), len(samples), 0) #TODO: calculate edit distance
        logging.info(result)
        return result