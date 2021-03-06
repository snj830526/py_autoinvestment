import requests


# 원화로 거래 가능한 코인 코드 전체 조회
def view_market_codes():
    data = get_market_data()
    arr = []
    for d in data:
        if 'USDT' not in d['market'] and 'BTC' not in d['market']:
            arr.append(d['market'])
    return arr


# 원화로 거래 가능한 코인명 전체 조회
def view_market_names():
    data = get_market_data()
    arr = []
    for d in data:
        if 'USDT' not in d['market'] and 'BTC' not in d['market']:
            arr.append(d['korean_name'])
    return arr


# 공통 부분 묶음
def get_market_data():
    url = "https://api.upbit.com/v1/market/all"
    query_string = {"isDetail": "true"}
    response = requests.request("GET", url, params=query_string)
    return response.json()
