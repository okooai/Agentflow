import os.path as osp, re, upyog as upy

from agentflow.model import BaseModel, Agent
from agentflow.config import CONST, DEFAULT


class Hub(BaseModel):
    def _resolve_agent_uri(self, uri):
        match = re.match(CONST["AF_HUB_NAME_PATTERN"], uri)
        if not match:
            raise ValueError(f"Invalid Agent URI format: {uri}")

        meta = match.groupdict()

        namespace = meta["namespace"]
        name = meta["name"]

        if not name:
            raise ValueError(f"Invalid Agent URI format: {uri}")

        tag = match.group("tag") or CONST["AF_TAG"]

        return {"namespace": namespace, "name": name, "tag": tag}

    async def _afetch_agent(self, name, cache=True):
        af_name = self._resolve_agent_uri(name)

        af_file = CONST["AF_FILENAME"]
        af_url_name = upy.join2(
            DEFAULT["AF_URL_HUB"], af_name["name"], af_file, path=True
        )
        af_file_path_target = upy.join2(
            DEFAULT["AF_CACHE_HUB"], af_file, af_name["name"], path=True
        )

        if not (osp.exists(af_file_path_target) and cache):
            upy.download_file(af_url_name, af_file_path_target)

        return Agent.load(af_file_path_target)

    async def aget(
        self,
        *names,
        cache=True,
    ):
        return upy.squash(
            await upy.run_async_all(
                [self._afetch_agent(name, cache=cache) for name in names]
            )
        )


async def ahub(*args, **kwargs):
    hub_ = Hub()
    return await hub_.aget(*args, **kwargs)


def hub(*args, **kwargs):
    return upy.run_async(ahub(*args, **kwargs))
