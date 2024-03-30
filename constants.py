from structure import ModelVersion, Region
from typing import Final

class AzureOpenAIConstansts:
    API_VERSION:Final[str]="2024-02-01"
    API_KEY:Final[str]="AZURE_OPENAI_API_KEY"
    MODEL_DEPLOYMENTS = {
        ModelVersion.gpt4t0125:'llm-runner-gpt4t-0125'
    }
    ENDPOINTS = {
        Region.EastUS:"https://eng-latency.openai.azure.com/"
    }

class OpenAIContants:
    MODEL_DEPLOYMENTS = {
        ModelVersion.gpt4t0125:'gpt-4-0125-preview'
    }

class WikiConstants:    
    RANDOM_URL: Final[str] = 'https://en.wikipedia.org/wiki/Special:Random'
    WIKI_PREFIX_LEN: Final[int] = len('https://en.wikipedia.org/wiki/')