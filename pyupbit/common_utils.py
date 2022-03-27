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


def check_my_investment():
    profit_rate = 0
    myinfo_map = pyupbit.get_my_coin_info()

    if myinfo_map is not None:
        # 코인명
        market = pyupbit.get_my_coin_name(myinfo_map)
        # 내가 매수 한 코인 단가
        buy_unit_price = pyupbit.get_my_coin_unit_price(myinfo_map)
        # 분단위 캔들
        coin_info = pyupbit.view_candle_min(market)
        # 코인의 현재 단가(분단위 캔들로 조회)
        current_my_coin_price = pyupbit.get_current_coin_price(coin_info)
        # 현재 수익률
        profit_rate = pyupbit.get_profit_rate(current_my_coin_price, int(buy_unit_price))

    return profit_rate <= 100.1


# 수익률 적자여부체크
def check_profit_rate_in_red(profit_rate):
    return profit_rate <= 100


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


# 일 캔들에서 값 추출(어제 거래량)
def get_today_trade_volume(candle):
    return candle[0]['candle_acc_trade_volume']


# 일 캔들에서 값 추출(어제 거래 금액)
def get_today_trade_amount(candle):
    return candle[0]['candle_acc_trade_price']


# 일 캔들에서 값 추출(오늘 고가)
def get_yesterday_high_price(candle):
    return candle[1]['high_price']


# 일 캔들에서 값 추출(오늘 저가)
def get_today_low_price(candle):
    return candle[0]['low_price']


# 일 캔들에서 값 추출(어제 거래량)
def get_yesterday_trade_volume(candle):
    return candle[1]['candle_acc_trade_volume']


# 일 캔들에서 값 추출(어제 거래 금액)
def get_yesterday_trade_amount(candle):
    return candle[1]['candle_acc_trade_price']


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


# map의 key, value 위치 swap
def reverse_map(old_dict):
    return dict([(value, key) for key, value in old_dict.items()])


# 지난 번 투자할만한 코인 맵
def get_prev_dict(investable_map, all_market_codes, all_market_names):
    if dict(investable_map):
        return investable_map
    else:
        return pyupbit.get_investable_coin_map(all_market_codes, all_market_names)


# 캔들 상태 조회
def is_plus_candle(prev_price, current_price):
    return True if prev_price < current_price else False


# 내가 보유 한 코인의 가치 조회
def get_my_value(unit_price, coin_quantity):
    return float(unit_price) * float(coin_quantity)
