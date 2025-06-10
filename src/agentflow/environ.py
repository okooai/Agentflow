import upyog as upy

from agentflow.config import CONST

def param(name):
    return upy.get_env_param(name,
        envvar = upy.getenvvar("PARAMETERS", prefix = \
            CONST['AF_ENVVAR_PREFIX_ACTION']
        ),
    )