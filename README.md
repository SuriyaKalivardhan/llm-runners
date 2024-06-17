# LLM Runners  (compares performance of various hosting providers)


## Usage

python runner.py \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-r/--region=[Region]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-m/--model_version=[ModelVersion]   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-rpm-request_per_minute=[RequestsPerMin]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -ns/--num_prompts=[PromptSize]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -ns/--num_samples[SamplingSize]  
Example:  
  > python runner.py -r=EastUS -m=gpt4t0125 -rpm=2 -ns=1000 -ns=200

Defaults:  
> Region=EastUS  
ModelVersion=gpt4t0125  
Unspecified num_samples and num_prompts will be uniform distribution from 100 to 5000 tokens


### Supported providers:
    - Azure OpenAI
    - OpenAI

Current supported Regions:

Region|Onboarded Date  
:-:|:-:
EastUS|4/16/2024
NorthCentralUS|4/17/2024
WestUS|4/17/2024
USSouth|4/18/2024
SwedenCentral|4/19/2024

### To onboard a new region:
1. Add the new region [here](structure.py#L23)
2. Push the changes to docker.io/suriyakalivardhan/llm-runners:v15 (ToDo: Automate this)
2. Deploy AzureOpenAI account in the regions (ToDo: Add script)
3. Deploy the runners `az container create -f acidep.yml`

### Access to metrics:
- Owners: Sid, Pankaj, Halit and Suriya
- For access to dashboard - please provide your ObjectId to one of the owners.



### Latest update (5/11) ###

Region|ModelVersion
:-:|:-
EastUS|gpt4t0125,gpt35t0613,textembeddings3large,textembeddings3small
FranceCentral|gpt4t1106,gpt35t0613,textembeddings3large
IndiaSouth|gpt4t1106
JapanEast|gpt35t0613
NorthCentralUS|gpt4t0125,gpt35t0613
SwedenCentral|gpt40613,gpt4t1106,textembeddings3large,gpt4t0409
UKSouth|gpt40613,gpt4t1106,gpt35t0613
WestUS|gpt4t1106
SouthCentralUS|gpt4o0513
EastUS2|gpt4t0409



