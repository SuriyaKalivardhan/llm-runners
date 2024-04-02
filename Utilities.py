from openai import OpenAI, AzureOpenAI
from constants import OpenAIContants, AzureOpenAIConstansts, ModelVersion
from structure import ServiceProvider, Region, RequestInput, ResponseOutput
import logging, os, time
from io import TextIOWrapper
from datetime import datetime
logging.basicConfig(level=logging.DEBUG)

class Utilities:
    def get_model_version(model_version:ModelVersion, provider:ServiceProvider) -> str:
        if provider == ServiceProvider.OpenAI:            
            return OpenAIContants.MODEL_DEPLOYMENTS[model_version]
        elif provider == ServiceProvider.AzureOpenAI:
            return AzureOpenAIConstansts.MODEL_DEPLOYMENTS[model_version]
        else:
            return None
        
    def getClient(provider:ServiceProvider, region:Region = None) -> OpenAI | AzureOpenAI:
        if provider == ServiceProvider.OpenAI:
            return OpenAI()
        elif provider == ServiceProvider.AzureOpenAI:
            return AzureOpenAI(
                api_key=os.getenv(AzureOpenAIConstansts.API_KEY),
                api_version=AzureOpenAIConstansts.API_VERSION,
                azure_endpoint = AzureOpenAIConstansts.ENDPOINTS[region]
        )

    def create_and_get_new_file() -> TextIOWrapper:        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = open(f"/tmp/{timestr}.tsv", "a")
        return f


    def log(provider:ServiceProvider, req:RequestInput, resp:ResponseOutput):
        return f"{provider.name}\t{str(datetime.utcnow())}\t{req.getStr()}\t{resp.getStr()}\n"
    
    def get_all_possible_input_sizes(max_total_len:int, min_prompt_len:int=1, max_prompt_len:int=None, min_gen_len:int=1, max_gen_len:int=None) -> list[tuple[int, int]]:
        result = []
        max_prompt_len = max_total_len if max_prompt_len is None else max_prompt_len
        max_gen_len = max_total_len if max_gen_len is None else max_gen_len

        i = min_prompt_len
        while i<max_prompt_len:
            j = min_gen_len
            while j<max_gen_len:
                if i+j > max_total_len:
                    break
                result.append((i, j))
                j = Utilities.tens_incr(j)

            i = Utilities.tens_incr(i)
        return result
    

    def tens_incr(x:int) -> int:
        if x<10:
            return x+1
        elif x<100:
            return x+10
        elif x<1000:
            return x+100
        elif x<10000:
            return x+1000
        elif x<100000:
            return x+10000
