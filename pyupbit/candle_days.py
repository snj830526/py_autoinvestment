import requests
import pyupbit
import time


# 일 캔들 조회(어제, 오늘)
def get_candle_data(market=""):
    url = "https://api.upbit.com/v1/candles/days"
    querystring = {"market": market, "count": "2"}
    response = requests.request("GET", url, params=querystring)
    return response.json()


# 코인 변동률 맵 조회(전체)
def get_coin_rate_map(market_codes=[]):
    result_map = {}
    for market in market_codes:
        d = get_candle_data(market)
        # 전날 대비 변동 률
        change_rate = pyupbit.get_change_rate(d)
        result_map.update({market: change_rate})
        time.sleep(0.2)
    return result_map


# 잘 될 것 같은 코인 목록 조회
def view_candle_day(market="KRW-BTC", market_name=""):
    d = get_candle_data(market)
    return get_rocketboosting_coins(d, market_name)


# 잘 될 것 같은 코인 계산
def get_rocketboosting_coins(candle_data, market_name):
    d = candle_data
    # 코인 코드
    market = pyupbit.get_market(d)
    # 목표 코인 단가( 오늘 시작가 + (어제 고가 - 어제 저가) * 0.5 )
    target_price = get_target_price_to_buy(market)
    # 코인 현재 단가
    current_price = pyupbit.get_current_coin_price(d)
    # 전날 대비 변동 률
    change_rate = pyupbit.get_change_rate(d)
    coin_info = pyupbit.get_coin_info_with_candle(d, market_name)
    # 현재 코인 단가가 목표가 보다 높고 단가가 1원 이상인 코인만 필터
    if current_price >= target_price and pyupbit.get_today_opening_price(d) > 1:
        print(coin_info)
        return {change_rate: market}
    else:
        return None


# 목표 코인 단가 계산
def get_target_price_to_buy(market="KRW-BTC"):
    d = get_candle_data(market)
    return d[0]['opening_price'] + (d[1]['high_price'] - d[1]['low_price']) * 0.1