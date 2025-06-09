import upyog as upy

from agentflow.model.base  import BaseModel
from agentflow.model.store import Store
from agentflow.model.message import (
    UserMessage,
    AgentMessage
)

class Session(BaseModel):
    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self.session_id = upy.get_random_str(8)
        self.store      = Store()

    async def setup(self):
        """
            Setup the Session.
        """
        store = self.store
        await store.ainsert_session(self)

    async def aget_messages(self, **kwargs):
        """
            Get messages from the Session's Store.
        """
        kwargs["where"] = upy.merge_dict(
            kwargs.get("where", {}),
            { "session_id": self.session_id }
        )

        messages = await self.store.aget_messages(**kwargs)

        for i, message in enumerate(messages):
            if message['actions']:
                messages[i]['actions'] = upy.load_json(message['actions'])

        return messages

    async def ainsert_message(self, message):
        """
            Insert a message into the Session's Store.
        """
        message.session = self
        await self.store.ainsert_message(message)