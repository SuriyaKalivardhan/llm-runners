az configure -d subscription=ea4faa5b-5e44-4236-91f6-5483d5b17d14 group=llm-runners region=eastus
az login --use-device-code
az account set -s ea4faa5b-5e44-4236-91f6-5483d5b17d14
az group create -n llm-runners -l eastus --tags owner=suriyak SkipAutoDeleteTill=2024-12-31


az container create -n llm-runner-eastus --restart-policy Always --image suriyakalivardhan/llm-runner:v4 --secure-environment-variables OPENAI_API_KEY=abc AZURE_OPENAI_API_KEY=def --command-line "python runner.py -r=EastUS -m gpt4t0125" --assign-identity /subscriptions/ea4faa5b-5e44-4236-91f6-5483d5b17d14/resourcegroups/llm-runners/providers/Microsoft.ManagedIdentity/userAssignedIdentities/llm-runner




az cognitiveservices account create --name eng-latency-frac --location FranceCentral --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0
az cognitiveservices account create --name eng-latency-ause --location AustraliaEast --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0
az cognitiveservices account create --name eng-latency-jape --location JapanEast --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0
az cognitiveservices account create --name eng-latency-inds --location SouthIndia --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar --kind OpenAI --sku s0



az cognitiveservices account deployment create --name eng-latency-wus --deployment-name llm-runner-textemb3-l --model-name text-embedding-3-large --model-version 1 --model-format OpenAI --sku-capacity 240 --sku-name "Standard"
az cognitiveservices account deployment create --name eng-latency-wus --deployment-name llm-runner-textemb3-s --model-name text-embedding-3-small --model-version 1 --model-format OpenAI --sku-capacity 240 --sku-name "Standard"
az cognitiveservices account deployment create --name eng-latency-wus --deployment-name llm-runner-gpt35t-0613 --model-name gpt-35-turbo --model-version 0613 --model-format OpenAI --sku-capacity 240 --sku-name "Standard"


az cognitiveservices account keys list --name eng-latency-frac  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1
az cognitiveservices account keys list --name eng-latency-inds  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1
az cognitiveservices account keys list --name eng-latency-swc  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1
az cognitiveservices account keys list --name eng-latency-uks  --subscription 6a6fff00-4464-4eab-a6b1-0b533c7202e0 -g haakar | jq -r .key1





EastUS: gpt4t0125,gpt35t0613,textembeddings3large,textembeddings3small
FranceCentral: gpt4t1106,gpt35t0613,textembeddings3large
IndiaSouth: gpt4t1106
JapanEast: gpt35t0613
NorthCentralUS: gpt4t0125,gpt35t0613
SwedenCentral: gpt40613,gpt4t1106,textembeddings3large
UKSouth: gpt40613,gpt4t1106,gpt35t0613
WestUS: gpt4t1106
SouthCentralUS: gpt4o0513


