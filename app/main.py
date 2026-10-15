from fastapi import FastAPI

from app.routers.main import router as prices_router


app = FastAPI(title="Deribit Price API")
app.include_router(prices_router)


@app.get("/")
async def root():
    return {"message": "Deribit Price API"}
