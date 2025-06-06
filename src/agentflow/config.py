from __future__ import absolute_import

import upyog as upy

from agentflow.__attr__ import __name__ as NAME

PATH = dict()

PATH["BASE"]  = upy.pardir(__file__, 1)
PATH["DATA"]  = upy.join2(PATH["BASE"], "data", path=True)
PATH["CACHE"] = upy.get_config_path(NAME)

CONST = {
    "AF_FILENAME_AGENT":            "Agentfile",
    "AF_FILENAME_ACTION":           "action.yml",
    "AF_FILENAME_ACTION_HANDLER":   "action.py",
    "AF_TAG":                       "latest",
    "AF_URL_REPO_BASE":             "https://github.com",
    "AF_NAMESPACE":                 "okooai-hub",
    "AF_URL_DATA":                  "https://raw.githubusercontent.com/okooai/Agentflow/refs/heads/develop/data",
    "AF_NAME_PATTERN":              r"^(?:(?P<namespace>[\w-]+)/)?(?P<name>[\w-]+)(?::(?P<tag>[\w-]+))?$",
    "AF_NAME_PATTERN_PROVIDER":     r"^(?P<namespace>[\w-]+)/(?P<name>[\w.-]+)$",
    "AF_CACHE_PROVIDERS":           upy.join2(PATH["CACHE"], "providers.json", path=True),
    "AF_ENVVAR_PREFIX":             "AF",
}
CONST["AF_URL_PROVIDERS"] =         upy.join2(CONST["AF_URL_DATA"], "providers.json", path=True)

DEFAULT = {
    "AF_CACHE_HUB":                 upy.join2(PATH["CACHE"], "hub", path=True),
    "AF_PROVIDER":                  "openai",
    "AF_PROVIDER_TIMEOUT":          30,
}