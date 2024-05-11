from enum import Enum
from dataclasses import dataclass

class ServiceProvider(Enum):
    OpenAI = 1
    AzureOpenAI = 2

class ModelVersion(Enum):
    gpt4t0125 = 1
    gpt4t1106 = 2
    gpt40613 = 3
    textembeddings3large = 4,
    textembeddings3small = 5,
    gpt35t0613 = 6

    def as_list():
        return [e.name for e in ModelVersion]

    def as_list_from_str(input:str):
        list_str = str.split(input,',')
        return [ModelVersion[item] for item in list_str]
    
    def embeddings_list():
        return [ModelVersion.textembeddings3large, ModelVersion.textembeddings3small]

class Region(Enum):
    Global = 1
    EastUS = 2
    NorthCentralUS  = 3
    SouthCentralUS = 4
    WestUS = 5
    SwedenCentral = 6
    UKSouth = 7
    FranceCentral = 8
    AustraliaEast = 9
    JapanEast = 10
    SouthIndia = 11

    def as_list():
        return [e.name for e in Region]

@dataclass
class RequestInput:
    model_version:ModelVersion
    Prompt:str
    max_token:int
    stream:bool
    expected_samples:str

@dataclass
class ResponseOutput:
    samples: str
    time_to_first_token:float
    time_between_tokens: list[float]
    mean_time_between_tokens:float
    time_to_last_token: float
    finish_reason:str
    n_prompts:int
    n_gen:int
    edit_distance:int

class Environment(Enum):
    Dev = 1
    Cloud = 2

    def as_list():
        return [e.name for e in Environment]