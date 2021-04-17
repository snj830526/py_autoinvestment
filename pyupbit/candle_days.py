import requests
import pyupbit


# 일 캔들 조회(어제, 오늘)
def get_candle_data(market=""):
    url = "https://api.upbit.com/v1/candles/days"
    querystring = {"market": market, "count": "2"}
    response = requests.request("GET", url, params=querystring)
    return response.json()


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
    # 현재 코인 단가가 목표가 보다 높고 단가가 1원 이상인 코인만 필터
    if current_price > target_price and pyupbit.get_today_opening_price(d) > 1:
        coin_info = '현재가 : ' + str(current_price) + '-' + market + "(" + market_name + "-" + \
                    str(pyupbit.get_change_rate(d)) + '%' + ")" + ' / opening_p : ' + \
                    str(pyupbit.get_today_opening_price(d)) + ' / high_p(오늘[어제]) : ' + \
                    str(pyupbit.get_today_high_price(d)) + '[' + str(pyupbit.get_yesterday_high_price(d)) + '] / low_p(오늘[어제]) : ' + \
                    str(pyupbit.get_today_low_price(d)) + '[' + str(pyupbit.get_yesterday_low_price(d)) + '] / prev_p : ' + \
                    str(pyupbit.get_yesterday_close_price(d)) + ' / change_p : ' + \
                    str(pyupbit.get_change_price(d))
        print(coin_info)
        return {pyupbit.get_change_rate(d): market}
    else:
        return None


# 목표 코인 단가 계산
def get_target_price_to_buy(market="KRW-BTC"):
    d = get_candle_data(market)
    return d[0]['opening_price'] + (d[1]['high_price'] - d[1]['low_price']) * 0.5