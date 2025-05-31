from __future__ import absolute_import

# imports - module imports
from agentflow.__attr__ import (
    __name__,
    __version__,
    __build__,
    __description__,
    __author__,
)

def get_version():
    version = "%s%s" % (__version__, " (%s)" % __build__ if __build__ else "")
    return version

from agentflow.model.hub import hub, ahub