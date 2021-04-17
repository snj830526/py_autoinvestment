import pyupbit


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


# 일 캔들에서 값 추출(코인 코드)
def get_market(candle):
    return candle[0]['market']


# 일 캔들에서 값 추출(현재 코인 단가)
def get_current_coin_price(candle):
    return pyupbit.view_candle_min(candle[0]['market'])[0]['trade_price']


# 일 캔들에서 값 추출(오늘 시작 코인 단가)
def get_today_opening_price(candle):
    return candle[0]['opening_price']


# 일 캔들에서 값 추출(변동률)
def get_change_rate(candle):
    return round(candle[0]['change_rate'] * 100, 2)


# 일 캔들에서 값 추출(오늘 고가)
def get_today_high_price(candle):
    return candle[0]['high_price']


# 일 캔들에서 값 추출(오늘 고가)
def get_yesterday_high_price(candle):
    return candle[1]['high_price']


# 일 캔들에서 값 추출(오늘 저가)
def get_today_low_price(candle):
    return candle[0]['low_price']


# 일 캔들에서 값 추출(어제 저가)
def get_yesterday_low_price(candle):
    return candle[1]['low_price']


# 일 캔들에서 값 추출(어제 마감가)
def get_yesterday_close_price(candle):
    return candle[0]['prev_closing_price']


def get_change_price(candle):
    return candle[0]['change_price']