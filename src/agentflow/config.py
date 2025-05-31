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
    "FILE_EXT": ".af",
    "URL_DATA": "https://raw.githubusercontent.com/achillesrasquinha/Agentflow/refs/heads/develop/data"
}
CONST["URL_PROVIDERS"] = upy.join2(CONST["URL_DATA"], "providers.json", path=True)

DEFAULT = {
    "URL_HUB":       upy.join2(CONST["URL_DATA"], "hub", path=True),
    "CACHE_HUB":     upy.join2(PATH["CACHE"], "hub", path=True),
    "PROVIDER":      "openai/gpt-4.1"
}