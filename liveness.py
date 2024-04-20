import logging, os, time
logging.basicConfig(level=logging.INFO)

def check_liveness():
    filename = "/tmp/livenessprobe.py"
    mtime = os.path.getmtime(filename)
    ctime = time.ctime(mtime)
    logging.info(f"File {filename=} was last touched at {ctime=} curtime: {time.time()}")
    if time.time()-mtime > 3600:
        logging.info("Fail livenss probe")
        exit(-1)
    else:
        logging.info("Livenss probe success")
        exit(0)

if __name__ == "__main__":
    check_liveness()