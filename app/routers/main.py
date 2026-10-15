
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.db.database import SessionDep
from app.models.cryptomodel import CryptoPrice
from app.schemas.crypto_price import CryptoPriceResponse, LastPriceResponse


router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=list[CryptoPriceResponse])
async def get_prices_by_ticker(
    session: SessionDep,
    ticker: str,
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
    ticker: str,
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
        ticker: str,
        date_from: int = Query(..., description="Начало периода (UNIX timestamp)"),
        date_to: int = Query(..., description="Конец периода (UNIX timestamp)")
):

    result = await session.scalars(
        select(CryptoPrice)
        .where(CryptoPrice.ticker == ticker.lower())
        .where(CryptoPrice.timestamp >= date_from)
        .where(CryptoPrice.timestamp <= date_to)
        .order_by(CryptoPrice.timestamp.asc())
    )
    return result.all()
