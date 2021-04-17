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
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def test_print():
    data = pyupbit.all_market_names.view_market_names()
    #for d in data:
    #    print(d)


def test_candle_min_loop():
    market_codes = pyupbit.all_market_names.view_market_codes()
    for code in market_codes:
        candle_data = pyupbit.view_candle_min(code)
        print(candle_data)
        time.sleep(5)


def test_candle_day_loop():
    market_codes = pyupbit.all_market_names.view_market_codes()
    market_names = pyupbit.all_market_names.view_market_names()
    print('오늘 날짜는? ' + str(datetime.today()))
    i = 0
    investable_coins = []
    for code in market_codes:
        coin = pyupbit.view_candle_day(code, market_names[i])
        if coin is not None:
            investable_coins.append(coin)
        time.sleep(0.3)
        i = i + 1
    investable_coins.sort(reverse=True)
    best_coin = ""
    for coin in investable_coins:
        best_coin = coin.split(':')[1]
    print('best_coin ::: ' + best_coin)
    test_order(best_coin)


def test_order(market="KRW-DOGE"):
    data = pyupbit.get_coin_investablity(market)
    account_money = float(data['bid_account']['balance']) - 5000
    coin_price = float(pyupbit.view_candle_min(market)[0]['trade_price'])
    coin_count = account_money / coin_price
    print(account_money, coin_price, round(coin_count, 2))
    pyupbit.order_coin(market, coin_price, coin_count, 'bid')


def profit_check_and_order():
    while True:
        my_investment = pyupbit.get_my_coin_info()
        for key in my_investment.keys():
            coin_candle = pyupbit.view_candle_min(key)
            buy_unit_price = float(my_investment[key][0])
            balance = float(my_investment[key][1])
            current_unit_price = float(coin_candle[0]['trade_price'])
            profit_rate = round((current_unit_price / buy_unit_price * 100), 2)
            slack_message1 = f"코인명 ::: {key}, 매수단가 ::: {buy_unit_price}, 현재단가 ::: {current_unit_price}, 수익률 ::: {str(profit_rate)}%"
            print(slack_message1)
            available_coin_amount = 5000 / current_unit_price
            print(f"거래 할 코인 수 ::: {available_coin_amount}")
            if profit_rate <= 85:
                pyupbit.order_5000(key, available_coin_amount, 'bid')
                pyupbit.send_message('#myinvestment', '[Buying!!]' + slack_message1)
                print('buy!!')
            elif profit_rate >= 100:
                pyupbit.order_5000(key, available_coin_amount, 'ask')
                pyupbit.send_message('#myinvestment', '[Selling!!]' + slack_message1)
                print('sell!!')
            else:
                pyupbit.send_message('#myinvestment', '[Thinking...]' + slack_message1)
                print('thinking...')
        time.sleep(5)

"""
def test_sell():
    pyupbit.order_5000('KRW-DOGE', 11.037527593818984, 'ask')
    print('test')
"""

if __name__ == '__main__':
    test_print()
    profit_check_and_order()
    # pyupbit.send_message('#myinvestment', 'test')
    #pyupbit.get_my_coin_info()
    #test_order()
    #test_candle_day_loop()
    #print(pyupbit.view_candle_min('KRW-DOGE'))
    # pyupbit.view_candle_day('KRW-DOGE', '도지코인')

