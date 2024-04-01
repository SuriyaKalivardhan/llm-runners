from WikiClient import WikiClient
from structure import ModelVersion, RequestInput
import logging
import tiktoken
logger = logging.getLogger(__name__)

class InputProcessor:
    def __init__(self, dataSourceClient:WikiClient) -> None:
        self.dataSourceClient = dataSourceClient
        self.encoder = tiktoken.get_encoding("cl100k_base")
        logger.setLevel(logging.DEBUG)

    def _get_all_possible_input_sizes(self, total_len:int, min_prompt_len:int=1) -> list[tuple[int, int]]:
        result = []
        for i in range(min_prompt_len, total_len):
            result.append((i, total_len-i))
        return result
    
    def _getDataInput(self, total_len:int, n_prompt:int):
        token_len = 0
        while token_len < total_len:
            page, text = self.dataSourceClient.get_random_page_text()
            logger.info(f"Got {page=} of length {len(text)} for {total_len=} and {n_prompt=}")
            tokens = self.encoder.encode(text)
            token_len = len(tokens)
            if token_len < total_len:
                logger.info(f"{token_len=} is smaller {total_len=} retrying..")
                continue
            prompt_tokens = tokens[:n_prompt]
            expected_sample_tokens = tokens[n_prompt:]
            prompt = self.encoder.decode(prompt_tokens)
            samples = self.encoder.decode(expected_sample_tokens)
            return (prompt, samples)
        
    def _getInput(self, model_version: ModelVersion, total_len:int, n_prompt, stream:bool) -> RequestInput:
        prompt, samples = self._getDataInput(total_len, n_prompt)
        return RequestInput(model_version, prompt, total_len-n_prompt, stream, samples)
    

    def getInput(self, model_version: ModelVersion = ModelVersion.gpt4t0125, total_len:int=1000, stream:bool=None, min_prompt_len=10) -> list[RequestInput]:
        input_len:list[tuple[int, int]] = self._get_all_possible_input_sizes(total_len, min_prompt_len)
        result:list[RequestInput] = []
        if stream is None:
            for n_prompt, n_samples in input_len:
                result.append(self._getInput(model_version, n_prompt+n_samples, n_prompt, True))
                result.append(self._getInput(model_version, n_prompt+n_samples, n_prompt, False))
        else:
            for n_prompt, n_samples in input_len:
                result.append(self._getInput(model_version, n_prompt+n_samples, n_prompt, stream))
        return result


            

        


