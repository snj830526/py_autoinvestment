import json

with open('config.json') as file:
    config = json.load(file)


# 슬랙 채널명
def get_slack_channel():
    return config['slack_channel']


# 슬랙 채널아이디
def get_slack_channel_id():
    return config['slack_channel_id']

# access key
def get_access_key():
    return config['access_key']


# secret_key
def get_secret_key():
    return config['secret_key']


# site_url
def get_site_url():
    return config['site_url']


# slack token
def get_slack_token():
    return config['slack_token']


# main.py path
def get_script_path():
    return config['main_script_path']


# 투자 할 금액
def get_my_order_price():
    return config['my_order_price']


# 자동 매각 기능 허용
def get_auto_sell():
    return config['auto_sell']


# 손절 퍼센트값
def get_force_sell_percent():
    return config['force_sell_percent']


# 구매용 슬랙 봇 토큰
def get_slack_bot_token():
    return config['purchase_slack_bot_token']


# 구매 키워드
def get_purchase_keywords():
    return ['2', '구매', '사라']


class StaticProperties:
    STANDARD_PROFIT_RATE = 100
