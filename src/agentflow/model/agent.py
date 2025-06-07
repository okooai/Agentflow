import upyog as upy

from agentflow.model.base       import BaseModel
from agentflow.model.action     import Action
from agentflow.model.provider   import provider
from agentflow.model.session    import Session
from agentflow.model.helper     import HubMixin
from agentflow.config           import DEFAULT

class AgentConsole(upy.Console):
    def __init__(self, agent, *args, **kwargs):
        super_ = super(AgentConsole, self)
        super_.__init__(*args, **kwargs)

        self.agent = agent

    async def ahandle(self, input):
        provider  = self.agent._provider
        session   = self.agent._session
        objective = self.agent.objective

        async for response in provider.achat(
            input,
            role   = { "system": objective },
            tools  = self.agent._build_schema_tools(),
            stream = True
        ):
            tools = response.get("tools")
            if tools:
                for tool in tools:
                    action = self.agent.actions[tool]

                    upy.echo(
                        upy.cli_format(
                            f"[a]: {action.name}",
                            upy.CLI_GRAY
                        )
                    )

                    result = await action.arun()

                    upy.echo(
                        upy.cli_format(
                            f"[o]: {upy.ellipsis(result, 50)}",
                            upy.CLI_GRAY
                        )
                    )

            if response["content"]:
                upy.echo(
                    upy.cli_format(
                        response["content"], upy.CLI_BLUE
                    )
                , nl=False)

        upy.echo()

class Agent(BaseModel, HubMixin):
    _REPR_ATTRS = ("id", "name")

    def __init__(self, *args, **kwargs):
        self._actions  = kwargs.pop("actions") or []

        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self._provider = provider(
            kwargs.get("provider") or DEFAULT["AF_PROVIDER"]
        )
        self._session  = Session()

    @staticmethod
    def load(name, fpath):
        metadata = upy.load_config(fpath)
        return Agent(
            name      = metadata.get("name") or name,
            objective = metadata["objective"],
            actions   = metadata.get("actions")
        )

    async def ainstall(self, **kwargs):
        self.log("info", f"Installing Agent '{self.name}'")

        if self._actions:
            actions = [Action(name=action) for action in self._actions]
            kwargs["fail"]  = kwargs.get("fail") or True

            actions = await upy.run_async_all(
                (action.aget(**kwargs) for action in actions),
            )
            self.actions    = {
                action.name: action for action in actions
            }

    def _build_schema_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": action.name,
                "description": action.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param: {
                            "type": "string",
                            "description": meta["description"],
                        } for param, meta in upy.iteritems(action.parameters)
                    },
                    "required": [
                        param for param in upy.iterkeys(action.parameters)
                    ]
                }
            }
        } for action in upy.itervalues(self.actions)]

    async def arun(self, input=None, interactive=False, stream=False,
        **kwargs):
        """
        Run Agent.
        """
        if interactive:
            console = AgentConsole(self)
            await console.arun(input=input)
        else:
            async for response in self._provider.achat(
                input,
                role   = { "system": self.objective },
                tools  = self._build_schema_tools(),
                stream = stream
            ):
                return response["content"]

    def run(self, *args, **kwargs):
        return upy.run_async(self.arun(*args, **kwargs))

    async def __call__(self, *args, **kwargs):
        return await self.arun(*args, **kwargs)