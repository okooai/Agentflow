import os.path as osp
import upyog as upy

from agentflow.model  import (
    BaseModel,
    Agent
)
from agentflow.config import CONST, DEFAULT

class Hub(BaseModel):
    def get(self, name,
        cache=True,
    ):
        af_file_ext = CONST["AF_FILE_EXT"]
        af_url_name = upy.join2(
            DEFAULT["AF_URL_HUB"],
            f"{name}{af_file_ext}",
            path=True
        )
        af_file_path_target = upy.join2(
            DEFAULT["AF_CACHE_HUB"],
            f"{name}{af_file_ext}",
            path=True
        )
        
        if not (osp.exists(af_file_path_target) and cache):
            upy.download_file(
                af_url_name,
                af_file_path_target,
            )

        return Agent.load(af_file_path_target)

def hub(name):
    hub_ = Hub()
    return hub_.get(name)

async def ahub(name):
    pass