from pydantic import BaseModel, ConfigDict


class CryptopriceS(BaseModel):
    ticker: str
    price: float
    timestamp: int

    model_config = ConfigDict(from_attributes=True)
