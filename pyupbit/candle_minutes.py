import requests


def view_candle_min(market="KRW-BTC"):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": market, "count": "1", "convertingPriceUnit": "KRW"}
    response = requests.request("GET", url, params=querystring)
    return response.json()

