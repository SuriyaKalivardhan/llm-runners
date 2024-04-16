tenantid = "6babcaad-604b-40ac-a9d7-9fd97c0b779f"
clientid = "6e8d915a-460b-499c-a77f-10add633ef38"
kusto_uri = "https://llm-runners.eastus.kusto.windows.net"
kusto_ingestion_uri = "https://ingest-llm-runners.eastus.kusto.windows.net"
kusto_database = "llm-runner"
import requests

def fetch_token_from_imds(resource_url='https://management.azure.com/'):
    imds_url = 'http://169.254.169.254/metadata/identity/oauth2/token'

    params = {
        'api-version': '2018-02-01',
        'resource': resource_url 
    }

    headers = {
        'Metadata': 'true'
    }

    try:
        response = requests.get(imds_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        access_token = data['access_token']
        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch token from IMDS: {e}")
        return None

if __name__ == "__main__":
    resource = 'https://management.azure.com/'
    token = fetch_token_from_imds(resource)
    print("Access Token:", token)


### Explanation
- **URL and Endpoint**: The IMDS endpoint used is `http://169.254.169.254/metadata/identity/oauth2/token`. This URL is standard for accessing the IMDS.
- **Parameters**:
  - `api-version`: Specifies the API version to use; "2018-02-01" is a common version.
  - `resource`: Specify the Azure resource URL you want the token for. In this case, it’s set to manage Azure resources (`https://management.azure.com/`).
- **Headers**: The header `Metadata: true` is essential to make requests to the IMDS to indicate that the call is made from within an Azure VM.

This script is ready to be used within an Azure VM that has been assigned a Managed Identity and provided appropriate access roles to fetch tokens for the specified resources. It's a straightforward method to obtain authentication credentials without hardcoding them in your applications.