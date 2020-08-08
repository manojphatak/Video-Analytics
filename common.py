import os
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import yaml

def get_env(envvar,defaultval,vtype):
    try:
        return vtype(os.environ.get(envvar,defaultval))
    except:
        return defaultval


def setup_logging():
    with open("logging.yml", 'rt') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
    logging.config.dictConfig(config)
    