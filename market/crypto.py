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

    return {
        "coins": coins,
        "time": datetime.now().strftime("%H:%M:%S")
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

    data = response.json()

    return {
        "coin": coin,
        "price": data[coin]["usd"]
    }