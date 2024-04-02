from structure import ModelVersion, Region
from typing import Final

class AzureOpenAIConstansts:
    API_VERSION:Final[str]="2024-02-01"
    API_KEY:Final[str]="AZURE_OPENAI_API_KEY"
    MODEL_DEPLOYMENTS: dict[ModelVersion, str] = {
        ModelVersion.gpt4t0125:'llm-runner-gpt4t-0125',        
        ModelVersion.gpt4t1106:'llm-runner-gpt4t-1106'
    }
    ENDPOINTS = {
        Region.EastUS:"https://eng-latency.openai.azure.com/",
        Region.NorthCentralUS:"https://eng-latency-ncus.openai.azure.com/",
        Region.SouthCentralUS:"https://eng-latency-scus.openai.azure.com/",
        Region.WestUS:"https://eng-latency.openai-wus.azure.com/",
        Region.SwedenCentral:"https://eng-latency-sw.openai.azure.com/",
    }

class OpenAIContants:
    MODEL_DEPLOYMENTS: dict[ModelVersion, str] = {
        ModelVersion.gpt4t0125:'gpt-4-0125-preview',
        ModelVersion.gpt4t1106:'gpt-4-1106-preview'
    }

class WikiConstants:    
    RANDOM_URL: Final[str] = 'https://en.wikipedia.org/wiki/Special:Random'
    WIKI_PREFIX_LEN: Final[int] = len('https://en.wikipedia.org/wiki/')