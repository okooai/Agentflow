
from __future__ import absolute_import


try:
    import os

    if os.environ.get("AGENTFLOW_GEVENT_PATCH"):
        from gevent import monkey
        monkey.patch_all(threaded = False, select = False)
except ImportError:
    pass

# imports - module imports
from agentflow.__attr__ import (
    __name__,
    __version__,
    __build__,

    __description__,

    __author__
)
from agentflow.config  import PATH

from upyog.cache       import Cache
from upyog.config      import Settings
from upyog.util.jobs   import run_all as run_all_jobs, run_job
from upyog import log

logger   = log.get_logger(__name__)

cache = Cache(dirname = __name__)
cache.create()

settings = Settings()


def get_version_str():
    version = "%s%s" % (__version__, " (%s)" % __build__ if __build__ else "")
    return version

from agentflow.model.hub import (
    hub,
    ahub
)