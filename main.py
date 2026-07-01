from fastapi import FastAPI
import requests

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

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": coin.lower(),
        "price_change_percentage": "24h"
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, params=params, headers=headers)

        if r.status_code != 200:
            return {"error": "API error", "status": r.status_code}

        data = r.json()

        if not data:
            return {"error": "Coin not found"}

        coin_data = data[0]

        return {
            "name": coin_data.get("name"),
            "symbol": coin_data.get("symbol"),
            "price": coin_data.get("current_price"),
            "change_24h": coin_data.get("price_change_percentage_24h"),
            "market_cap": coin_data.get("market_cap"),
            "status": "ok"
        }

    except Exception as e:
        return {"error": str(e)}