import logging
import time

def init_logger(logname):
    #logging.basicConfig()
    logging.Formatter.converter = time.localtime
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s:[%(levelname)s]:%(message)s"))
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger