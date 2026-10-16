from pydantic import BaseModel, ConfigDict


class LastPriceResponse(BaseModel):
    price: float

    model_config = ConfigDict(from_attributes=True)


class CryptoPriceResponse(LastPriceResponse):
    ticker: str
    timestamp: int
