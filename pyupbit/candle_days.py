import requests
import pyupbit


# 일 캔들 조회(어제, 오늘)
def get_candle_data(market=""):
    url = f"{pyupbit.get_site_url()}/v1/candles/days"
    # url = f'{pyupbit.get_site_url()}/v1/candles/minutes/{5}'
    querystring = {"market": market, "count": "2"}
    response = requests.request("GET", url, params=querystring)
    return response.json()


def get_minute_candle_data(market='', minute=5, count=3):
    url = f'{pyupbit.get_site_url()}/v1/candles/minutes/{minute}'
    querystring = {"market": market, "count": f"{count}"}
    response = requests.request("GET", url, params=querystring)
    return response.json()
