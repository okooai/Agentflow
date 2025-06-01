import os.path as osp, re, upyog as upy

from agentflow.model     import BaseModel, Agent
from agentflow.config    import CONST, DEFAULT
from agentflow.exception import AgentflowError

class Hub(BaseModel):
    def _resolve_agent_uri(self, uri):
        match = re.match(CONST["AF_NAME_PATTERN_AGENT"], uri)
        if not match:
            raise ValueError(f"Invalid Agent URI format: {uri}")

        meta = match.groupdict()

        url  = CONST["AF_URL_REPO_BASE"]

        namespace = meta["namespace"]
        name = meta["name"]

        if not namespace:
            namespace = CONST["AF_NAMESPACE"]

        if not name:
            raise ValueError(f"Invalid Agent URI format: {uri}")

        tag = match.group("tag") or CONST["AF_TAG"]

        return {"namespace": namespace, "name": name, "tag": tag,
            "url": url}

    async def _afetch_agent(self, name, verbose=False):
        meta   = self._resolve_agent_uri(name)

        url    = upy.join2(meta["url"], meta["namespace"], meta["name"], path=True)
        target = upy.join2(
            DEFAULT["AF_CACHE_HUB"],
            meta["namespace"],
            meta["name"],
            path=True
        )

        if not osp.exists(target):
            upy.git_clone(url, target, depth=1, verbose=verbose)
        else:
            upy.update_git_repo(
                target, clone=False, url=url
            )

        fpath = upy.join2(target, CONST["AF_FILENAME"], path=True)

        agent = None

        try:
            agent = Agent.load(name, fpath)
        except upy.FileNotFoundError:
            errstr = f"No Agentfile found for '{name}'"
            self.log("error", errstr)

            upy.remove(target, recursive=True)

            raise AgentflowError(errstr)

        return agent

    async def aget(
        self,
        *names,
        fail=False,
        verbose=False
    ):
        agents = await upy.run_async_all(
            [self._afetch_agent(name, verbose=verbose) for name in names]
        , fail=False)

        refmap = zip(names, agents)

        agents, errors = upy.array_filter(
            lambda x: isinstance(x, Agent),
            agents,
            other=True
        )

        count  = len(agents)

        self.log("success", (
                f"Fetched {count} {upy.pluralize('Agent', count)}: "
                f"{upy.join2([a.name for a in agents], by=', ')}"
            )
        )

        if errors:
            errmap = {name: e for name, e in refmap if isinstance(e, Exception)}
            errstr = (
                f"Failed to fetch {len(errors)} {upy.pluralize('Agent', len(errors))}: "
                f"{upy.join2([f'({name}: {repr(e)})' for name, e in upy.iteritems(errmap)], by=', ')}"
            )
            self.log("error", errstr)

            if fail:
                raise AgentflowError(errstr)

        return upy.squash(agents)

async def ahub(*args, **kwargs):
    hub_ = Hub()
    return await hub_.aget(*args, **kwargs)

def hub(*args, **kwargs):
    return upy.run_async(ahub(*args, **kwargs))