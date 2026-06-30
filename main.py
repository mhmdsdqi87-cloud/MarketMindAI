from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from market.crypto import get_price, get_prices

app = FastAPI(
    title="TEKA MarketMind AI",
    version="0.5.0"
)

# پوشه فایل‌های استاتیک (CSS، عکس و ...)
app.mount("/static", StaticFiles(directory="static"), name="static")

# پوشه قالب‌های HTML
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


@app.get("/btc")
def btc():
    return get_price("bitcoin")


@app.get("/crypto/{coin}")
def crypto(coin: str):
    return get_price(coin)