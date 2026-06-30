import requests

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    response = requests.get(url, timeout=10)

    data = response.json()

    return data["bitcoin"]["usd"]