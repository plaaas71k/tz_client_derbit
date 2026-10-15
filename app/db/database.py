from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(f"postgresql+asyncpg://data_crypto:example@localhost:5432/data_crypto")


new_session = async_sessionmaker(engine, expire_on_commit=False)


class DataCrypto(DeclarativeBase):
    pass


async def get_db():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]