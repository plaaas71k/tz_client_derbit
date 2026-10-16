import aiohttp


class ClientCrypto:

    BASE_URL = 'https://www.deribit.com/api/v2/public/get_index_price'

    def __init__(self, timeout_seconds: float = 10.0):
        self._timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    async def get_index_price(self, index_name: str) -> dict:
        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            async with session.get(self.BASE_URL, params={'index_name': index_name}) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return {"error": f"Bad status {response.status}"}



