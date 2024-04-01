from constants import AzureOpenAIConstansts
from openai import OpenAI, AzureOpenAI
from WikiClient import WikiClient
from structure import ServiceProvider, Region, ModelVersion, RequestInput
from InputProcessor import InputProcessor
from StreamingRequestHandler import StreamingRequestHandler
import os

class Inferencer:
    def __init__(self, azure_region:Region):
        self.streaming_handlers:dict[ServiceProvider, StreamingRequestHandler] = {
            # ServiceProvider.OpenAI:StreamingRequestHandler(ServiceProvider.OpenAI),
            ServiceProvider.AzureOpenAI:StreamingRequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        }
        self.non_streaming_handlers = {} #TODO: Enable non-streaming handlers



    def score(self, requests:list[RequestInput]):
        for request in requests:
            if request.stream:
                for handler in self.streaming_handlers.values():
                    handler.score(request)
