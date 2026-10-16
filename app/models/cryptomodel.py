from app.db.database import DataCrypto
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

class CryptoPrice(DataCrypto):
    __tablename__ = "crypto_prices"
    __table_args__ = (
        Index("ix_crypto_prices_ticker_timestamp", "ticker", "timestamp"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[int] = mapped_column()
