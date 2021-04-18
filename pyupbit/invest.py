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
    return res


# 코인 10,000원 어치 매수 / 코인 수 만큼 매도(사용 안함)
def order_10000(market_name="KRW-BTC", order_volume=0, type='bid'):
    if type == 'bid':
        order_money = 10000 / order_volume
    else:
        print(f'대상코인현재정보 ::: {pyupbit.view_candle_min(market_name)}')
        order_money = pyupbit.get_current_coin_price(pyupbit.view_candle_min(market_name))
    return order_coin(market_name, order_money, order_volume, type)


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


# 투자해도 될 것 같은 코인 조회
def get_investable_coin_map(market_codes=[], market_names=[]):
    investable_coins_map = {}
    i = 0
    for code in market_codes:
        # coin = { 전날 대비 변동률 : 코인 코드 }
        coin = pyupbit.view_candle_day(code, market_names[i])
        if coin is not None:
            investable_coins_map.update(coin)
        time.sleep(0.3)
        i = i + 1
    return investable_coins_map


# 거래 가능한 코인 중 가장 좋을 것 같은 코인 조회
def get_best_coin_name(investable_coins_map={}, prev_coins_map={}):
    print('오늘 날짜는? ' + str(datetime.today()))
    while True:
        if dict(investable_coins_map):
            reverse_new_map = reverse_map(investable_coins_map)
            print(f'reverse_new_map ::: {reverse_new_map}')
            if dict(prev_coins_map):
                reverse_old_map = reverse_map(prev_coins_map)
                print(f'reverse_old_map ::: {reverse_old_map}')
                # 코인 맵에서 이전 상승률 보다 상승률이 낮은 코인 제거
                filtered_map = map_filtering(reverse_old_map, reverse_new_map)
                print(f'original_map :: {reverse_new_map} / filtered_map :: {filtered_map}')
                investable_coins_map = reverse_map(filtered_map)

            if dict(investable_coins_map):
                coins_map = sorted(investable_coins_map.items(), reverse=True)
                best_coin = list(coins_map[0])[1]
                coin_dynamic_rate = list(coins_map[0])[0]
                slack_message = f"best_coin ::: {best_coin} / change_rate ::: {coin_dynamic_rate}%"
                print(slack_message)
                pyupbit.send_message('#myinvestment', slack_message)
                return best_coin
        else:
            print(f'아직 사지지 않았습니다. 30초 후 다시 초기화 작업 시작합니다..')
            time.sleep(30)
            return get_best_coin_name(investable_coins_map)


# map의 key, value 위치 swap
def reverse_map(old_dict):
    return dict([(value, key) for key, value in old_dict.items()])


# 맵 객체 값으로 필터링(수익률 필터링)
def map_filtering(original_map, new_map):
    bad_arr = []
    for old_key, old_value in original_map.items():
        if old_key in new_map:
            new_value = new_map[old_key]
            if old_value > new_value:
                bad_arr.append(old_key)
    for old_key in bad_arr:
        original_map.pop(old_key, None)
    return original_map


# 가장 좋을 것 같은 코인 매수
def order_best_coin(best_coin=''):
    coin_info = pyupbit.view_candle_min(best_coin)
    order_volume = pyupbit.get_possible_order_volume(coin_info, 50000)
    order_money = (50000 / order_volume)
    print(f'잘 될 것 같은 코인 구매 ::: unit_price : {order_money}, amount : {order_volume}')
    # 50,000원 어치 매수
    return pyupbit.order_coin(
        market_name=best_coin,
        order_money=order_money,
        order_volume=order_volume,
        type='bid'
    )


# 주문 취소(동작 하지 않음)
def cancel_order(order_uuid=''):
    if order_uuid:
        query = {
            'uuid': order_uuid,
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

        res = requests.delete(site_url + "/v1/order", params=query, headers=headers)
        print(f'주문취소결과 ::: {res.json()}')
    else:
        print(f'주문 uuid ::: {order_uuid} ?!')
