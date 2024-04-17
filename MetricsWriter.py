from structure import Environment, Region, RequestInput, ResponseOutput, ServiceProvider
from Utilities import Utilities
from constants import KustoConstants
from io import TextIOWrapper
from datetime import datetime
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties
from azure.kusto.data import KustoConnectionStringBuilder, DataFormat
import requests, logging, io, threading
logging.basicConfig(level=logging.INFO)

class MetricsWriter:
    def __init__(self, environment:Environment, region:Region) -> None:        
        self.region = region
        self.file:TextIOWrapper = Utilities.create_and_get_new_file()
        self.kustoClient = None
        self.INGESTION_PROPERTIES = None
        if environment == Environment.Cloud:
            self.INGESTION_PROPERTIES = IngestionProperties(database=KustoConstants.KUSTO_DATABASE, table=KustoConstants.KUSTO_TABLE, data_format=DataFormat.TSV,
                ingestion_mapping_reference=KustoConstants.KUSTO_MAPPING_REFERENCE, additional_properties={'ignoreFirstRecord': 'false'})
            self.refresh_kusto_client()

    def writeMetrics(self, requestTime:datetime, provider:ServiceProvider, request:RequestInput, response:ResponseOutput):        
        requestTime_str = requestTime.strftime("%Y-%m-%d %H:%M:%S.%f")
        logline_str = f"{requestTime_str}\t{self.region}\t{request.model_version.name}\t{provider.name}\t{response.n_prompts}\t{response.n_gen}\t{request.stream}\t{response.finish_reason}\t{response.time_to_first_token:.4f}\t{response.mean_time_between_tokens:.4f}\t{response.time_to_last_token:.4f}"
        
        self.file.write(logline_str)
        self.file.flush()
        
        if self.kustoClient is not None:
            self.kustoClient.ingest_from_stream(io.StringIO(logline_str), ingestion_properties=self.INGESTION_PROPERTIES)
        
    def refresh_kusto_client(self):        
        threading.Timer(3600.0, self.refresh_kusto_client).start()
        params = {
            'api-version': '2018-02-01',
            'resource': KustoConstants.KUSTO_INGEST_URI
        }

        headers = {
            'Metadata': 'true'
        }

        try:
            response = requests.get(KustoConstants.IMDS_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            token = data['access_token']
            self.kustoClient = QueuedIngestClient(KustoConnectionStringBuilder.with_aad_user_token_authentication(KustoConstants.KUSTO_INGEST_URI, token))
        except requests.exceptions.RequestException as e:
            logging.critical(f"Failed to fetch token from IMDS: {e}")

    def close(self):
        self.file.close()