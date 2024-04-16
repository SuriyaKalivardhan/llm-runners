tenantid = "6babcaad-604b-40ac-a9d7-9fd97c0b779f"
clientid = "6e8d915a-460b-499c-a77f-10add633ef38"
kusto_uri = "https://llm-runners.eastus.kusto.windows.net"
kusto_ingestion_uri = "https://ingest-llm-runners.eastus.kusto.windows.net"
kusto_database = "llm-runner"
import requests

imds_url = 'http://169.254.169.254/metadata/identity/oauth2/token'

params = {
    'api-version': '2018-02-01',
    'resource': kusto_ingestion_uri 
}

headers = {
    'Metadata': 'true'
}

try:
    response = requests.get(imds_url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    access_token = data['access_token']
    print(access_token)
    print(data)

    import io
    import time
    from datetime import datetime, timezone
    from azure.kusto.data import DataFormat
    from azure.kusto.ingest import QueuedIngestClient, IngestionProperties, FileDescriptor, BlobDescriptor, ReportLevel, ReportMethod
    from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
    from azure.kusto.data.exceptions import KustoServiceError
    from azure.kusto.data.helpers import dataframe_from_result_table
    KCSB_INGEST   = KustoConnectionStringBuilder.with_aad_user_token_authentication(kusto_ingestion_uri, access_token)
    INGESTION_CLIENT = QueuedIngestClient(KCSB_INGEST)    
    n_prompt= 123
    n_gen=456
    ttft=0.0
    mean_tbt=0.0
    ttlt=0.0
    Region='TestRegion'
    pbool = True
    ModelVersion='TestModelVersion'
    for _ in range(1000):
        p_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        provider = 'openai' if pbool else 'azure'
        content = io.StringIO(f"{p_time}\t{Region}\t{ModelVersion}\t{provider}\t{n_prompt}\t{n_gen}\t{ttft:.4f}\t{mean_tbt:.4f}\t{ttlt:.4f}")
        print(f"Ingesting {content.getvalue()}")
        INGESTION_PROPERTIES = IngestionProperties(database=kusto_database, table="InferencingEvents", data_format=DataFormat.TSV,
                                           ingestion_mapping_reference="InferencingEvents_TSV_Mapping", additional_properties={'ignoreFirstRecord': 'false'})

        INGESTION_CLIENT.ingest_from_stream(content, ingestion_properties=INGESTION_PROPERTIES)
        time.sleep(3)
        n_prompt +=1
        n_gen +=1
        ttft +=0.1
        mean_tbt += 0.1
        ttlt += 0.1
        pbool = not pbool


except requests.exceptions.RequestException as e:
    print(f"Failed to fetch token from IMDS: {e}")