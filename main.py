from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from market.crypto import get_price
from market.crypto import get_price, get_prices

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):

    coins = get_prices()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "coins": coins
        }
    )

@app.get("/btc")
def btc():
    return get_price("bitcoin")


@app.get("/crypto/{coin}")
def crypto(coin: str):
    return get_price(coin)