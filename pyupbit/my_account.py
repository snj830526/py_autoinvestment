import uuid
import jwt
import requests
import pyupbit


# 내 계좌 정보 조회
def get_my_account():
    payLoad = {
        'access_key': pyupbit.get_access_key(),
        'nonce': str(uuid.uuid4())
    }

    jwt_token = jwt.encode(payLoad, pyupbit.get_secret_key())
    authorized_token = 'Bearer {}'.format(jwt_token)
    headers = {'Authorization': authorized_token}

    response = requests.request("GET", pyupbit.get_site_url() + '/v1/accounts', headers=headers)

    return response.json()


# 내가 가진 코인 요약 정보 조회(코인 1개만 처리)
def get_my_coin_info():
    account = get_my_account()
    if len(account) > 1:
        krw_balance = account[0]['balance']
        market_name = account[1]['unit_currency'] + '-' + account[1]['currency']
        buy_price = account[1]['avg_buy_price']
        balance = account[1]['balance']
        result = {market_name: [buy_price, balance, krw_balance]}
        print(f"내 계좌 요약 정보 ::: {result}")
        return result
    else:
        return None
