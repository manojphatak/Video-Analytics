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
    currdir = os.path.dirname(__file__)
    log_config= os.path.join(currdir, "logging.yml")
    with open(log_config, 'rt') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
    logging.config.dictConfig(config)
    