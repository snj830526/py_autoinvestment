import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests
import configparser


config = configparser.ConfigParser()
config.read('config.json')

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
    print(f'주문결과 ::: {res}')


def order_5000(market_name="KRW-BTC", order_volume=0, type='bid'):
    order_coin(market_name, 5000, order_volume, type)
