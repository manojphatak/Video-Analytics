import os
import logging
from logging.handlers import RotatingFileHandler
import tempfile

APP_LOGGER_NAME = "video_analytics"

def get_env(envvar,defaultval,vtype):
    try:
        return vtype(os.environ.get(envvar,defaultval))
    except:
        return defaultval


def _get_logger(logname= APP_LOGGER_NAME):
    logger = logging.getLogger(logname)
        
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s:[%(levelname)s]:%(message)s")
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    logsdir = os.environ.get("LOGSDIR",tempfile.gettempdir())
    assert os.path.exists(logsdir), logsdir
    logfile = logname + ".log"
    logfile = os.path.join(logsdir, logfile)

    handler_file = RotatingFileHandler(logfile,maxBytes=1024*1024, backupCount=10)
    handler_file.setLevel(logging.DEBUG)
    handler_file.setFormatter(formatter)
    logger.addHandler(handler_file)
    return logger