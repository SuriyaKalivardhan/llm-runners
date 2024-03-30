from structure import ModelVersion, Region

class AzureOpenAIConstansts:
    api_version:str="2024-02-01",
    api_key="AZURE_OPENAI_API_KEY"
    model_deployments = {
        ModelVersion.gpt4t0125:'llm-runner-gpt4t-0125'
    }
    endpoints = {
        Region.EastUS:"https://eng-latency.openai.azure.com/"
    }

class OpenAIContants:
    model_deployments = {
        ModelVersion.gpt4t0125:'gpt-4-0125-preview'
    }