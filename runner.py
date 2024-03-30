from structure import ServiceProvider, Region
from constants import AzureOpenAIConstansts
from openai import OpenAI, AzureOpenAI
import os

def getClient(provider:ServiceProvider, region:Region = None) -> OpenAI | AzureOpenAI:
    if provider == ServiceProvider.OpenAI:
        return OpenAI()
    elif provider == ServiceProvider.AzureOpenAI:
        return AzureOpenAI(
            api_key=os.getenv(AzureOpenAIConstansts.api_key),
            api_version=AzureOpenAIConstansts.api_version,
            azure_endpoint = AzureOpenAIConstansts.endpoints[region]
)

if __name__ == "__main__":
    openai = getClient(ServiceProvider.OpenAI)
    azureopenai = getClient(ServiceProvider.AzureOpenAI, Region.EastUS)