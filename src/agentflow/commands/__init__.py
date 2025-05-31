# imports - compatibility imports
from __future__ import absolute_import

import upyog as upy

from agentflow.commands.util import cli_format
from agentflow import cli
from agentflow.__attr__ import __name__

logger = upy.get_logger(level=upy.LOG_DEBUG)

ARGUMENTS = dict(
    jobs            = 1,
    check           = False,
    interactive     = False,
    yes             = False,
    no_cache        = False,
    no_color        = True,
    output          = None,
    ignore_error    = False,
    force           = False,
    verbose         = False,
)


@cli.command
def command(**ARGUMENTS):
    try:
        return _command(**ARGUMENTS)
    except Exception as e:
        if not isinstance(e, upy.DependencyNotFoundError):
            cli.echo()

            upy.pretty_print_error(e)

            cli.echo(
                cli_format(
                    """\
An error occured while performing the above command. This could be an issue with
"agentflow". Kindly post an issue at https://github.com/achillesrasquinha/agentflow/issues""",
                    cli.RED,
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


def _command(*args, **kwargs):
    a = to_params(kwargs)

    if not a.verbose:
        logger.setLevel(upy.LOG_NOTSET)

    logger.info(f"Environment: {upy.environment()}")
    logger.info(f"Arguments Passed: {locals()}")

    file_ = a.output

    if file_:
        logger.info(f"Writing to output file {file_}...")
        upy.touch(file_)

    logger.info(f"Using {a.jobs} Jobs...")
