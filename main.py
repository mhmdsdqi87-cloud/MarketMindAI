from fastapi import FastAPI
import requests
import time

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