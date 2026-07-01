from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

app = FastAPI()

# CORS برای فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# کش ساده برای جلوگیری از 429
CACHE = {
    "data": None,
    "time": 0
}

CACHE_TIME = 20  # ثانیه


# =========================
# 📊 COIN DATA API
# =========================
@app.get("/api/coins")
def get_coins():
    global CACHE

    now = time.time()

    # اگر کش هنوز معتبره
    if CACHE["data"] and now - CACHE["time"] < CACHE_TIME:
        return CACHE["data"]

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,cardano,tron,chainlink,avalanche-2",
        "price_change_percentage": "24h"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)

        if r.status_code != 200:
            return {"error": "API error", "status": r.status_code}

        data = r.json()

        result = {
            "data": data,
            "updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        CACHE["data"] = result
        CACHE["time"] = now

        return result

    except Exception as e:
        return {"error": str(e)}


# =========================
# 🤖 AI ANALYSIS API
# =========================
@app.get("/api/ai")
def ai_analysis():

    coins = get_coins()

    if "data" not in coins:
        return {
            "status": "error",
            "message": "no data"
        }

    data = coins["data"]

    up = 0
    down = 0

    for coin in data:
        change = coin.get("price_change_percentage_24h", 0)

        if change > 0:
            up += 1
        else:
            down += 1

    total = up + down if (up + down) > 0 else 1

    sentiment = "NEUTRAL"
    score = 50

    if up > down:
        sentiment = "BULLISH 🚀"
        score = int((up / total) * 100)
    else:
        sentiment = "BEARISH 📉"
        score = int((down / total) * 100)

    return {
        "status": "ok",
        "sentiment": sentiment,
        "confidence": score,
        "up": up,
        "down": down,
        "updated": coins.get("updated")
    }


# =========================
# 🏠 HOME (Fix Not Found)
# =========================
@app.get("/")
def home():
    return {
        "status": "MarketMindAI Running 🚀",
        "endpoints": [
            "/api/coins",
            "/api/ai"
        ]
    }