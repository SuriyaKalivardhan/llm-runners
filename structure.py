from enum import Enum
from dataclasses import dataclass

class ServiceProvider(Enum):
    OpenAI = 1
    AzureOpenAI = 2

class ModelVersion(Enum):
    gpt4t0125 = 1

class Region(Enum):
    Global = 1
    EastUS = 2

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
    time_to_last_token: float
    finish_reason:str
    n_prompts:int
    n_gen:int
    edit_distance:int