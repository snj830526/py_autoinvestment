from multiprocessing import Process
import time
from datetime import datetime
import pyupbit

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""
def test_print():
    data = pyupbit.all_market_names.view_market_names()
    #for d in data:
    #    print(d)
"""

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
        {25.53: 'USDT-ETC'},
        {11.71: 'KRW-IOST'},
        {8.74: 'KRW-DMT'},
        {21.8: 'KRW-IQ'},
        {9.0: 'KRW-QKC'},
        {17.12: 'KRW-BTT'}
    ]

    for a in arr:
        map.update(a)
    sorted(map.items(), reverse=True)
    print(f'결과 ::: {map}')
    keys = list(map.values())[0]
    print(keys)
    #for key, value in map.items():
    #    print(key)


def profit_check_and_order():
    counter = 0
    while True:
        if counter % 720 == 0:
            # 전 시간에 투자 한 코인 전량 매도
            pyupbit.sell_all()
            print('Finding the best coin to invest...(It runs once in an hour.)')
            print(f"이번시간에 투자할 코인은? {best_coin}")
            # 10000원 어치 매수
            best_coin = pyupbit.get_best_coin_name()
            pyupbit.order_best_coin(best_coin)

        my_investment = pyupbit.get_my_coin_info()
        if my_investment is not None:
            for key in my_investment.keys():
                coin_candle = pyupbit.view_candle_min(key)
                buy_unit_price = pyupbit.get_my_coin_unit_price(my_investment)
                krw_balance = pyupbit.get_my_krw_balance(my_investment)
                my_coin_balance = pyupbit.get_my_coin_total_amount(my_investment)
                current_unit_price = pyupbit.get_current_coin_price(coin_candle)
                profit_rate = pyupbit.get_profit_rate(current_unit_price, buy_unit_price)
                slack_message1 = f"코인명 ::: {key}, 매수단가 ::: {buy_unit_price}, 현재단가 ::: {current_unit_price}, 수익률 ::: {str(profit_rate)}%"
                print(slack_message1)
                if profit_rate <= 85:
                    if krw_balance >= 10000:
                        available_coin_amount = pyupbit.get_possible_order_volume(coin_candle)
                        pyupbit.order_10000(key, available_coin_amount, 'bid')
                        pyupbit.send_message('#myinvestment', f'[Buying!!-{str(datetime.today())}]' + slack_message1)
                        print('buy!!')
                elif profit_rate > 100:
                    available_coin_amount = pyupbit.get_my_coin_total_amount(my_investment)
                    pyupbit.order_10000(key, available_coin_amount, 'ask')
                    pyupbit.send_message('#myinvestment', f'[Selling!!-{str(datetime.today())}]' + slack_message1)
                    print('sell!!')
                else:
                    print('thinking...')
            else:
                # 10000원 어치 매수
                best_coin = pyupbit.get_best_coin_name()
                pyupbit.order_best_coin(best_coin)
        counter = counter + 1
        time.sleep(5)


if __name__ == '__main__':
    profit_check_and_order()

