from __future__ import absolute_import

import upyog as upy

from agentflow.__attr__ import (
    __name__ as NAME
)

PATH = dict()

PATH["BASE"]  = upy.pardir(__file__, 1)
PATH["DATA"]  = upy.join2(PATH["BASE"], "data", path=True)
PATH["CACHE"] = upy.get_config_path(NAME)

CONST = {
    "AF_FILE_EXT": ".af",
}

DEFAULT = {
    "AF_URL_HUB": "https://raw.githubusercontent.com/achillesrasquinha/Agentflow/refs/heads/develop/data/hub",
    "AF_CACHE_HUB": upy.join2(PATH["CACHE"], "hub", path=True),
    "AF_PROVIDER": "openai/gpt-4.1"
}