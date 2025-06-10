import os.path as osp
import upyog as upy

from agentflow.model.base   import BaseModel
from agentflow.model.helper import HubMixin
from agentflow.config import CONST

class Action(BaseModel, HubMixin):
    _REPR_ATTRS = ("name",)

    async def _afetch_action(self, name, **kwargs):
        return self._fetch_hub("action", name, **kwargs)

    async def _handle_after_aget(self, name, target, **kwargs):
        fpath = upy.join2(target,
            CONST["AF_FILENAME_ACTION"], path=True
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
            parameters  = config.get("parameters") or {},
            config_path = fpath,
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

    async def arun(self, **params):
        """
            Run Action.
        """
        config_path = self.config_path
        config_dir  = upy.pardir(config_path, 1)

        path_handler = upy.join2(
            config_dir, CONST["AF_FILENAME_ACTION_HANDLER"], path=True
        )
        if not osp.exists(path_handler):
            errstr = f"No Action handler found for '{self.name}'"
            self.log("error", errstr)
            raise ValueError(errstr)

        with upy.ShellEnvironment(cwd = config_dir) as shell:
            module, ext = osp.splitext(CONST["AF_FILENAME_ACTION_HANDLER"])
            python = upy.get_python_exec("python")

            param_string = None
            if params:
                param_string = upy.create_param_string(params)

            env    = {
                upy.getenvvar("PARAM", prefix = CONST["AF_ENVVAR_PREFIX"]): param_string
            }

            code, output, error = shell(\
                f"{python} -c 'import upyog as upy; import {module}; print(upy.run_async({module}.handle()))'",
                output=True, env = env
            )

        return output