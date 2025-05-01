from logging import getLogger, Logger

from aiohttp import ClientSession

logger: Logger = getLogger(__name__)

class CatImageAPI:
    def __init__(self, api_key: str, client: ClientSession) -> None:
        self._base_url = "https://api.thecatapi.com/v1/images/search"
        self._headers = {
            "x-api-key": api_key
        }
        self._client = client

    async def get_cat_image(self) -> str:
        """Get a random cat image URL."""
        async with self._client.get(self._base_url, headers=self._headers) as response:
            logger.debug("Requesting cat image from %s", self._base_url)
            response.raise_for_status()
            data = await response.json()
            logger.debug("Received cat image data: %s", data)
            return data[0]["url"]
