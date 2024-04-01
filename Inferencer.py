from structure import ServiceProvider, Region, RequestInput
from StreamingRequestHandler import StreamingRequestHandler
from RequestHandler import RequestHandler

class Inferencer:
    def __init__(self, azure_region:Region):
        self.streaming_handlers = [
            StreamingRequestHandler(ServiceProvider.OpenAI),
            StreamingRequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
        self.non_streaming_handlers = [
            RequestHandler(ServiceProvider.OpenAI),
            RequestHandler(ServiceProvider.AzureOpenAI, azure_region),
        ]
    def score(self, requests:list[RequestInput]):
        for request in requests:
            if request.stream:
                for handler in self.streaming_handlers:
                    handler.score(request)
            else:
                for handler in self.non_streaming_handlers:
                    handler.score(request)
