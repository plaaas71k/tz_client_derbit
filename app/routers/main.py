from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.db.database import SessionDep
from app.models.cryptomodel import CryptoPrice
from app.schemas.CryptopriceS import CryptopriceS


router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=list[CryptopriceS])
async def get_prices(
    session: SessionDep,
    ticker: Annotated[str, Query(min_length=1, description="Currency index ticker")],
) -> list[CryptoPrice]:
    result = await session.scalars(
        select(CryptoPrice)
        .where(CryptoPrice.ticker == ticker.lower())
        .order_by(CryptoPrice.timestamp.asc())
    )
    return list(result.all())
