from fastapi import FastAPI
import requests
import time

CACHE = {}
CACHE_TIME = {}

app = FastAPI()

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"status": "MarketMindAI is running 🚀"}

# ---------------- COINS LIST (optional) ----------------
@app.get("/coins")
def get_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, params=params, headers=headers)

    if r.status_code != 200:
        return {"error": "API failed", "status": r.status_code}

    return r.json()


# ---------------- SEARCH (FIXED) ----------------
@app.get("/search")
def search_coin(coin: str):

    now = time.time()

    # cache key
    key = coin.lower()

    # اگر کش هنوز معتبره
    if key in CACHE and now - CACHE_TIME[key] < 30:
        return CACHE[key]

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": key,
        "price_change_percentage": "24h"
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, params=params, headers=headers)

    if r.status_code != 200:
        return {"error": "API rate limit (429)", "hint": "try later"}

    data = r.json()

    if not data:
        return {"error": "Coin not found"}

    result = {
        "name": data[0].get("name"),
        "price": data[0].get("current_price"),
        "change_24h": data[0].get("price_change_percentage_24h"),
        "status": "ok"
    }

    CACHE[key] = result
    CACHE_TIME[key] = now

    return result