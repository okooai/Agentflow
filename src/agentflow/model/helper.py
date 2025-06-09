import os.path as osp, re, upyog as upy

from agentflow.__attr__     import __name__ as NAME
from agentflow.config       import CONST, DEFAULT
from agentflow.exception    import AgentflowError

class HubMixin:
    @staticmethod
    def _resolve_af_uri(uri):
        match = re.match(CONST["AF_NAME_PATTERN"], uri)
        if not match:
            raise ValueError(f"Invalid {NAME} URI format: {uri}")

        meta = match.groupdict()

        url  = CONST["AF_URL_REPO_BASE"]

        namespace = meta["namespace"]
        name = meta["name"]

        if not namespace:
            namespace = CONST["AF_NAMESPACE"]

        if not name:
            raise ValueError(f"Invalid URI format: {uri}")

        tag = match.group("tag") or CONST["AF_TAG"]

        return {"namespace": namespace, "name": name, "tag": tag,
            "url": url}

    def _fetch_hub(self, type_, name, verbose=False):
        meta   = self._resolve_af_uri(name)

        url    = upy.join2(meta["url"], meta["namespace"], meta["name"], path=True)
        target = upy.join2(
            DEFAULT["AF_PATH_CACHE_HUB"],
            upy.pluralize(type_, count=2),
            meta["namespace"],
            meta["name"],
            path=True
        )

        if not osp.exists(target):
            upy.git_clone(url, target, depth=1, verbose=False)
        else:
            upy.update_git_repo(
                target, clone=False, url=url, verbose=False
            )

        return target

    async def aget(
        self,
        type_,
        names,
        fetcher,
        after_aget = None,
        fail       = False,
        verbose    = False,
    ):
        """
            Retrieve a list of repos from the Hub.
        """
        names = upy.sequencify(names)

        async def _fetch(name, **kwargs):
            target = await fetcher(name, **kwargs)
            if after_aget:
                return await after_aget(name, target)
            return target

        repos = await upy.run_async_all(
            [_fetch(name, verbose=verbose) for name in names]
        , fail=fail)

        refmap = zip(names, repos)

        repos, errors = upy.array_filter(
            lambda x: not isinstance(x, Exception),
            repos,
            other=True
        )

        count  = len(repos)

        self.log("success", (
                f"Fetched {count} {upy.pluralize(upy.capitalize(type_), count)}: "
                f"{upy.join2([r.name for r in repos], by=', ')}"
            )
        )

        if errors:
            errmap = {name: e for name, e in refmap if isinstance(e, Exception)}
            errstr = (
                f"Failed to fetch {len(errors)} {upy.pluralize(upy.capitalize(type_), len(errors))}: "
                f"{upy.join2([f'({name}: {repr(e)})' for name, e in upy.iteritems(errmap)], by=', ')}"
            )
            self.log("error", errstr)

            if fail:
                raise AgentflowError(errstr)

        return upy.squash(repos)