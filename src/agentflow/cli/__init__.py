import upyog as upy

from agentflow.cli.parser import get_args

command = upy.build_cli_command(args_getter=get_args)