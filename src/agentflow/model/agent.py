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
        provider  = self.agent._provider
        objective = self.agent.objective

        async for response in provider.achat(
            input,
            role   = { "system": objective },
            stream = True
        ):
            upy.echo(
                upy.cli_format(
                    response["content"], upy.CLI_BLUE
                )
            , nl=False)
        upy.echo()

class Agent(BaseModel):
    _REPR_ATTRS = ("id", "name")

    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self._provider = provider(
            kwargs.get("provider") or DEFAULT["AF_PROVIDER"]
        )

    @staticmethod
    def load(name, fpath):
        metadata = upy.load_config(fpath)
        return Agent(
            name      = metadata.get("name") or name,
            objective = metadata["objective"],
        )

    async def arun(self, input=None, interactive=False, stream=False, **kwargs):
        """
        Run Agent.
        """
        if interactive:
            console = AgentConsole(self)
            await console.arun()
        else:
            async for response in self._provider.achat(
                input,
                role   = { "system": self.objective },
                stream = stream
            ):
                return response["content"]

    def run(self, *args, **kwargs):
        return upy.run_async(self.arun(*args, **kwargs))

    async def __call__(self, *args, **kwargs):
        return await self.arun(*args, **kwargs)