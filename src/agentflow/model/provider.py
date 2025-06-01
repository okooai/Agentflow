import os.path as osp, re, upyog as upy
import httpx

from agentflow.model.base import BaseModel
from agentflow.config import CONST

class Provider(BaseModel):
    def __init__(self,
        namespace=None, name=None,
        auth_type=None, **kwargs
    ):
        super_ = super(BaseModel, self)
        super_.__init__(
            namespace=namespace, name=name,
            auth_type=auth_type, **kwargs
        )

        self._session = httpx.AsyncClient()

    async def achat(self, input=None):
        print(input)

def _resolve_provider_name(provider):
    match = re.match(CONST["AF_NAME_PATTERN_PROVIDER"], provider)

    if not match:
        raise ValueError(f"Invalid provider name format: {provider}")
    
    return match.groupdict()

def get_providers(refresh=False):
    path_target = CONST["AF_CACHE_PROVIDERS"]
    if not osp.exists(path_target) or refresh:
        upy.download_file(CONST["AF_URL_PROVIDERS"], path_target)

    providers = upy.load_json(path_target)
    providers_copy = providers.copy()

    for key, provider in upy.iteritems(providers):
        meta = _resolve_provider_name(key)
        provider = {**provider, **meta}

        if "alias" in provider:
            providers_copy[provider["alias"]] = provider

        providers_copy[key]["name"] = key

    return providers_copy

def provider(name):
    providers = get_providers()
    if name not in providers:
        raise ValueError(f"Provider '{name}' not found.")

    meta = providers[name]

    return Provider(
        namespace = meta["namespace"],
        name      = meta["name"],
        auth_type = meta["auth_type"],
    )