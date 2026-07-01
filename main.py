from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import math

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache (برای جلوگیری از 429)
CACHE = {}
CACHE_TIME = 20  # ثانیه

# Coin mapping
SYMBOLS = {
    "btc": "bitcoin",
    "bitcoin": "bitcoin",
    "eth": "ethereum",
    "ethereum": "ethereum",
    "sol": "solana",
    "solana": "solana"
}

# گرفتن دیتا
def fetch_coin(coin: str):
    coin = coin.lower()
    coin = SYMBOLS.get(coin, coin)

    if coin in CACHE:
        data, t = CACHE[coin]
        if time.time() - t < CACHE_TIME:
            return data

    url = f"https://api.coingecko.com/api/v3/coins/{coin}"

    r = requests.get(url)

    if r.status_code != 200:
        return {"error": "Coin not found", "status": r.status_code}

    data = r.json()

    price = data["market_data"]["current_price"]["usd"]
    change_24h = data["market_data"]["price_change_percentage_24h"]
    market_cap = data["market_data"]["market_cap"]["usd"]

    result = {
        "name": data["name"],
        "symbol": data["symbol"],
        "price": price,
        "change_24h": change_24h,
        "market_cap": market_cap,
        "status": "ok"
    }

    CACHE[coin] = (result, time.time())
    return result


# 🧠 AI Trading Signal Engine
def ai_signal(price, change_24h, market_cap):
    score = 0

    # روند 24h
    if change_24h > 3:
        score += 2
    elif change_24h > 0:
        score += 1
    elif change_24h < -3:
        score -= 2
    else:
        score -= 1

    # مارکت کپ (پایداری)
    if market_cap > 1e11:
        score += 1

    # تصمیم نهایی
    if score >= 2:
        return "BUY 🟢"
    elif score <= -2:
        return "SELL 🔴"
    else:
        return "HOLD 🟡"


# Home
@app.get("/")
def home():
    return {
        "status": "AI Trading API Running",
        "endpoints": ["/search", "/ai"]
    }


# قیمت ساده
@app.get("/search")
def search(coin: str = Query(...)):
    return fetch_coin(coin)


# 🤖 AI Trading Endpoint (اصلی)
@app.get("/ai")
def ai(coin: str = Query(...)):
    data = fetch_coin(coin)

    if "error" in data:
        return data

    signal = ai_signal(
        data["price"],
        data["change_24h"],
        data["market_cap"]
    )

    return {
        "coin": data["name"],
        "price": data["price"],
        "change_24h": data["change_24h"],
        "market_cap": data["market_cap"],
        "ai_signal": signal,
        "status": "ok"
    }