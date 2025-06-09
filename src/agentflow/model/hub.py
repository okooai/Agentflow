import upyog as upy

from agentflow.model.base   import BaseModel
from agentflow.model.helper import HubMixin
from agentflow.model.agent  import Agent
from agentflow.config       import CONST
from agentflow.exception    import AgentflowError

class Hub(BaseModel, HubMixin):
    async def _handle_after_agent_aget(self, name, target, **kwargs):
        fpath = upy.join2(target,
            CONST["AF_FILENAME_AGENT"], path=True
        )

        agent = None

        try:
            agent = Agent.load(name, fpath)
            await agent.ainstall()
        except upy.FileNotFoundError:
            errstr = f"No Agentfile found for '{name}'"
            self.log("error", errstr)

            upy.remove(target, recursive=True)

            raise AgentflowError(errstr)

        return agent

    async def _afetch_agent(self, name, **kwargs):
        return self._fetch_hub("agent", name, **kwargs)

    async def aget(self,
        *names,
        **kwargs
    ):
        """
            Get Agent Action.
        """
        super_ = super(Hub, self)
        return await super_.aget(
            type_   = "agent",
            names   = names,
            fetcher = self._afetch_agent,
            after_aget = self._handle_after_agent_aget,
            **kwargs
        )

async def ahub(*args, **kwargs):
    hub_ = Hub()
    return await hub_.aget(*args, **kwargs)

def hub(*args, **kwargs):
    return upy.run_async(ahub(*args, **kwargs))