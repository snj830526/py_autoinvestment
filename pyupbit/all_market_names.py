import requests


def view_market_codes():
    url = "https://api.upbit.com/v1/market/all"
    queryString = {"isDetail":"true"}
    response = requests.request("GET", url, params=queryString)
    data = response.json()
    arr = []
    for d in data:
        if 'USDT' not in d['market'] and 'BTC' not in d['market']:
            arr.append(d['market'])
    return arr


def view_market_names():
    url = "https://api.upbit.com/v1/market/all"
    queryString = {"isDetail":"true"}
    response = requests.request("GET", url, params=queryString)
    data = response.json()
    arr = []
    for d in data:
        arr.append(d['korean_name'])
    return arr