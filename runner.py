from WikiClient import WikiClient
from structure import Region, ModelVersion
from InputProcessor import InputProcessor
from Inferencer import Inferencer
from Utilities import Utilities

if __name__ == "__main__":
    #ip:InputProcessor = InputProcessor(WikiClient())
    #requests = ip.getInput(ModelVersion.gpt4t0125, total_len=4000, stream=True, min_prompt_len=100, min_gen_len=10)
    #inf:Inferencer  = Inferencer(Region.SwedenCentral)
    #inf.score(requests)
    inputs = Utilities.get_all_possible_input_sizes(10000, 500, 8000, 50, 1000)
    print(inputs)
    region = Region.EastUS
    model_version = ModelVersion.gpt4t0125
    region = Region.NorthCentralUS
    model_version = ModelVersion.gpt4t0125
    region = Region.WestUS
    model_version = ModelVersion.gpt4t1106
    inf:Inferencer  = Inferencer(region)
    inf.score_v1(inputs, model_version,True)
    inf.close()