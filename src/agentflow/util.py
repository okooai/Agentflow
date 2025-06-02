import httpx

async def arequest(url, method="get", **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()