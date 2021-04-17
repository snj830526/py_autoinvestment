import uuid
import jwt
import requests
import configparser


config = configparser.ConfigParser()
config.read('config.json')

access_key = config['access_key']
secret_key = config['secret_key']
site_url = config['site_url']


def get_my_account():
    payLoad = {
        'access_key': accessKey,
        'nonce': str(uuid.uuid4())
    }

    jwt_token = jwt.encode(payLoad, secretKey)
    authorized_token = 'Bearer {}'.format(jwt_token)
    headers = {'Authorization': authorized_token}

    response = requests.request("GET", serverUrl + '/v1/accounts', headers=headers)

    return response.json()


def get_my_coin_info():
    account = get_my_account()
    market_name = account[1]['unit_currency'] + '-' +account[1]['currency']
    buy_price = account[1]['avg_buy_price']
    balance = account[1]['balance']
    result = {market_name: [buy_price, balance]}
    print(f"내 계좌 요약 정보 ::: {result}")
    return result
