from openai.types import CreateEmbeddingResponse
from structure import RequestInput, ResponseOutput, ServiceProvider, Region
from Utilities import Utilities
import openai
import time
import logging
logging.basicConfig(level=logging.INFO)

class EmbeddingHandler:
    def __init__(self, provider:ServiceProvider, region:Region = Region.Global):        
        self.provider = provider
        self.client = Utilities.getClient(provider, region)
        
    def score(self, req:RequestInput) -> ResponseOutput:
        model_version:str = Utilities.get_model_version(req.model_version, self.provider)
        back_off = 5.0
        while True:
            try:
                start = time.time()
                response:CreateEmbeddingResponse = self.client.embeddings.create(
                    input=req.Prompt,
                    model=model_version)
                logging.info(f"Logging {len(response.data[0].embedding)} embeddings for {response.usage.prompt_tokens}")
                
                end = time.time()

                ttft = ttlt = ttbt = end-start

                ttft = '%.6f'%(ttft)
                #tbt = ['%.6f'%(bt) for bt in byteTimes[1:]]
                ttlt = '%.6f'%(ttlt)
                ttbt = '%.6f'%(ttbt)
    
                prompts_usage = response.usage.prompt_tokens
                result = ResponseOutput(None, ttft, [ttbt], ttbt, ttlt, None, prompts_usage, 0, 0) #TODO: calculate edit distance
                return result
            except openai.RateLimitError as e:
                logging.info(f"A 429 status code was received; backing off {back_off=} {e}")
                time.sleep(back_off)
                back_off = back_off * 1.5