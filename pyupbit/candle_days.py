import requests
import pyupbit


def get_candle_data(market=""):
    url = "https://api.upbit.com/v1/candles/days"
    querystring = {"market": market, "count": "2"}
    response = requests.request("GET", url, params=querystring)
    return response.json()


def view_candle_day(market="KRW-BTC", market_name=""):
    d = get_candle_data(market)
    return get_rocketboosting_coins(d, market_name)


def get_rocketboosting_coins(candle_data, market_name):
    d = candle_data
    target_price = d[0]['opening_price'] + (d[1]['high_price'] - d[1]['low_price']) * 0.5
    current_price = pyupbit.view_candle_min(d[0]['market'])[0]['trade_price']
    #print(f'target_price ::: {target_price} / current_price ::: {current_price} / opening_price ::: {d[0]["opening_price"]}')
    if current_price > target_price and d[0]['opening_price'] > 1:
        coin_info = '현재가 : ' + str(current_price) + '-' + d[0]['market'] + "(" + market_name + "-" + \
                    str(round(d[0]['change_rate'] * 100, 2)) + '%' + ")" + ' / opening_p : ' + \
                    str(d[0]['opening_price']) + ' / high_p(오늘[어제]) : ' + \
                    str(d[0]['high_price']) + '[' + str(d[1]['high_price']) + '] / low_p(오늘[어제]) : ' + \
                    str(d[0]['low_price']) + '[' + str(d[1]['low_price']) + '] / prev_p : ' + \
                    str(d[0]['prev_closing_price']) + ' / change_p : ' + \
                    str(d[0]['change_price'])
        print(coin_info)
        return {round(d[0]['change_rate'] * 100, 2): d[0]['market']}
    else:
        return None


def get_target_price_to_buy(market="KRW-BTC"):
    d = get_candle_data(market)
    return d[0]['opening_price'] + (d[1]['high_price'] - d[1]['low_price']) * 0.5