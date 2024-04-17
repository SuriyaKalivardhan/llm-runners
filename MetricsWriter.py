from structure import Environment, Region, RequestInput, ResponseOutput, ServiceProvider
from Utilities import Utilities
from io import TextIOWrapper

class MetricsWriter:
    def __init__(self, environment:Environment, region:Region) -> None:
        self.file:TextIOWrapper = Utilities.create_and_get_new_file()
        self.kustclient = None
        if environment == Environment.Cloud:
            pass

    def writeMetrics(self, provider:ServiceProvider, request:RequestInput, response:ResponseOutput):
        self.file.write(Utilities.log(provider, request, response))
        self.file.flush()

    def close(self):
        self.file.close()