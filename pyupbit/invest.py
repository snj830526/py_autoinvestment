import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests
import json
import pyupbit

file = open('config.json')
config = json.load(file)

access_key = config['access_key']
secret_key = config['secret_key']
site_url = config['site_url']


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

    res = requests.post(site_url + "/v1/orders", params=query, headers=headers)
    print(f'주문결과 ::: {res.json()}')


def order_5000(market_name="KRW-BTC", order_volume=0, type='bid'):
    order_money = round(5000 / order_volume / 10) * 10
    order_coin(market_name, order_money, order_volume, type)


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
