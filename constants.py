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
    
class KustoConstants:
    AAD_TENANT_ID: Final[str] = "6babcaad-604b-40ac-a9d7-9fd97c0b779f"    
    CLIENT_ID = "6e8d915a-460b-499c-a77f-10add633ef38"
    KUSTO_URI: Final[str] = "https://llm-runners.eastus.kusto.windows.net"
    KUSTO_INGEST_URI: Final[str] = "https://ingest-llm-runners.eastus.kusto.windows.net"
    IMDS_URL = 'http://169.254.169.254/metadata/identity/oauth2/token'
    KUSTO_DATABASE: Final[str] = "llm-runner"
    KUSTO_TABLE: Final[str] = "InferencingEvents"
    KUSTO_MAPPING_REFERENCE= "InferencingEvents_TSV_Mapping"