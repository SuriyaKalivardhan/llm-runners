az configure -d subscription=ea4faa5b-5e44-4236-91f6-5483d5b17d14 group=llm-runners region=eastus
az login --use-device-code
az account set -s ea4faa5b-5e44-4236-91f6-5483d5b17d14
az group create -n llm-runners -l eastus --tags owner=suriyak SkipAutoDeleteTill=2024-12-31
az container create -n testacr3 --restart-policy Always --image suriyakalivardhan/testimage:v1 --secure-environment-variables abcd=xyz  --command-line "python myrunner.py -n=60"