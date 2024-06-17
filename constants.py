from structure import ModelVersion, Region
from typing import Final

class AzureOpenAIConstansts:
    API_VERSION:Final[str]="2024-02-01"
    API_KEY:Final[str]="AZURE_OPENAI_API_KEY"
    MODEL_DEPLOYMENTS: dict[ModelVersion, str] = {
        ModelVersion.gpt4t0409:'llm-runner-gpt4t-0409',
        ModelVersion.gpt4t0125:'llm-runner-gpt4t-0125',
        ModelVersion.gpt4t1106:'llm-runner-gpt4t-1106',
        ModelVersion.gpt40613:'llm-runner-gpt4-0613',
        ModelVersion.textembeddings3large:'llm-runner-textemb3-l',
        ModelVersion.textembeddings3small:'llm-runner-textemb3-s',
        ModelVersion.gpt35t0613:'llm-runner-gpt35t-0613',
        ModelVersion.gpt4o0513:'llm-runner-gpt40-0513'

    }
    ENDPOINTS = {
        Region.EastUS:"https://eng-latency.openai.azure.com/",
        Region.EastUS2:"https://eng-latency.openai.azure.com/",
        Region.NorthCentralUS:"https://eng-latency-ncus.openai.azure.com/",
        Region.SouthCentralUS:"https://eng-latency-scus.openai.azure.com/",
        Region.WestUS:"https://eng-latency-wus.openai.azure.com/",
        Region.SwedenCentral:"https://eng-latency-sw.openai.azure.com/",
        Region.UKSouth:"https://eng-latency-uks.openai.azure.com/",
        Region.FranceCentral:"https://francecentral.api.cognitive.microsoft.com/",
        Region.AustraliaEast:"https://australiaeast.api.cognitive.microsoft.com/",
        Region.JapanEast:"https://japaneast.api.cognitive.microsoft.com/",
        Region.SouthIndia:"https://southindia.api.cognitive.microsoft.com/",
        Region.EastUS2:"https://eng-latency-eus2.openai.azure.com/",
    }

class OpenAIContants:
    MODEL_DEPLOYMENTS: dict[ModelVersion, str] = {
        ModelVersion.gpt4t0125:'gpt-4-0125-preview',
        ModelVersion.gpt4t1106:'gpt-4-1106-preview',
        ModelVersion.gpt40613:'gpt-4-0613',
        ModelVersion.textembeddings3large:'text-embedding-3-large',
        ModelVersion.textembeddings3small:'text-embedding-3-small',
        ModelVersion.gpt35t0613:'gpt-3.5-turbo-0613',
        ModelVersion.gpt4o0513:'gpt-4o',
        ModelVersion.gpt4t0409:'gpt-4-turbo-2024-04-09',
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

class ApplicationConstants:
    LivenessFile = "/tmp/livenessprobe.txt"