from fastapi import FastAPI
from market.crypto import get_btc_price

app = FastAPI(
    title="TEKA MarketMind AI",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "company": "TEKA",
        "status": "Running"
    }

@app.get("/btc")
def btc():

    price = get_btc_price()

    return {
        "symbol": "BTCUSDT",
        "price": price
    }