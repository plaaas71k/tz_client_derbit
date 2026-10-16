
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.db.database import SessionDep
from app.models.cryptomodel import CryptoPrice
from app.schemas.crypto_price import CryptoPriceResponse, LastPriceResponse


router = APIRouter(prefix="/prices", tags=["prices"])
TickerQuery = Annotated[str, Query(min_length=1, description="Currency index ticker")]


@router.get("", response_model=list[CryptoPriceResponse])
async def get_prices_by_ticker(
    session: SessionDep,
    ticker: TickerQuery,
) -> list[CryptoPrice]:
    result = await session.scalars(
        select(CryptoPrice)
        .where(CryptoPrice.ticker == ticker.lower())
        .order_by(CryptoPrice.timestamp.asc())
    )
    return result.all()


@router.get("/last", response_model=LastPriceResponse)
async def get_last_price_by_ticker(
    session: SessionDep,
    ticker: TickerQuery,
) -> CryptoPrice:
    result = await session.scalars(
        select(CryptoPrice)
        .where(CryptoPrice.ticker == ticker.lower())
        .order_by(CryptoPrice.timestamp.desc())
    )
    price = result.first()
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No prices found for ticker '{ticker.lower()}'",
        )
    return price


@router.get("/history", response_model=list[CryptoPriceResponse])
async def get_price_history_by_ticker(
        session: SessionDep,
        ticker: TickerQuery,
        date_from: int = Query(..., description="Начало периода (UNIX timestamp)"),
        date_to: int = Query(..., description="Конец периода (UNIX timestamp)")
):

    if date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="date_from must not be greater than date_to",
        )

    result = await session.scalars(
        select(CryptoPrice)
        .where(CryptoPrice.ticker == ticker.lower())
        .where(CryptoPrice.timestamp >= date_from)
        .where(CryptoPrice.timestamp <= date_to)
        .order_by(CryptoPrice.timestamp.asc())
    )
    return result.all()
