from agentflow.model.base import BaseModel

class Message(BaseModel):
    def __init__(self, content=None, *args, **kwargs):
        super_ = super(Message, self)
        super_.__init__(*args, **kwargs)

        self.content = content

    def __str__(self):
        return self.content

class UserMessage(Message):
    role = "user"

class AgentMessage(Message):
    role = "agent"