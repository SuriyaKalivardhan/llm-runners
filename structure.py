from enum import Enum
from dataclasses import dataclass

class ServiceProvider(Enum):
    OpenAI = 1
    AzureOpenAI = 2

class ModelVersion(Enum):
    gpt4t0125 = 1
    gpt4t1106 = 2

class Region(Enum):
    Global = 1
    EastUS = 2
    NorthCentralUS  = 3
    SouthCentralUS = 4
    WestUS = 5
    SwedenCentral = 6

@dataclass
class RequestInput:
    model_version:ModelVersion
    Prompt:str
    max_token:int
    stream:bool
    expected_samples:str

    def __repr__(self) -> str:
        return f"{self.model_version.name}\t{self.Prompt}\t{self.max_token}\t{self.stream}\t{self.expected_samples}"
    
    def getStr(self) -> str:
        return f"{self.model_version.name}\t{self.max_token}"

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

    def __repr__(self) -> str:
        return f"{self.samples}\t{self.time_to_first_token}\t{self.time_between_tokens}\t{self.time_to_last_token}\t{self.finish_reason}\t{self.n_prompts}\t{self.n_gen}\t{self.edit_distance}"
    
    def getStr(self) -> str:
        return f"{self.time_to_first_token}\t{self.time_between_tokens[0]}\t{self.time_to_last_token}\t{self.finish_reason}\t{self.n_prompts}\t{self.n_gen}"