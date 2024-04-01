from WikiClient import WikiClient
from structure import Region, ModelVersion
from InputProcessor import InputProcessor
from Inferencer import Inferencer

if __name__ == "__main__":
    ip:InputProcessor = InputProcessor(WikiClient())
    result = ip.getInput(ModelVersion.gpt4t0125, total_len=8, stream=None, min_prompt_len=6)
    inp = []
    inp.append(result[len(result)-1])
    inp[0].max_token = 10
    print(inp)
    inf:Inferencer  = Inferencer(Region.EastUS)
    output = inf.score(inp)
    print(output)