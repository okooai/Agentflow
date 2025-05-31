import upyog as upy

from agentflow.model.base import BaseModel
from agentflow.model.provider import provider

from agentflow.config import DEFAULT


class Agent(BaseModel):
    _REPR_ATTRS = ["id", "name"]

    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self._provider = provider(kwargs.get("provider") or DEFAULT["AF_PROVIDER"])

    @staticmethod
    def load(fpath):
        metadata = upy.load_config(fpath)
        return Agent(name=metadata["name"])

    def run(self, input=None):
        """
        Run Agent.
        """
        pass

    def __call__(self, input=None):
        return self.run(input)
