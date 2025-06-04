import upyog as upy

from agentflow.cli.parser import get_args

def command(fn):
    args   = get_args()

    params = upy.get_function_arguments(fn)
    params = upy.merge_dict(params, args)

    def wrapper(*args, **kwargs):
        return fn(**params)

    return wrapper