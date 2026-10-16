import asyncio
import time

from celery import Celery
from app.db.database import engine, new_session

from app.client import ClientCrypto
from app.models.cryptomodel import CryptoPrice
from app.config import settings



app = Celery(
    'tasks',
    broker= settings.REDIS_URL,
    backend=settings.REDIS_URL
)


app.conf.beat_schedule = {
    'fetch-crypto-prices': {
        'task': 'app.tasks.fetch_crypto_prices',
        'schedule': 60.0,
    }
}


async def fetch_and_save():
    client = ClientCrypto()
    tickers = ["btc_usd", "eth_usd"]

    try:
        async with new_session() as session:
            async with session.begin():
                for ticker in tickers:
                    data = await client.get_index_price(ticker)

                    if "error" in data:
                        continue

                    price = data.get('result', {}).get('index_price')

                    if price is None:
                        continue

                    session.add(
                        CryptoPrice(
                            ticker=ticker,
                            price=price,
                            timestamp=int(time.time()),
                        )
                    )
    finally:
        await engine.dispose()


@app.task(name='app.tasks.fetch_crypto_prices')
def fetch_crypto_prices():
    asyncio.run(fetch_and_save())
