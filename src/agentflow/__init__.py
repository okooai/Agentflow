from __future__ import absolute_import

import upyog as upy
from upyog import (
    arequest
)

# imports - module imports
from agentflow.__attr__ import (
    __name__,
    __version__,
    __build__,
    __description__,
    __author__,
)

def get_version():
    return upy.build_version_str(__version__, __build__)

from agentflow.model.hub import hub, ahub
from agentflow.environ   import param