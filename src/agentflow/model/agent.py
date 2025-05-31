from agentflow.model    import BaseModel
from agentflow.provider import provider

from agentflow.config   import DEFAULT

class Agent(BaseModel):
    _REPR_ATTRS = [
        "name"
    ]

    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)

        self._provider = provider(
            kwargs.get("provider") or DEFAULT["AF_PROVIDER"]
        )

    @staticmethod
    def load(fpath):
        return Agent()
    
    def run(self, input=None):
        """
        Run Agent.
        """
        pass