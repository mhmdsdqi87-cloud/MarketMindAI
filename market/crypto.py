import requests

BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

COINS = [
    "bitcoin",
    "ethereum",
    "solana",
    "binancecoin",
    "ripple"
]

def get_prices():

    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    coins = []

    for coin in COINS:
        coins.append({
            "name": coin.title(),
            "price": data[coin]["usd"]
        })

    return coins


def get_price(coin):

    params = {
        "ids": coin,
        "vs_currencies": "usd"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return {
        "coin": coin,
        "price": data[coin]["usd"]
    }