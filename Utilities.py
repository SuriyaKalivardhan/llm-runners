from openai import OpenAI, AzureOpenAI
from constants import OpenAIContants, AzureOpenAIConstansts, ModelVersion, ApplicationConstants, AWSConstants
from structure import ServiceProvider, Region
import logging, os, time
from io import TextIOWrapper
import boto3
import random
import sys
from pathlib import Path
logging.basicConfig(level=logging.INFO)

class Utilities:
    def get_model_version(model_version:ModelVersion, provider:ServiceProvider) -> str:
        try:
            if provider == ServiceProvider.OpenAI:
                return OpenAIContants.MODEL_DEPLOYMENTS[model_version]
            elif provider == ServiceProvider.AzureOpenAI:
                return AzureOpenAIConstansts.MODEL_DEPLOYMENTS[model_version]
            elif provider == ServiceProvider.AWS:
                return AWSConstants.MODEL_DEPLOYMENTS[model_version]
            else:
                return None
        except KeyError:
            return None

    def getClient(provider:ServiceProvider, region:Region = None):
        if provider == ServiceProvider.OpenAI:
            return OpenAI(
                max_retries=0
            )
        elif provider == ServiceProvider.AzureOpenAI:
            return AzureOpenAI(
                api_key=os.getenv(AzureOpenAIConstansts.API_KEY),
                api_version=AzureOpenAIConstansts.API_VERSION,
                azure_endpoint = AzureOpenAIConstansts.ENDPOINTS[region],
                max_retries=0
            )
        elif provider == ServiceProvider.AWS:
            return boto3.client(AWSConstants.Service, AWSConstants.Region[region])

    def create_and_get_new_file() -> TextIOWrapper:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = open(f"/tmp/{timestr}.tsv", "a")
        return f

    def construct_candidates( rpm:int, num_prompts:int, num_samples:int) -> list[tuple[int, int]]:
        if num_prompts != sys.maxsize and num_samples != sys.maxsize:
            return [(num_prompts, num_samples) for _ in range(rpm*60)]
        else:
            return Utilities.get_uniform_distributed_candidates()

    def get_uniform_distributed_candidates(min_prompt_len:int=50, max_prompt_len:int=5000, min_gen_len:int=10, max_gen_len:int=1000) -> list[tuple[int, int]]:
        result = []
        i=10
        while i>0:
            x = random.randint(min_prompt_len, max_prompt_len)
            j=10
            i-=1
            while j>0:
                y = random.randint(min_gen_len, max_gen_len)
                j-=1
                result.append((x, y))
        return result

    def get_back_off_time(total_tokens:int) -> float:
        return (total_tokens*1.0)/(60000/60)
    

    def touch_for_liveness() -> None:
        with Path(ApplicationConstants.LivenessFile) as f:
            f.touch()
