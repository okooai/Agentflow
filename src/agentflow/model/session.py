import upyog as upy

from agentflow.model.base import BaseModel

class Session(BaseModel):
    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self._session_id = upy.get_random_str(8)