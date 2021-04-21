import requests
import pyupbit


def view_candle_min(market="KRW-BTC"):
    url = f"{pyupbit.get_site_url()}/v1/candles/minutes/1"
    query_string = {"market": market, "count": "1", "convertingPriceUnit": "KRW"}
    response = requests.request("GET", url, params=query_string)
    return response.json()

