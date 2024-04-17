from structure import Region, ModelVersion, Environment
from Inferencer import Inferencer
from Utilities import Utilities
import argparse
import logging
logging.basicConfig(level=logging.INFO)

def main(environment:Environment, region:Region, model_version:ModelVersion):
    candidates = Utilities.get_uniform_distributed_candidates()
    logging.info(candidates)
    inf:Inferencer  = Inferencer(environment, region)
    inf.score_stream(candidates, model_version)
    inf.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', type=str, default=Environment.Cloud.name, choices=Environment.as_list())    
    parser.add_argument('-r', '--region', type=str, default=Region.EastUS.name, choices=Region.as_list())    
    parser.add_argument('-m', '--model_version', type=str, default=ModelVersion.gpt4t0125.name, choices=ModelVersion.as_list())
    args = parser.parse_args()
    main(Environment[args.environment], Region[args.region], ModelVersion[args.model_version])