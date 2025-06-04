import upyog as upy

from agentflow.model.base   import BaseModel
from agentflow.model.helper import HubMixin

class Action(BaseModel, HubMixin):
    _REPR_ATTRS = ("name",)

    async def _afetch_action(self, name, **kwargs):
        return self._fetch_hub("action", name, **kwargs)
    
    async def _handle_after_aget(self, name, target, **kwargs):
        fpath = upy.join2(target,
            "action.yml", path=True
        )

        action = None

        try:
            action = Action.load(fpath)
        except upy.FileNotFoundError:
            errstr = f"No Actionfile found for '{name}'"
            self.log("error", errstr)

            upy.remove(target, recursive=True)

            raise ValueError(errstr)

        return action

    @staticmethod
    def load(fpath):
        config = upy.load_config(fpath)
        return Action(
            name        = config["name"],
            description = config["description"],
        )

    async def aget(self, **kwargs):
        """
            Get Agent Action.
        """
        super_ = super(Action, self)
        return await super_.aget(
            type_   = "action",
            names   = self.name,
            fetcher = self._afetch_action,
            after_aget = self._handle_after_aget,
            **kwargs
        )