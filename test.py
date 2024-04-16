tenantid = "6babcaad-604b-40ac-a9d7-9fd97c0b779f"
clientid = "6e8d915a-460b-499c-a77f-10add633ef38"
kusto_uri = "https://llm-runners.eastus.kusto.windows.net"
kusto_ingestion_uri = "https://ingest-llm-runners.eastus.kusto.windows.net"
kusto_database = "llm-runner"
import adal
authority_url = 'https://login.microsoftonline.com/'+tenantid
context = adal.AuthenticationContext(authority_url)
token = context.acquire_token(kusto_ingestion_uri, kusto_database, clientid)
print(token["accessToken"])