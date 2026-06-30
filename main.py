from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from market.crypto import get_prices, get_price

app = FastAPI(
    title="TEKA MarketMind AI",
    version="1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):

    market = get_prices()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "coins": market["coins"],
            "time": market["time"]
        }
    )


@app.get("/search")
def search(request: Request, coin: str):

    data = get_price(coin)

    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "coin": data["coin"],
            "price": data["price"]
        }
    )


@app.get("/crypto/{coin}")
def crypto(coin: str):

    return get_price(coin)