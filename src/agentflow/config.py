from __future__ import absolute_import

import upyog as upy

from agentflow.__attr__ import __name__ as NAME

PATH = dict()

PATH["BASE"] = upy.pardir(__file__, 1)
PATH["DATA"] = upy.join2(PATH["BASE"], "data", path=True)
PATH["CACHE"] = upy.get_config_path(NAME)

CONST = {
    "AF_FILENAME":          "Agentfile",
    "AF_TAG":               "latest",
    "AF_URL_DATA":          "https://raw.githubusercontent.com/achillesrasquinha/Agentflow/refs/heads/develop/data",
    "AF_HUB_NAME_PATTERN":  r"^(?:(?P<namespace>[\w-]+)/)?(?P<name>[\w-]+)(?::(?P<tag>[\w-]+))?$",
}
CONST["AF_URL_PROVIDERS"] = upy.join2(CONST["AF_URL_DATA"], "providers.json", path=True)

DEFAULT = {
    "AF_URL_HUB":   upy.join2(CONST["AF_URL_DATA"], "hub", path=True),
    "AF_CACHE_HUB": upy.join2(PATH["CACHE"], "hub", path=True),
    "AF_PROVIDER":  "openai",
}
