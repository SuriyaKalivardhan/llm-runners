from enum import Enum
from dataclasses import dataclass

class ServiceProvider(Enum):
    OpenAI = 1
    AzureOpenAI = 2

class ModelVersion(Enum):
    gpt4t0125 = 1
    gpt4t1106 = 2

    def as_list():
        [e.name for e in Region]

class Region(Enum):
    Global = 1
    EastUS = 2
    NorthCentralUS  = 3
    SouthCentralUS = 4
    WestUS = 5
    SwedenCentral = 6

    def as_list():
        [e.name for e in Region]

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
        [e.name for e in Environment]