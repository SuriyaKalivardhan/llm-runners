from openai import OpenAI
from openai.types import CreateEmbeddingResponse, Embedding
from openai import Stream
from structure import RequestInput, ResponseOutput, ServiceProvider, Region
from Utilities import Utilities
import openai
import time
import logging
import tiktoken
logging.basicConfig(level=logging.INFO)

class StreamingRequestHandler:
    def __init__(self, provider:ServiceProvider, region:Region = Region.Global):        
        self.provider = provider
        self.client = Utilities.getClient(provider, region)
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
    def score(self, req:RequestInput) -> ResponseOutput:
        model_version:str = Utilities.get_model_version(req.model_version, self.provider)
        back_off = 5.0
        while True:
            try:
                samples = []
                finish_reason:str = None
                byteTimes = []

                start = time.time()
                response:CreateEmbeddingResponse = self.client.embeddings.create(
                    input=req.Prompt,
                    model=model_version)
                
                end = time.time()

                ttft = ttlt = start-end
                ttbt = 0.0

                ttft = '%.6f'%(ttft)
                #tbt = ['%.6f'%(bt) for bt in byteTimes[1:]]
                ttlt = '%.6f'%(ttlt)
                ttbt = '%.6f'%(ttbt)

                prompt_encoded = self.encoder.encode(req.Prompt)
                samples = []
                result = ResponseOutput("", ttft, [ttbt], ttbt, ttlt, finish_reason, len(prompt_encoded), len(samples), 0) #TODO: calculate edit distance
                return result
            except openai.RateLimitError as e:
                logging.info(f"A 429 status code was received; backing off {back_off=} {e}")
                time.sleep(back_off)
                back_off = back_off * 1.5