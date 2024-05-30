from structure import Region, ModelVersion, Environment
from Inferencer import Inferencer
from Utilities import Utilities
import argparse
import logging
import sys
from typing import List
logging.basicConfig(level=logging.INFO)

def main(environment:Environment, region:Region, model_versions:List[ModelVersion], rpm:int, num_prompts:int, num_samples:int):
    logging.info(f"{environment=} {region=} {model_versions=} {rpm=} {num_prompts=} {num_samples=}")
    candidates = Utilities.construct_candidates(rpm, num_prompts, num_samples)
    logging.info(candidates)
    inf:Inferencer  = Inferencer(environment, region)
    inf.score(candidates, model_versions)
    inf.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', type=str, default=Environment.Dev.name)
    parser.add_argument('-r', '--region', type=str, default=Region.SouthCentralUS.name)
    parser.add_argument('-m', '--model_versions', type=str, default=ModelVersion.gpt4o0513.name)
    parser.add_argument('-rpm', '--request_per_minute', type=int, default=2)
    parser.add_argument('-np', '--num_prompts', type=int, default=sys.maxsize)
    parser.add_argument('-ns', '--num_samples', type=int, default=sys.maxsize)
    args = parser.parse_args()
    while True:
        main(Environment[args.environment], Region[args.region], ModelVersion.as_list_from_str(args.model_versions), args.request_per_minute, args.num_prompts, args.num_samples)