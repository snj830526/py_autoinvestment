import pyupbit
import time
from datetime import datetime


def test1():
    print('test')


def util_test():
    print('teststart')
    print(pyupbit.view_market_names())


def test_candle_min_loop():
    market_codes = pyupbit.all_market_names.view_market_codes()
    for code in market_codes:
        candle_data = pyupbit.view_candle_min(code)
        print(candle_data)
        time.sleep(5)


def test_order(market="KRW-DOGE"):
    data = pyupbit.get_coin_investablity(market)
    account_money = float(data['bid_account']['balance']) - 5000
    coin_price = float(pyupbit.view_candle_min(market)[0]['trade_price'])
    coin_count = account_money / coin_price
    print(account_money, coin_price, round(coin_count, 2))
    pyupbit.order_coin(market, coin_price, coin_count, 'bid')


def test_sort():
    map = {}

    arr = [
        {-6.8: 'USDT-ETC'},
        {-11.71: 'KRW-IOST'},
        {-24.91: 'KRW-DMT'},
        {-7.74: 'KRW-IQ'},
        {-16.12: 'KRW-QKC'},
        {-11.32: 'KRW-BTT'}
    ]

    for a in arr:
        map.update(a)
    sorted_map = sorted(map.items(), reverse=True)
    print(f'결과 ::: {sorted_map}')
    keys = list(sorted_map[0])[1]
    print(keys)
    #for key, value in map.items():
    #    print(key)


def test_profit_rate():
    print('test start')
    my_investment = pyupbit.get_my_coin_info()
    current_coin = pyupbit.view_candle_min(list(my_investment.keys())[0])
    current_coin_price = pyupbit.get_current_coin_price(current_coin)
    print(f'my_investment ::: {my_investment} / current_coin_info ::: {current_coin_price}')
    day_candle = pyupbit.view_candle_day('KRW-IQ', 'test')
    print(f'day ::: {day_candle}')


def test_best_coin():
    investable_coins_map = {}
    market_codes = pyupbit.all_market_names.view_market_codes()
    market_names = pyupbit.all_market_names.view_market_names()
    i = 0
    for code in market_codes:
        coin = pyupbit.view_candle_day(code, market_names[i])
        if coin is not None:
            print(f'all coins ::: {coin}')
            investable_coins_map.update(coin)
        time.sleep(0.5)
        i = i + 1
    investable_coins_map = sorted(investable_coins_map.items(), reverse=True)
    print(f'coins ::: {investable_coins_map}')
    best_coin = list(investable_coins_map[0])[1]
    coin_dynamic_rate = list(investable_coins_map[0])[0]
    slack_message = f"best_coin ::: {best_coin} / change_rate ::: {coin_dynamic_rate}%"
    print(slack_message)
    print(f'best coin 결과 ::: {best_coin}')


if __name__ == '__main__':
    test_sort()
