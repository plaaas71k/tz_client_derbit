from app.db.database import DataCrypto
from sqlalchemy.orm import Mapped, mapped_column

class CryptoPrice(DataCrypto):
    __tablename__ = "crypto_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[int] = mapped_column()