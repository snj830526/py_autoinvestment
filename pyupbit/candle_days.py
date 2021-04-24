import requests
import pyupbit


# 일 캔들 조회(어제, 오늘)
def get_candle_data(market=""):
    url = f"{pyupbit.get_site_url()}/v1/candles/days"
    querystring = {"market": market, "count": "2"}
    response = requests.request("GET", url, params=querystring)
    return response.json()
