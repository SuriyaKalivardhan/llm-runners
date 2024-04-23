az configure -d subscription=ea4faa5b-5e44-4236-91f6-5483d5b17d14 group=llm-runners region=eastus
az login --use-device-code
az account set -s ea4faa5b-5e44-4236-91f6-5483d5b17d14
az group create -n llm-runners -l eastus --tags owner=suriyak SkipAutoDeleteTill=2024-12-31


az container create -n llm-runner-eastus --restart-policy Always --image suriyakalivardhan/llm-runner:v4 --secure-environment-variables OPENAI_API_KEY=abc AZURE_OPENAI_API_KEY=def --command-line "python runner.py -r=EastUS -m gpt4t0125" --assign-identity /subscriptions/ea4faa5b-5e44-4236-91f6-5483d5b17d14/resourcegroups/llm-runners/providers/Microsoft.ManagedIdentity/userAssignedIdentities/llm-runner




az cognitiveservices account create --name eng-latency-frac --location FranceCentral --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0
az cognitiveservices account create --name eng-latency-ause --location AustraliaEast --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0
az cognitiveservices account create --name eng-latency-jape --location JapanEast --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0
az cognitiveservices account create --name eng-latency-inds --location SouthIndia --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0



az cognitiveservices account keys list --name eng-latency-frac  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1
az cognitiveservices account keys list --name eng-latency-inds  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1
az cognitiveservices account keys list --name eng-latency-swc  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1
az cognitiveservices account keys list --name eng-latency-uks  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1




az cognitiveservices account deployment create --name eng-latency-frac --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --deployment-name llm-runner-gpt4t-1106 --model-name gpt-4 --model-version "1106-preview" --sku-name "Standard"

