az configure -d subscription=ea4faa5b-5e44-4236-91f6-5483d5b17d14 group=llm-runners region=eastus
az login --use-device-code
az account set -s ea4faa5b-5e44-4236-91f6-5483d5b17d14
az group create -n llm-runners -l eastus --tags owner=suriyak SkipAutoDeleteTill=2024-12-31


az container create -n llm-runner-eastus --restart-policy Always --image suriyakalivardhan/llm-runner:v4 --secure-environment-variables OPENAI_API_KEY=abc AZURE_OPENAI_API_KEY=def --command-line "python runner.py -r=EastUS -m gpt4t0125" --assign-identity /subscriptions/ea4faa5b-5e44-4236-91f6-5483d5b17d14/resourcegroups/llm-runners/providers/Microsoft.ManagedIdentity/userAssignedIdentities/llm-runner