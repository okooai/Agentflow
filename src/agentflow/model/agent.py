import upyog as upy

from agentflow.model.base       import BaseModel
from agentflow.model.action     import Action
from agentflow.model.provider   import provider
from agentflow.model.session    import Session
from agentflow.model.message    import (
    UserMessage,
    AgentMessage
)
from agentflow.model.helper     import HubMixin
from agentflow.config           import DEFAULT

class AgentConsole(upy.Console):
    def __init__(self, agent, *args, **kwargs):
        super_ = super(AgentConsole, self)
        super_.__init__(*args, **kwargs)

        self.agent = agent

    async def ahandle(self, input_=None):
        provider  = self.agent._provider
        session   = self.agent._session
        objective = self.agent.objective
        
        prompt    = await self.agent._abuild_model_prompt(input_=input_)

        chunks    = []

        async for response in provider.achat(
            prompt,
            role    = { "system": objective },
            tools   = self.agent._build_schema_tools(),
            stream  = True
        ):
            tools   = response.get("tools")
            if tools:
                actions = []

                for tool, args in upy.iteritems(tools):
                    action = self.agent.actions[tool]

                    upy.echo(
                        upy.cli_format(
                            f"[a]: {action.name}",
                            upy.CLI_GRAY
                        )
                    )

                    result = await action.arun(**args)
                    actions.append({
                        "name": action.name, "args": args,
                        "result": result
                    })

                    upy.echo(
                        upy.cli_format(
                            f"[o]: {upy.ellipsis(result, 50)}",
                            upy.CLI_GRAY
                        )
                    )

                await session.ainsert_message(
                    AgentMessage(
                        actions = actions
                    )
                )

                await self.ahandle()
            else:
                # TODO: handle when both content and tools are provided.
                content = response.get("content")
                if content:
                    upy.echo(
                        upy.cli_format(
                            content, upy.CLI_BLUE
                        )
                    , nl=False)

                    chunks.append(content)

        if chunks:
            message_agent = AgentMessage(
                content = upy.join2(chunks)
            )
            await session.ainsert_message(message_agent)

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

    @property
    def actions(self):
        if not hasattr(self, "_actions_map"):
            self._actions_map = {}

        return self._actions_map
    
    @actions.setter
    def actions(self, value):
        if not isinstance(value, dict):
            raise TypeError("Actions must be a dictionary.")
        self._actions_map = value

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

    async def _abuild_model_prompt(self, input_=None):
        session = self._session

        prompt  = None
        chunks  = []

        if input_:
            message = UserMessage(content=input_)
            await session.ainsert_message(message)

        messages = await session.aget_messages()

        if messages:
            for message in messages:
                # TODO: deserialize
                content = message['content']
                if message['actions']:
                    actions = message['actions']
                    chunks.append(
                        f"{message['role']}: [actions] - {actions}"
                    )
                else:
                    chunks.append(f"{message['role']}: {content}")

        if chunks:
            prompt = upy.join2(chunks, by="\n")

        return prompt

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
        await self._session.setup()

        if interactive:
            console = AgentConsole(self)
            await console.arun(input_=input)
        else:
            async for response in self._provider.achat(
                self._abuild_model_prompt(input_=input),
                role   = { "system": self.objective },
                tools  = self._build_schema_tools(),
                stream = stream
            ):
                return response["content"]

    def run(self, *args, **kwargs):
        return upy.run_async(self.arun(*args, **kwargs))

    async def __call__(self, *args, **kwargs):
        return await self.arun(*args, **kwargs)