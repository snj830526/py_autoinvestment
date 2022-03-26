import pyupbit
import time
from datetime import datetime


def test1():
    print('test')


def util_test():
    print('teststart')


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
    #day_candle = pyupbit.view_candle_day('KRW-IQ', 'test')
    #print(f'day ::: {day_candle}')


def test_best_coin():
    investable_coins_map = {}
    # market_codes = pyupbit.all_market_names.view_market_codes()
    # market_names = pyupbit.all_market_names.view_market_names()
    i = 0
    # for code in market_codes:
        #coin = pyupbit.view_candle_day(code, market_names[i])
        #if coin is not None:
            #print(f'all coins ::: {coin}')
            #investable_coins_map.update(coin)
        # time.sleep(0.5)
        #i = i + 1
    investable_coins_map = sorted(investable_coins_map.items(), reverse=True)
    print(f'coins ::: {investable_coins_map}')
    best_coin = list(investable_coins_map[0])[1]
    coin_dynamic_rate = list(investable_coins_map[0])[0]
    slack_message = f"best_coin ::: {best_coin} / change_rate ::: {coin_dynamic_rate}%"
    print(slack_message)
    print(f'best coin 결과 ::: {best_coin}')


def test_map_filtering():
    original_map = {'KRW-IOST': 4.95, 'KRW-GAS': 8.73, 'KRW-MOC': 5.8, 'KRW-AHT': 11.9, 'KRW-DOGE': 5.19}
    new_map = {'KRW-IOST': 1.95, 'KRW-GAS': 7.73, 'KRW-MOC': 5.8, 'KRW-AHT': 19.9, 'KRW-DOGE': 1.19}

    bad_arr = []
    for old_key, old_value in original_map.items():
        new_value = new_map[old_key]
        if old_value > new_value:
            print('bad!')
            bad_arr.append(old_key)
        else:
            print('good!!')

    for old_key in bad_arr:
        original_map.pop(old_key, None)

    print(f'bad_arr ::: {bad_arr}, result ::: {original_map}')


def test_process():
    print('process alive!')


def test_init():
    print('init test')
    order_money = 20_000
    my_coin_dict = pyupbit.get_my_coin_info()
    coin_name = ''
    for key, value in my_coin_dict.items():
        coin_name = key
    unit_price = my_coin_dict[coin_name][0]
    quantity = my_coin_dict[coin_name][1]
    coin_value = float(unit_price) * float(quantity)
    print(f'코인 단가 : {unit_price}, 수량 : {quantity}, 가치 : {round(float(unit_price) * float(quantity), 2)}')
    # 분단위 캔들
    coin_info = pyupbit.view_candle_min(coin_name)
    # 내가 매수 한 코인 단가
    buy_unit_price = pyupbit.get_my_coin_unit_price(my_coin_dict)
    # 현재 코인 단가
    current_unit_price = pyupbit.get_current_coin_price(coin_info)
    # 수익률(100%가 매수 시점 단가)
    profit_rate = pyupbit.get_profit_rate(current_unit_price, buy_unit_price)
    print(f'매수시 코인 단가 : {buy_unit_price}, 현재코인단가 : {current_unit_price}, 수익률 : {profit_rate}')
    if profit_rate > 100:
        print('팔기')
    else:
        print('버티기')


if __name__ == '__main__':
    test_init()
