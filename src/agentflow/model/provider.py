import os.path as osp, re, upyog as upy
import httpx

from agentflow.model.base import BaseModel
from agentflow.config import CONST, DEFAULT

class Provider(BaseModel):
    def __init__(self,
        namespace=None, name=None, url=None, endpoints=None,
        auth_type=None, **kwargs
    ):
        super_ = super(BaseModel, self)
        super_.__init__(
            namespace=namespace, name=name, url=url, endpoints=endpoints,
            auth_type=auth_type, **kwargs
        )

        self._session = httpx.AsyncClient()

    def _build_request_url(self, type_):
        endpoint = self.endpoints[type_]
        url      = f"{self.url}{endpoint}"
        return url
    
    def _build_envvar(self, key):
        return upy.getenvvar(f"{upy.upper(self.namespace)}_{upy.upper(key)}",
            prefix=CONST["AF_ENVVAR_PREFIX"])
    
    def _build_request_headers(self):
        auth_type = self.auth_type
        headers   = self._session.headers.copy()

        if auth_type == "api_key":
            envvar  = self._build_envvar("api_key")
            api_key = upy.getenv(envvar)

            headers["Authorization"] = f"Bearer {api_key}"
        else:
            raise NotImplementedError(
                f"Auth type '{auth_type}' is not implemented."
            )

        return headers

    def _build_request_data(self, input=None, stream=True, role=None,
        tools=None):
        roles = []
        if role:
            for key, content in upy.iteritems(role):
                roles.append({"role": key, "content": content})

        body = {
            "model": self.name,
            "messages": roles + [
                {"role": "user", "content": str(input)}
            ],
            "stream": stream
        }

        if tools:
            body["tools"] = tools

        return body

    async def achat(self, input=None, stream=True, role=None, tools=None):
        url     = self._build_request_url("chat")
        headers = self._build_request_headers()
        body    = self._build_request_data(input, stream=stream, role=role,
            tools=tools
        )
        
        session_args = {
            "method": "post", "url": url, "headers": headers,
            "json": body, "timeout": DEFAULT["AF_PROVIDER_TIMEOUT"]
        }

        if stream:
            async with self._session.stream(**session_args) as response:
                response.raise_for_status()

                prefix = "data: "
                async for chunk in response.aiter_lines():
                    chunk = upy.safe_decode(chunk)
                    chunk = upy.strip(chunk)

                    if chunk.startswith(prefix):
                        payload = upy.strip(chunk[len(prefix):])
                        if payload != "[DONE]":
                            data  = upy.load_json(payload)
                            delta = data["choices"][0]["delta"]

                            content = delta.get("content")
                            tools   = delta.get("tool_calls")
                            
                            result  = {"content": content}

                            if tools:
                                names = []

                                for tool in tools:
                                    name = upy.getattr2(tool, "function.name")
                                    if name:
                                        names.append(name)

                                if names:
                                    result["tools"] = names

                            yield result
        else:
            response = await self._session.request(**session_args)
            response.raise_for_status()

            data = response.json()

            content = data["choices"][0]["message"]["content"]

            if content:
                yield {"content": content}

    def chat(self, *args, **kwargs):
        return upy.run_async(self.achat(*args, **kwargs))

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
        url       = meta["url"],
        endpoints = meta["endpoints"],
        auth_type = meta["auth_type"],
    )