import asyncio
from app.client import ClientCrypto



async def main():
    client_derbit = ClientCrypto()


    for ticker in ("btc_usd", "eth_usd"):
        result = await client_derbit.get_index_price(ticker)
        print(ticker, result)


if __name__ == "__main__":
    asyncio.run(main())