import requests
import time

CACHE = None
LAST_UPDATE = 0
CACHE_TIME = 60  # هر 60 ثانیه یک بار آپدیت

COINS_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_from_api():
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,cardano,tron,chainlink,avalanche-2",
        "price_change_percentage": "24h"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i in range(3):  # retry 3 بار
        try:
            res = requests.get(COINS_URL, params=params, headers=headers, timeout=10)

            if res.status_code == 200:
                return res.json()

            # اگر rate limit شد
            if res.status_code == 429:
                time.sleep(2)

        except Exception as e:
            print("API Error:", e)
            time.sleep(2)

    return []


def get_prices():
    global CACHE, LAST_UPDATE

    now = time.time()

    # 🔥 اگر cache هنوز معتبره
    if CACHE and (now - LAST_UPDATE) < CACHE_TIME:
        return CACHE

    data = fetch_from_api()

    coins = []

    for c in data:
        try:
            coins.append({
                "symbol": c.get("symbol", "").upper(),
                "name": c.get("name", ""),
                "price": c.get("current_price", 0),
                "change": c.get("price_change_percentage_24h", 0),
                "image": c.get("image", ""),
                "rank": c.get("market_cap_rank", 0)
            })
        except:
            continue

    if not coins:
        result = {
            "coins": [],
            "time": "API Loading...",
            "gainer": {"symbol": "-", "change": 0},
            "loser": {"symbol": "-", "change": 0}
        }
    else:
        result = {
            "coins": coins,
            "time": time.strftime("%H:%M:%S"),
            "gainer": max(coins, key=lambda x: x["change"]),
            "loser": min(coins, key=lambda x: x["change"])
        }

    CACHE = result
    LAST_UPDATE = now

    return result


def get_price(coin_id: str):
    data = fetch_from_api()

    for c in data:
        if c["id"] == coin_id:
            return {
                "symbol": c["symbol"].upper(),
                "price": c["current_price"],
                "change": c["price_change_percentage_24h"]
            }

    return None


def get_bitcoin_chart():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

    params = {
        "vs_currency": "usd",
        "days": 1
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        prices = data.get("prices", [])

        return {
            "labels": [p[0] for p in prices],
            "values": [p[1] for p in prices]
        }

    except:
        return {
            "labels": [],
            "values": []
        }