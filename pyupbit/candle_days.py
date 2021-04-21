import requests
import pyupbit


# 일 캔들 조회(어제, 오늘)
def get_candle_data(market=""):
    url = f"{pyupbit.get_site_url()}/v1/candles/days"
    querystring = {"market": market, "count": "2"}
    response = requests.request("GET", url, params=querystring)
    return response.json()


# 잘 될 것 같은 코인 목록 조회
def view_candle_day(market="KRW-BTC", market_name=""):
    d = get_candle_data(market)
    return pyupbit.get_rocketboosting_coins(d, market_name)

