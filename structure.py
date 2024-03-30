from enum import Enum

class ServiceProvider(Enum):
    OpenAI = 1
    AzureOpenAI = 2

class ModelVersion(Enum):
    gpt4t0125 = 1

class Region(Enum):
    EastUS = 1