from WikiClient import WikiClient
from structure import Region, ModelVersion
from InputProcessor import InputProcessor
from Inferencer import Inferencer
from Utilities import Utilities

if __name__ == "__main__":
    #ip:InputProcessor = InputProcessor(WikiClient())
    #requests = ip.getInput(ModelVersion.gpt4t0125, total_len=4000, stream=True, min_prompt_len=100, min_gen_len=10)
    inputs = Utilities.get_all_possible_input_sizes(4000, 100, 2000, 100, 2000)
    print(inputs)
    inf:Inferencer  = Inferencer(Region.EastUS)
    #inf:Inferencer  = Inferencer(Region.SwedenCentral)
    #inf.score(requests)
    inf.score_v1(inputs, ModelVersion.gpt4t0125,True)
    inf.close()