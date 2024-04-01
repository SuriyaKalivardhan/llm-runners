from WikiClient import WikiClient
from structure import ModelVersion, RequestInput
import logging
import tiktoken
logging.basicConfig(level=logging.INFO)
class InputProcessor:
    def __init__(self, dataSourceClient:WikiClient) -> None:
        self.dataSourceClient = dataSourceClient
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def _get_all_possible_input_sizes(self, total_len:int, min_prompt_len:int=1, min_gen_len:int=1) -> list[tuple[int, int]]:
        result = []        
        i = min_prompt_len
        while i<total_len:
            j = min_gen_len
            while i<total_len:
                if i+j > total_len:
                    break
                result.append((i, j))
                if j<10:
                    j = j+1
                elif j<100:
                    j = j+10
                elif j<1000:
                    j = j+100
                elif j<10000:
                    j = j+1000
                elif j<100000:
                    j = j+10000

            if i<10:
                i = i+1
            elif i<100:
                i = i+10
            elif i<1000:
                    i = i+100
            elif i<10000:
                    i = i+1000
            elif i<100000:
                    i = i+10000
        return result
    
    def _getDataInput(self, total_len:int, n_prompt:int):
        token_len = 0
        while token_len < total_len:
            page, text = self.dataSourceClient.get_random_page_text()            
            text = ' '.join(text.splitlines())
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
            return (prompt, samples)
        
    def _getInput(self, model_version: ModelVersion, total_len:int, n_prompt, stream:bool) -> RequestInput:
        prompt, samples = self._getDataInput(total_len, n_prompt)
        return RequestInput(model_version, prompt, total_len-n_prompt, stream, samples)
    

    def getInput(self, model_version: ModelVersion = ModelVersion.gpt4t0125, total_len:int=1000, stream:bool=None, min_prompt_len=10, min_gen_len=10) -> list[RequestInput]:
        input_len:list[tuple[int, int]] = self._get_all_possible_input_sizes(total_len, min_prompt_len, min_gen_len)
        result:list[RequestInput] = []
        if stream is None:
            logging.info("No streaming is specified, generating for both streaming and non-streaming")
            for n_prompt, n_samples in input_len:
                result.append(self._getInput(model_version, n_prompt+n_samples, n_prompt, True))
                result.append(self._getInput(model_version, n_prompt+n_samples, n_prompt, False))
        else:
            for n_prompt, n_samples in input_len:
                result.append(self._getInput(model_version, n_prompt+n_samples, n_prompt, stream))
        return result


            

        


