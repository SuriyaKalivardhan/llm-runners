from openai import OpenAI, AzureOpenAI
from constants import OpenAIContants, AzureOpenAIConstansts, ModelVersion
from structure import ServiceProvider, Region
import logging, os
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

