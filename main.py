from fastapi import FastAPI
import requests
import time
import random


def ai_analyze_market(coins):
    up = 0
    down = 0

    for c in coins:
        if c["change"] > 0:
            up += 1
        else:
            down += 1

    if up > down:
        trend = "BULLISH 🚀"
        confidence = min(50 + (up * 5), 95)
    else:
        trend = "BEARISH 📉"
        confidence = min(50 + (down * 5), 95)

    return {
        "trend": trend,
        "confidence": confidence
    }
app = FastAPI()

CACHE = {
    "data": None,
    "time": 0
}

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,cardano,tron,chainlink,avalanche-2",
    "price_change_percentage": "24h"
}

CACHE_TIME = 60  # seconds


def fetch_coins():
    try:
        r = requests.get(API_URL, params=PARAMS, timeout=10)

        if r.status_code == 429:
            return CACHE["data"] or []

        return r.json()

    except:
        return CACHE["data"] or []


@app.get("/api/coins")
def get_coins():
    now = time.time()

    if CACHE["data"] and now - CACHE["time"] < CACHE_TIME:
        return CACHE["data"]

    data = fetch_coins()

    CACHE["data"] = data
    CACHE["time"] = now

    return data


@app.get("/")
def home():
    return {"status": "online"}

@app.get("/api/ai")
def ai_status():
    market = get_prices()
    ai = ai_analyze_market(market["coins"])

    return {
        "trend": ai["trend"],
        "confidence": ai["confidence"],
        "time": market["time"]
    }