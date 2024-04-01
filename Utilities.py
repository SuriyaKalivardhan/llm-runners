from openai import OpenAI, AzureOpenAI
from constants import OpenAIContants, AzureOpenAIConstansts, ModelVersion
from structure import ServiceProvider, Region, RequestInput, ResponseOutput
import logging, os, time
from io import TextIOWrapper
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
        return f"{provider.name}\t{req}\t{resp}\n"

