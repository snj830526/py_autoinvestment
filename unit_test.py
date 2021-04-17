import pyupbit


def test1():
    print('test')


def util_test():
    print('teststart')
    print(pyupbit.view_market_codes())
    key = 'KRW-NEO'
    coin_candle = pyupbit.view_candle_min(key)
    my_investment = pyupbit.get_my_coin_info()
    my_coin_balance = pyupbit.get_my_coin_total_amount(my_investment)
    available_coin_amount = pyupbit.get_possible_order_volume(coin_candle)
    pyupbit.order_10000(key, my_coin_balance, 'ask')


if __name__ == '__main__':
    test1()
    util_test()
