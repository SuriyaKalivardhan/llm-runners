import argparse
import logging
import os
import time

from constants import ApplicationConstants

logging.basicConfig(level=logging.INFO)


def check_liveness(threshold: int):
    filename = ApplicationConstants.LivenessFile
    mtime = os.path.getmtime(filename)
    ctime = time.ctime(mtime)
    logging.info(
        f"File {filename=} was last touched at {ctime=} curtime: {time.time()}"
    )
    if time.time() - mtime > threshold:
        logging.info("Fail livenss probe")
        exit(-1)
    else:
        logging.info("Livenss probe success")
        exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=60,
        help="Seconds since the last liveness signal to still be considered healthy.",
    )
    args = parser.parse_args()
    check_liveness(args.threshold)


if __name__ == "__main__":
    main()
