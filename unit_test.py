import pyupbit


def test1():
    print('test')


def util_test():
    print('teststart')
    print(pyupbit.view_market_codes())
    best_coin = 'KRW-IOST'
    coin_info = pyupbit.view_candle_min(best_coin)
    print(pyupbit.get_coin_investablity(best_coin))
    pyupbit.order_10000(
        market_name=best_coin,
        order_volume=pyupbit.get_possible_order_volume(coin_info),
        type='bid'
    )


if __name__ == '__main__':
    test1()
    util_test()
