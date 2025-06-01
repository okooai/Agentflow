import upyog as upy

from agentflow.model.base import BaseModel
from agentflow.model.provider import provider

from agentflow.config import DEFAULT

class AgentConsole(upy.Console):
    def __init__(self, agent, *args, **kwargs):
        super_ = super(AgentConsole, self)
        super_.__init__(*args, **kwargs)

        self.agent = agent

    async def ahandle(self, input):
        provider = self.agent._provider
        response = await provider.achat(input)
        return response["content"]

class Agent(BaseModel):
    _REPR_ATTRS = ("id", "name")

    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self._provider = provider(kwargs.get("provider") or DEFAULT["AF_PROVIDER"])

    @staticmethod
    def load(name, fpath):
        metadata = upy.load_config(fpath)
        return Agent(name=metadata.get("name") or name)

    async def arun(self, input=None, interactive=False, **kwargs):
        """
        Run Agent.
        """
        if interactive:
            console = AgentConsole(self)
            await console.arun()

    def run(self, *args, **kwargs):
        return upy.run_async(self.arun(*args, **kwargs))

    async def __call__(self, *args, **kwargs):
        return await self.arun(*args, **kwargs)