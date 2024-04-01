from structure import ServiceProvider, Region, RequestInput
from StreamingRequestHandler import StreamingRequestHandler
from RequestHandler import RequestHandler
from io import TextIOWrapper
from Utilities import Utilities

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
        self.file:TextIOWrapper = Utilities.create_and_get_new_file()

    def score(self, requests:list[RequestInput]):
        for request in requests:
            if request.stream:
                for handler in self.streaming_handlers:
                    response = handler.score(request)
                    self.file.write(Utilities.log(handler.provider, request, response))
            else:
                for handler in self.non_streaming_handlers:
                    response = handler.score(request)
                    self.file.write(Utilities.log(handler.provider, request, response))
            self.file.flush()

    def close(self):
        self.file.close()