# imports - compatibility imports
from __future__ import absolute_import

import upyog as upy

from agentflow.commands.util import cli_format
from agentflow.cli           import command as cli_command
from agentflow.__attr__      import __name__

logger = upy.get_logger(level=upy.LOG_DEBUG)

ARGUMENTS = dict(
    jobs            = 1,
    check           = False,
    interactive     = False,
    yes             = False,
    no_cache        = False,
    no_color        = True,
    output          = None,
    ignore_errors   = False,
    force           = False,
    verbose         = False,

    name            = None,
)

@cli_command
def command(**ARGUMENTS):
    try:
        return upy.run_async(_command(**ARGUMENTS))
    except Exception as e:
        if not isinstance(e, upy.DependencyNotFoundError):
            upy.echo()

            upy.pretty_print_error(e)

            upy.echo(
                cli_format(
                    """\
An error occured while performing the above command. This could be an issue with
"agentflow". Kindly post an issue at https://github.com/achillesrasquinha/agentflow/issues""",
                    upy.CLI_RED,
                )
            )
        else:
            raise e

def to_params(kwargs):
    class O(object):
        pass

    params = O()

    kwargs = upy.merge_dict(ARGUMENTS, kwargs)

    for k, v in upy.iteritems(kwargs):
        k = k.replace("-", "_")
        setattr(params, k, v)

    return params

async def _command(*args, **kwargs):
    a = to_params(kwargs)

    if not a.verbose:
        logger.setLevel(upy.LOG_NOTSET)

    file_ = a.output

    if file_:
        upy.touch(file_)

    from agentflow.model.hub import ahub

    if   a.command_1 == "get":
        await ahub(*a.name, fail=not a.ignore_errors, verbose=a.verbose)
    elif a.command_1 == "run":
        agent    = await ahub(a.name, fail=not a.ignore_errors, verbose=a.verbose)
        if a.input or a.interactive:
            response = await agent.arun(
                input=a.input, interactive=a.interactive, stream=a.stream)

            if not a.interactive:
                upy.echo(cli_format(response, upy.CLI_BLUE))