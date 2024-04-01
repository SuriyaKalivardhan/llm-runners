from WikiClient import WikiClient
from structure import ServiceProvider, Region, ModelVersion
from constants import AzureOpenAIConstansts
from openai import OpenAI, AzureOpenAI
from InputProcessor import InputProcessor
import os

def getClient(provider:ServiceProvider, region:Region = None) -> OpenAI | AzureOpenAI:
    if provider == ServiceProvider.OpenAI:
        return OpenAI()
    elif provider == ServiceProvider.AzureOpenAI:
        return AzureOpenAI(
            api_key=os.getenv(AzureOpenAIConstansts.API_KEY),
            api_version=AzureOpenAIConstansts.API_VERSION,
            azure_endpoint = AzureOpenAIConstansts.ENDPOINTS[region]
)

if __name__ == "__main__":
    openai = getClient(ServiceProvider.OpenAI)
    azureopenai = getClient(ServiceProvider.AzureOpenAI, Region.EastUS)
    ip:InputProcessor = InputProcessor(WikiClient())
    result = ip.getInput(ModelVersion.gpt4t0125, total_len=10, stream=None, min_prompt_len=5)
    # for i in result:
    #     print(result, end="\n")