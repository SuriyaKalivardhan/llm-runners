from structure import ServiceProvider, Region, RequestInput, ModelVersion, Environment
from StreamingRequestHandler import StreamingRequestHandler
from RequestHandler import RequestHandler
from Utilities import Utilities
from WikiClient import WikiClient
import logging
import tiktoken
from datetime import datetime, timezone
import time
from MetricsWriter import MetricsWriter

logging.basicConfig(level=logging.INFO)

class Inferencer:
    def __init__(self, environment:Environment, azure_region:Region):
        self.dataSourceClient = WikiClient()
        self.encoder = tiktoken.get_encoding("cl100k_base")

        self.streaming_handlers = [
            StreamingRequestHandler(ServiceProvider.OpenAI),
            StreamingRequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
        self.non_streaming_handlers = [
            RequestHandler(ServiceProvider.OpenAI),
            RequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]

        self.metricsWriter = MetricsWriter(environment, azure_region)

    def score_stream(self, candidates:tuple[int, int], model_version: ModelVersion = ModelVersion.gpt4t0125) -> list[RequestInput]:
        for n_prompt, n_samples in candidates:
            request = self._getInput(model_version, n_prompt, n_samples, True)
            logging.info(request)
            for handler in self.streaming_handlers:
                requestTime = datetime.now(timezone.utc)
                try:
                    response = handler.score(request)
                    self.metricsWriter.writeMetrics(requestTime, handler.provider, request, response)
                except Exception as e:
                    import traceback
                    logging.critical(traceback.format_exc())
            back_off = Utilities.get_back_off_time(n_prompt+n_samples)
            logging.info(f"{back_off=}")
            time.sleep(back_off)

    def close(self):
        self.metricsWriter.close()

    def _getDataInput(self, n_prompt:int, n_samples:int):
        token_len = 0
        total_len = n_prompt # + n_samples (Just n_prompt for now since we are not recording samples)
        logging.info(f"{n_prompt=} {n_samples=}")
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
            # expected_sample_tokens = tokens[n_prompt:]
            prompt = self.encoder.decode(prompt_tokens)
            # samples = self.encoder.decode(expected_sample_tokens) #TODO: Enable this for edit distance later
            # samples = None
            #return (prompt, samples)
            return prompt
        
    def _getInput(self, model_version: ModelVersion, n_prompt:int, n_samples:int, stream:bool) -> RequestInput:
        prompt = self._getDataInput(n_prompt, n_samples)
        return RequestInput(model_version, prompt, n_samples, stream, None)