from structure import ServiceProvider, Region, RequestInput, ModelVersion
from StreamingRequestHandler import StreamingRequestHandler
from RequestHandler import RequestHandler
from io import TextIOWrapper
from Utilities import Utilities
from WikiClient import WikiClient
import logging
import tiktoken
import time
logging.basicConfig(level=logging.DEBUG)

class Inferencer:
    def __init__(self, azure_region:Region):
        self.streaming_handlers = [
            StreamingRequestHandler(ServiceProvider.OpenAI),
            StreamingRequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
        self.non_streaming_handlers = [
            RequestHandler(ServiceProvider.OpenAI),
            RequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
        self.file:TextIOWrapper = Utilities.create_and_get_new_file()
        self.dataSourceClient = WikiClient()        
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def score(self, requests:list[RequestInput]):
        for request in requests:
            logging.info(f"Starting {request.model_version.name} {request.stream} {len(request.Prompt)/4} {request.max_token}")
            if request.stream:
                for handler in self.streaming_handlers:
                    response = handler.score(request)
                    self.file.write(Utilities.log(handler.provider, request, response))
            else:
                for handler in self.non_streaming_handlers:
                    response = handler.score(request)
                    self.file.write(Utilities.log(handler.provider, request, response))
            self.file.flush()

    def score_v1(self, inputs:tuple[int, int], model_version: ModelVersion = ModelVersion.gpt4t0125, stream:bool=None) -> list[RequestInput]:
        if stream == True:
            for n_prompt, n_samples in inputs:
                request = self._getInput(model_version, n_prompt, n_samples, stream)
                print(request)
                for handler in self.streaming_handlers:
                    try:
                        response = handler.score(request)
                        self.file.write(Utilities.log(handler.provider, request, response))
                    except:
                        logging.critical("Exception caught")
                self.file.flush()
                logging.info(f"Sleeping {(n_prompt+n_samples)/50} to backoff")
                time.sleep((n_prompt+n_samples)/50)

    def close(self):
        self.file.close()

    def _getDataInput(self, n_prompt:int, n_samples:int):
        token_len = 0
        total_len = n_prompt + n_samples
        print(f"{n_prompt=} {n_samples=}")
        while token_len < total_len:
            page, text = self.dataSourceClient.get_random_page_text()            
            text = ' '.join(text.splitlines())
            text = text.replace('\t', ' ')
            logging.info(f"Got {page=} of length {len(text)} for {total_len=} and {n_prompt=}")
            tokens = self.encoder.encode(text)
            token_len = len(tokens)
            if token_len < total_len:
                logging.info(f"{token_len=} is smaller {total_len=} retrying another page..")
                continue
            prompt_tokens = tokens[:n_prompt]
            expected_sample_tokens = tokens[n_prompt:]
            prompt = self.encoder.decode(prompt_tokens)
            samples = self.encoder.decode(expected_sample_tokens) #TODO: Enable this for edit distance later
            samples = None
            #return (prompt, samples)
            return prompt
        
    def _getInput(self, model_version: ModelVersion, n_prompt:int, n_samples:int, stream:bool) -> RequestInput:
        prompt = self._getDataInput(n_prompt, n_samples)
        return RequestInput(model_version, prompt, n_samples, stream, "")