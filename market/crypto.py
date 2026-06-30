import requests
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

COINS = [
    "bitcoin",
    "ethereum",
    "solana",
    "binancecoin",
    "ripple",
    "dogecoin",
    "cardano",
    "tron",
    "chainlink",
    "avalanche-2"
]


def get_prices():
    params = {
        "vs_currency": "usd",
        "ids": ",".join(COINS),
        "price_change_percentage": "24h"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    coins = []

    for coin in data:
        coins.append({
            "name": coin["name"],
            "symbol": coin["symbol"].upper(),
            "price": round(coin["current_price"], 2),
            "change": round(coin["price_change_percentage_24h"], 2),
            "image": coin["image"],
            "market_cap": coin["market_cap"],
            "rank": coin["market_cap_rank"]
        })

    gainer = max(coins, key=lambda x: x["change"])
    loser = min(coins, key=lambda x: x["change"])

    return {
        "coins": coins,
        "time": datetime.now().strftime("%H:%M:%S"),
        "gainer": gainer,
        "loser": loser
    }


def get_price(coin):
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": coin,
            "vs_currencies": "usd"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if coin not in data:
        return {
            "coin": coin,
            "price": None
        }

    return {
        "coin": coin,
        "price": data[coin]["usd"]
    }


def get_bitcoin_chart():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

    params = {
        "vs_currency": "usd",
        "days": "1"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return [round(item[1], 2) for item in data["prices"]]