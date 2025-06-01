import upyog as upy

from agentflow.cli.parser import get_args

def cli_format(string, type_):
    args = get_args(as_dict=False)

    if hasattr(args, "no_color") and not args.no_color:
        string = upy.cli_format(string, type_)

    return string