import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests
import json
import pyupbit
from datetime import datetime
import time


file = open('config.json')
config = json.load(file)

access_key = config['access_key']
secret_key = config['secret_key']
site_url = config['site_url']


# 코인이 투자 가능한 상태인지 조회
def get_coin_investablity(market="KRW-BTC"):
    query = {
        'market': market,
    }
    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(site_url + "/v1/orders/chance", params=query, headers=headers)

    return res.json()


# 코인 주문(매수, 매도)
def order_coin(market_name="KRW-BTC", order_money=0, order_volume=0, type='bid'):
    query = {
        'market': market_name,
        'side': type,
        'volume': order_volume,
        'price': order_money,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    print(f'현재 주문 금액은? {order_money * order_volume} order_money ::: {order_money} order_volume ::: {order_volume}')

    res = requests.post(site_url + "/v1/orders", params=query, headers=headers)
    print(f'주문결과 ::: {res.json()}')


# 코인 10,000원 어치 매수 / 코인 수 만큼 매도
def order_10000(market_name="KRW-BTC", order_volume=0, type='bid'):
    if type == 'bid':
        order_money = 10000 / order_volume
    else:
        print(f'대상코인현재정보 ::: {pyupbit.view_candle_min(market_name)}')
        order_money = pyupbit.get_current_coin_price(pyupbit.view_candle_min(market_name))
    order_coin(market_name, order_money, order_volume, type)


# 내 계좌에 있는 코인 전부 매도
def sell_all():
    myinfo_map = pyupbit.get_my_coin_info()

    if myinfo_map is not None:
        market = pyupbit.get_my_coin_name(myinfo_map)
        coin_info = pyupbit.view_candle_min(market)

        current_my_coin_price = pyupbit.get_current_coin_price(coin_info)
        my_coin_amount = pyupbit.get_my_coin_total_amount(myinfo_map)

        order_price = current_my_coin_price
        order_volume = my_coin_amount
        type = 'ask'

        # 전량 매도!
        order_coin(
            market_name=market,
            order_money=order_price,
            order_volume=order_volume,
            type=type
        )


# 거래 가능한 코인 중 가장 좋을 것 같은 코인 조회
def get_best_coin_name():
    investable_coins_map = {}
    market_codes = pyupbit.all_market_names.view_market_codes()
    market_names = pyupbit.all_market_names.view_market_names()
    print('오늘 날짜는? ' + str(datetime.today()))
    while True:
        i = 0
        for code in market_codes:
            coin = pyupbit.view_candle_day(code, market_names[i])
            if coin is not None:
                investable_coins_map.update(coin)
            time.sleep(0.3)
            i = i + 1
        investable_coins_map = sorted(investable_coins_map.items(), reverse=True)
        best_coin = list(investable_coins_map[0])[1]
        coin_dynamic_rate = list(investable_coins_map[0])[0]
        slack_message = f"best_coin ::: {best_coin} / change_rate ::: {coin_dynamic_rate}%"
        print(slack_message)
        pyupbit.send_message('myinvestment', slack_message)
        return best_coin


# 가장 좋을 것 같은 코인 매수
def order_best_coin(best_coin=''):
    coin_info = pyupbit.view_candle_min(best_coin)
    order_volume = pyupbit.get_possible_order_volume(coin_info, 50000)
    order_money = (50000 / order_volume)
    print(f'첫 구매 ::: unit_price : {order_money}, amount : {order_volume}')
    # 50,000원 어치 매수
    pyupbit.order_coin(
        market_name=best_coin,
        order_money=order_money,
        order_volume=order_volume,
        type='bid'
    )