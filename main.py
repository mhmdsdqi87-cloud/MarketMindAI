from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ساده‌ترین cache واقعی
CACHE = {}
CACHE_TTL = 60  # 60 ثانیه

# گرفتن دیتا از CoinGecko
def fetch_coin(coin: str):
    coin = coin.lower().strip()

    # cache check
    if coin in CACHE:
        if time.time() - CACHE[coin]["time"] < CACHE_TTL:
            return CACHE[coin]["data"]

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

        r = requests.get(url, params=params, timeout=5)

        # اگر rate limit خوردی
        if r.status_code == 429:
            return {
                "error": "rate_limited",
                "message": "Too many requests, try again later"
            }

        if r.status_code != 200:
            return {
                "error": "api_error",
                "status": r.status_code
            }

        data = r.json()

        if coin not in data:
            return {
                "error": "not_found",
                "coin": coin
            }

        result = {
            "name": coin,
            "price": data[coin].get("usd", 0),
            "change_24h": data[coin].get("usd_24h_change", 0),
            "status": "ok",
            "timestamp": int(time.time())
        }

        CACHE[coin] = {
            "data": result,
            "time": time.time()
        }

        return result

    except Exception as e:
        return {
            "error": "server_error",
            "detail": str(e)
        }


# ✅ این همون endpoint اصلیه (404 رو کامل حل می‌کنه)
@app.get("/search")
def search(coin: str = Query(...)):
    return fetch_coin(coin)


# health check برای render
@app.get("/")
def home():
    return {
        "status": "ok",
        "service": "MarketMind AI",
        "endpoints": ["/search?coin=bitcoin"]
    }