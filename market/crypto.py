import requests
import time

CACHE = {
    "data": None,
    "time": 0
}

CACHE_TTL = 30  # ثانیه


COINS = "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,cardano,tron,chainlink,avalanche-2"


def get_prices():
    now = time.time()

    # ✅ اگر کش هنوز معتبره
    if CACHE["data"] and now - CACHE["time"] < CACHE_TTL:
        return CACHE["data"]

    url = (
        "https://api.coingecko.com/api/v3/coins/markets"
        f"?vs_currency=usd&ids={COINS}&price_change_percentage=24h"
    )

    try:
        response = requests.get(url, timeout=10)

        # ❌ اگر rate limit خورد
        if response.status_code == 429:
            return CACHE["data"] or {
                "coins": [],
                "time": "Rate Limited",
                "gainer": {"symbol": "--", "change": 0},
                "loser": {"symbol": "--", "change": 0}
            }

        response.raise_for_status()
        data = response.json()

        coins = []
        for i, c in enumerate(data):
            coins.append({
                "symbol": c["symbol"].upper(),
                "name": c["name"],
                "price": round(c["current_price"], 4),
                "change": round(c.get("price_change_percentage_24h", 0), 2),
                "image": c["image"],
                "rank": c.get("market_cap_rank", i + 1)
            })

        # 🏆 بهترین و بدترین
        sorted_coins = sorted(coins, key=lambda x: x["change"], reverse=True)

        result = {
            "coins": coins,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "gainer": sorted_coins[0] if sorted_coins else {},
            "loser": sorted_coins[-1] if sorted_coins else {}
        }

        # 💾 ذخیره در کش
        CACHE["data"] = result
        CACHE["time"] = now

        return result

    except Exception as e:
        return CACHE["data"] or {
            "coins": [],
            "time": "Error",
            "gainer": {"symbol": "--", "change": 0},
            "loser": {"symbol": "--", "change": 0}
        }


def get_price(coin_id: str):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_id}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 429:
            return {"coin": coin_id, "price": "Rate Limited"}

        r.raise_for_status()
        data = r.json()

        if not data:
            return {"coin": coin_id, "price": "Not Found"}

        c = data[0]

        return {
            "coin": c["name"],
            "price": c["current_price"]
        }

    except:
        return {"coin": coin_id, "price": "Error"}


def get_bitcoin_chart():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 429:
            return {"error": "rate_limited"}

        r.raise_for_status()
        data = r.json()

        return {
            "prices": data.get("prices", [])
        }

    except:
        return {"error": "failed"}