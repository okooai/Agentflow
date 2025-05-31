import upyog as upy

from agentflow.__attr__ import __name__, __version__, __description__, __command__

_DESCRIPTION_JUMBOTRON = """
%s (v %s)

%s
""" % (
    upy.cli_format(__name__, upy.CLI_RED),
    upy.cli_format(__version__, upy.CLI_BOLD),
    upy.cli_format(__description__, upy.CLI_BOLD),
)


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
                }
            },
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
