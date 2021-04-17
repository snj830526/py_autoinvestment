import pyupbit
import time


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
        {6.8: 'USDT-ETC'},
        {11.71: 'KRW-IOST'},
        {24.91: 'KRW-DMT'},
        {7.74: 'KRW-IQ'},
        {16.12: 'KRW-QKC'},
        {11.32: 'KRW-BTT'}
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


if __name__ == '__main__':
    test_profit_rate()
