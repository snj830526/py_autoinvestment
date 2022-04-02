import hashlib
import uuid
from urllib.parse import urlencode

import jwt
import requests

import pyupbit


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
        'access_key': pyupbit.get_access_key(),
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, pyupbit.get_secret_key()).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(pyupbit.get_site_url() + "/v1/orders/chance", params=query, headers=headers)

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
        'access_key': pyupbit.get_access_key(),
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, pyupbit.get_secret_key()).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    print(f'현재 주문 금액은? {order_money * order_volume} order_money ::: {order_money} order_volume ::: {order_volume}')

    res = requests.post(pyupbit.get_site_url() + "/v1/orders", params=query, headers=headers)
    print(f'주문결과 ::: {res.json()}')
    return res


# 코인 10,000원 어치 매수 / 코인 수 만큼 매도(사용 안함)
def order_10000(market_name="KRW-BTC", order_volume=0, order_type='bid'):
    if order_type == 'bid':
        order_money = 10000 / order_volume
    else:
        print(f'대상코인현재정보 ::: {pyupbit.view_candle_min(market_name)}')
        order_money = pyupbit.get_current_coin_price(pyupbit.view_candle_min(market_name))
    return order_coin(market_name, order_money, order_volume, order_type)


# 내 계좌에 있는 코인 전부 매도(수익률에 따라 전량 매도 할지 결정하도록 변경)
def sell_all():
    # config.json 자동 매도 기능 허용 여부 확인
    if pyupbit.get_auto_sell() == 'YES':
        myinfo_map = pyupbit.get_my_coin_info()

        if myinfo_map is not None:
            # 코인명
            market = pyupbit.get_my_coin_name(myinfo_map)
            # 내가 구매 한 코인 수
            my_coin_amount = pyupbit.get_my_coin_total_amount(myinfo_map)
            # 분단위 캔들
            coin_info = pyupbit.view_candle_min(market)
            # 코인의 현재 단가(분단위 캔들로 조회)
            current_my_coin_price = pyupbit.get_current_coin_price(coin_info)

            order_price = current_my_coin_price
            order_volume = my_coin_amount
            order_type = 'ask'

            # 전량 매도!
            order_coin(
                market_name=market,
                order_money=order_price,
                order_volume=order_volume,
                type=order_type
            )
    # else:
    #     pyupbit.send_message(pyupbit.get_slack_channel(), '자동 매도 기능을 허용하지 않았습니다. \ninvest_helper에게 요청 하세요.')


# 가장 좋을 것 같은 코인 매수
def order_best_coin(best_coin='', order_amount=0):
    coin_info = pyupbit.view_candle_min(best_coin)
    order_volume = pyupbit.get_possible_order_volume(coin_info, order_amount)
    order_money = round(order_amount / order_volume, 1)
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
            'access_key': pyupbit.get_access_key(),
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, pyupbit.get_secret_key()).decode('utf8')
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.delete(pyupbit.get_site_url() + "/v1/order", params=query, headers=headers)
        print(f'주문취소결과 ::: {res.json()}')
    else:
        print(f'주문 uuid ::: {order_uuid} ?!')
