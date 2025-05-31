import os.path as osp
import upyog as upy

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

        for name in names:
            af_file_ext = CONST["FILE_EXT"]
            af_url_name = upy.join2(
                DEFAULT["URL_HUB"],
                f"{name}{af_file_ext}",
                path=True
            )
            af_file_path_target = upy.join2(
                DEFAULT["CACHE_HUB"],
                f"{name}{af_file_ext}",
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