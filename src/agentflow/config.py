from __future__ import absolute_import

import upyog as upy

from agentflow.__attr__ import __name__ as NAME

PATH = dict()

PATH["BASE"] = upy.pardir(__file__, 1)
PATH["DATA"] = upy.join2(PATH["BASE"], "data", path=True)
PATH["CACHE"] = upy.get_config_path(NAME)

CONST = {
    "AF_FILENAME":              "Agentfile",
    "AF_TAG":                   "latest",
    "AF_URL_REPO_BASE":         "https://github.com",
    "AF_NAMESPACE":             "okooai",
    "AF_URL_DATA":              "https://raw.githubusercontent.com/okooai/Agentflow/refs/heads/develop/data",
    "AF_NAME_PATTERN_AGENT":    r"^(?:(?P<namespace>[\w-]+)/)?(?P<name>[\w-]+)(?::(?P<tag>[\w-]+))?$",
    "AF_NAME_PATTERN_PROVIDER": r"^(?P<namespace>[\w-]+)/(?P<name>[\w.-]+)$",
    "AF_CACHE_PROVIDERS":       upy.join2(PATH["CACHE"], "providers.json", path=True)
}
CONST["AF_URL_PROVIDERS"] = upy.join2(CONST["AF_URL_DATA"], "providers.json", path=True)

DEFAULT = {
    "AF_CACHE_HUB": upy.join2(PATH["CACHE"], "hub", path=True),
    "AF_PROVIDER":  "openai",
}
