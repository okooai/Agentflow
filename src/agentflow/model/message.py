from agentflow.model.base import BaseModel

class Message(BaseModel):
    def __init__(self, content=None, actions=None, *args, **kwargs):
        super_ = super(Message, self)
        super_.__init__(*args, **kwargs)

        self.content = content
        self.actions = actions or []

    def __str__(self):
        return self.content

class UserMessage(Message):
    role = "user"

class AgentMessage(Message):
    role = "agent"
