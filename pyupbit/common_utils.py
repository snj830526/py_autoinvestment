# 분 단위 코인정보로 현재 코인 단가 추출(매입, 매도 시 코인 단가 추출용)
def get_current_coin_price(coin_info=[]):
    return float(coin_info[0]['trade_price'])


# 내가 소유 한 코인 이름
def get_my_coin_name(myinfo_map={}):
    return list(myinfo_map.keys())[0]


# 내가 매입 한 코인 단가
def get_my_coin_unit_price(myinfo_map):
    return float(myinfo_map[get_my_coin_name(myinfo_map)][0])


# 내가 소유 한 코인 수
def get_my_coin_total_amount(myinfo_map={}):
    return float(myinfo_map[get_my_coin_name(myinfo_map)][1])


# 가용한 자금
def get_my_krw_balance(myinfo_map):
    return float(myinfo_map[get_my_coin_name(myinfo_map)][2])


# 주문 가능 수량
def get_possible_order_volume(coin_info=[]):
    unit_price = get_current_coin_price(coin_info)
    if unit_price == 0:
        return 0
    else:
        return float(10000 / unit_price)


# 수익률 계산
def get_profit_rate(current_unit_price=0, buy_unit_price=0):
    if buy_unit_price == 0:
        return 0
    else:
        return round((current_unit_price / buy_unit_price * 100), 2)
