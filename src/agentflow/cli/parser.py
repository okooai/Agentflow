import upyog as upy

from agentflow.__attr__ import (
    __label__,
    __version__,
    __description__,
    __command__
)
from agentflow import get_version

_DESCRIPTION_JUMBOTRON = f"""
{upy.cli_format(__label__,       upy.CLI_BLUE)} v{upy.cli_format(get_version(),   upy.CLI_BOLD)}

{upy.cli_format(__description__, upy.CLI_BOLD)}
"""

def get_parser():
    parser = upy.get_base_parser(__command__, _DESCRIPTION_JUMBOTRON)
    upy.add_sub_commands(parser, {
        "get": {
            "help": "Fetch an Agent from the Hub",
            "args": {
                "name": {
                    "help": "Agent Name(s)",
                    "type": str,
                    "nargs": "+",
                }
            }
        },
        "list": {
            "help": "List all locally available Agents"
        },
        "run": {
            "help": "Run an Agent",
            "args": {
                "name": {
                    "help": "Name of the Agent to run",
                    "type": str
                },
                "input": {
                    "help": "Input to the Agent",
                    "type": str,
                    "nargs": "?",
                }
            },
            "kwargs": {
                "remove": {
                    "flag": ("-rm", "--remove"),
                    "help": "Delete the session after running",
                    "action": "store_true",
                },
                "interactive": {
                    "flag": ("-it", "--interactive"),
                    "help": "Run the Agent in interactive mode",
                    "action": "store_true",
                },
                "stream": {
                    "flag": "--stream",
                    "help": "Stream the Agent's response",
                    "action": "store_true",
                }
            }
        },
    })
    return parser

def get_args(args=None, known=True, as_dict=True):
    parser = get_parser()

    if known:
        args, _ = parser.parse_known_args(args)
    else:
        args = parser.parse_args(args)

    if as_dict:
        args = args.__dict__

    return args
