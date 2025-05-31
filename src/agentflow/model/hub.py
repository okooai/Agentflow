import os.path as osp, upyog as upy

from agentflow.model  import (
    BaseModel,
    Agent
)
from agentflow.config import CONST, DEFAULT

class Hub(BaseModel):
    async def aget(self, *names,
        cache=True,
    ):
        agents = []

        af_file = CONST["FILENAME"]
        for name in names:
            af_url_name = upy.join2(
                DEFAULT["URL_HUB"],
                name,
                af_file,
                path=True
            )
            af_file_path_target = upy.join2(
                DEFAULT["CACHE_HUB"],
                af_file,
                name,
                path=True
            )
            
            if not (osp.exists(af_file_path_target) and cache):
                upy.download_file(
                    af_url_name,
                    af_file_path_target
                )

            agent = Agent.load(af_file_path_target)
            agents.append(agent)

        return upy.squash(agents)

async def ahub(*args, **kwargs):
    hub_ = Hub()
    return await hub_.aget(*args, **kwargs)

def hub(*args, **kwargs):
    return upy.run_async(ahub(*args, **kwargs))