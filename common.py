import os

def get_env(envvar,defaultval,vtype):
    try:
        return vtype(os.environ.get(envvar,defaultval))
    except:
        return defaultval