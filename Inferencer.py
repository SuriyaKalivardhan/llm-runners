from structure import ServiceProvider, Region, RequestInput, ModelVersion, Environment
from handlers.EmbeddingHandler import EmbeddingHandler
from handlers.RequestHandler import RequestHandler
from handlers.StreamingRequestHandler import StreamingRequestHandler
from Utilities import Utilities
from WikiClient import WikiClient
import logging
import tiktoken
from datetime import datetime, timezone
import time, threading, traceback
from MetricsWriter import MetricsWriter
from typing import List

logging.basicConfig(level=logging.INFO)

class Inferencer:
    def __init__(self, environment:Environment, azure_region:Region):
        self.dataSourceClient = WikiClient()
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.embedding_handlers = [
            EmbeddingHandler(ServiceProvider.OpenAI),
            EmbeddingHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
        self.streaming_handlers = [
            StreamingRequestHandler(ServiceProvider.OpenAI),
            StreamingRequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
        self.non_streaming_handlers = [
            RequestHandler(ServiceProvider.OpenAI),
            RequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]

        self.metricsWriter = MetricsWriter(environment, azure_region)

    def score(self, candidates:tuple[int, int], model_versions: List[ModelVersion] = [ModelVersion.gpt4t0125]): #TODO: Update the function name - Not just streaming anymore. Include embeddings
        Utilities.touch_for_liveness()
        for idx, (n_prompt, n_samples) in enumerate(candidates):
            text_only_request = self._getInput(model_versions[0], n_prompt, n_samples, True, includeImage=False)
            for model_version in model_versions:
                text_only_request.model_version = model_version
                logging.info(f"{idx=} {text_only_request=}")
                threads = []

                if model_version in ModelVersion.vision_list():                    
                    text_image_request = self._getInput(model_version, n_prompt, n_samples, True, includeImage=True)                    
                    for handler in self.streaming_handlers:
                        threads.append(threading.Thread(target=self.invokeHandler, args=(handler, text_image_request)))
                elif model_version in ModelVersion.embeddings_list():
                    for handler in self.embedding_handlers:
                        threads.append(threading.Thread(target=self.invokeHandler, args=(handler, text_only_request)))
                else:
                    for handler in self.streaming_handlers:
                        threads.append(threading.Thread(target=self.invokeHandler, args=(handler, text_only_request)))

                for t in threads:
                    t.start()

                for t in threads:
                    t.join()

                Utilities.touch_for_liveness()

                back_off = Utilities.get_back_off_time(n_prompt+n_samples)
                logging.info(f"{back_off=}")
                time.sleep(back_off)
    
    def invokeHandler(self, handler:StreamingRequestHandler, request:RequestInput):
        requestTime = datetime.now(timezone.utc)
        try:
            response = handler.score(request)
            self.metricsWriter.writeMetrics(requestTime, handler.provider, request, response)
        except Exception as e:
            logging.critical(traceback.format_exc())

    def close(self):
        self.metricsWriter.close()

    def _getDataInputText(self, n_prompt:int, n_samples:int):
        token_len = 0
        total_len = n_prompt # + n_samples (Just n_prompt for now since we are not recording samples)
        logging.info(f"{n_prompt=} {n_samples=}")
        while token_len < total_len:
            page, text = self.dataSourceClient.get_random_page_text()
            text = ' '.join(text.splitlines())
            text = text.replace('\t', ' ')
            #logging.info(f"Got {page=} of length {len(text)} for {total_len=} and {n_prompt=}")
            tokens = self.encoder.encode(text)
            token_len = len(tokens)
            if token_len < total_len:
                #logging.info(f"{token_len=} is smaller {total_len=} retrying another page..")
                continue
            prompt_tokens = tokens[:n_prompt]
            # expected_sample_tokens = tokens[n_prompt:]
            prompt = self.encoder.decode(prompt_tokens)
            # samples = self.encoder.decode(expected_sample_tokens) #TODO: Enable this for edit distance later
            # samples = None
            #return (prompt, samples)
            return prompt

    def _getDataInputTextAndImage(self):
        prompt, imageUrl = self.dataSourceClient.get_random_page_textAndImage()
        prompt = ' '.join(prompt.splitlines())
        prompt = prompt.replace('\t', ' ')
        return prompt, imageUrl
        
    def _getInput(self, model_version: ModelVersion, n_prompt:int, n_samples:int, stream:bool, includeImage:bool=False) -> RequestInput:
        image_url:str = None
        if includeImage:
            prompt, image_url = self._getDataInputTextAndImage()
        else:
            prompt = self._getDataInputText(n_prompt, n_samples)
        return RequestInput(model_version, prompt, n_samples, stream, None, image_url)