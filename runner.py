from WikiClient import WikiClient
from structure import Region, ModelVersion
from InputProcessor import InputProcessor
from Inferencer import Inferencer

if __name__ == "__main__":
    ip:InputProcessor = InputProcessor(WikiClient())
    requests = ip.getInput(ModelVersion.gpt4t0125, total_len=4000, stream=True, min_prompt_len=100, min_gen_len=10)
    inf:Inferencer  = Inferencer(Region.EastUS)
    inf.score(requests)
    inf.close()