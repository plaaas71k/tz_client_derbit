from fastapi import FastAPI

from app.routers.main import router as prices_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "=" * 50)
    print("FASTAPI APPLICATION STARTED SUCCESSFULLY!")
    print("SWAGGER DOCUMENTATION: http://localhost:8000/docs")

    yield


app = FastAPI(title="Deribit Price API", lifespan=lifespan)
app.include_router(prices_router)


@app.get("/")
async def root():
    return {"message": "Deribit Price API"}
