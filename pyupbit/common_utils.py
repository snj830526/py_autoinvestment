import pyupbit


# 분 단위 코인정보로 현재 코인 단가 추출(매입, 매도 시 코인 단가 추출용 - 0.01% 싸게 구매해보기!)
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
def get_possible_order_volume(coin_info=[], order_money=10000):
    unit_price = get_current_coin_price(coin_info)
    if unit_price == 0:
        return 0
    else:
        return float(order_money / unit_price)


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


# 일 캔들에서 값 추출(변동 가격)
def get_change_price(candle):
    return candle[0]['change_price']


# 매수 주문 uuid 추출
def get_order_bid_uuid(response_json):
    if 'uuid' in response_json:
        return response_json["uuid"]
    else:
        return None


def get_coin_info_with_candle(d, market_name):
    # 코인 코드
    market = pyupbit.get_market(d)
    # 목표 코인 단가( 오늘 시작가 + (어제 고가 - 어제 저가) * 0.5 )
    target_price = pyupbit.get_target_price_to_buy(market)
    # 코인 현재 단가
    current_price = pyupbit.get_current_coin_price(d)
    coin_info = f"""목표가: {target_price} / 현재가: {str(current_price)} - {market} ({market_name}:{str(pyupbit.get_change_rate(d))}%) opening_p:{str(pyupbit.get_today_opening_price(d))} high_p(오늘[어제]):{str(pyupbit.get_today_high_price(d))}[{str(pyupbit.get_yesterday_high_price(d))}] low_p(오늘[어제]):{str(pyupbit.get_today_low_price(d))}[{str(pyupbit.get_yesterday_low_price(d))}] prev_p:{str(pyupbit.get_yesterday_close_price(d))} change_p:{str(pyupbit.get_change_price(d))}"""
    return coin_info


# 목표 코인 단가 계산
def get_target_price_to_buy(market="KRW-BTC"):
    d = pyupbit.get_candle_data(market)
    return d[0]['opening_price'] + (d[1]['high_price'] - d[1]['low_price']) * 0.5


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
        new_map.pop(old_key, None)
    return new_map
