from pydantic import BaseModel


class LastPriceResponse(BaseModel):
    price: float

class CryptoPriceResponse(LastPriceResponse):
    ticker: str
    timestamp: int