import pyupbit
import time
from datetime import datetime


# 피봇 기준선 계산
from pyupbit import check_profit_rate_in_red, is_plus_candle


def calc_standard_line(prev_day_high_price, prev_day_low_price, today_open_price):
    return round((prev_day_high_price + prev_day_low_price + today_open_price) / 3, 2)


# 1차 저항선 계산
def first_higher_line(standard_line, prev_day_low_price):
    return round(2 * standard_line - prev_day_low_price, 2)


# 2차 저항선 계산
def second_higher_line(standard_line, prev_day_high_price, prev_day_low_price):
    return round(standard_line + prev_day_high_price - prev_day_low_price, 2)


# 1차 지지선 계산
def first_lower_line(standard_line, prev_day_high_price):
    return round(2 * standard_line - prev_day_high_price, 2)


# 2차 지지선 계산
def second_lower_line(standard_line, prev_day_high_price, prev_day_low_price):
    return round(standard_line - prev_day_high_price + prev_day_low_price, 2)


"""
새로 만들어 보는 계산 식(100% 손해 본 후 다시 짜는 로직)

전체 코인 중 살만한 코인을 고른다(기존의 로직 사용)
내려가고 있는 코인을 사서 기다리는건 어떨까? -> 적용했고 테스트 중

매수 가격에서 올라간다 -> 좋음
매수 가격에서 내려간다 -> 싫음(대부분)

하한선은 있을 필요가 있나?
하한의 기준은?

상한선은 있을 필요가 있나?
상한의 기준은?

매도 기준이 되는 가격은?
1차 지지선?
d = pyupbit.get_candle_data(market)
target_price = d[0]['opening_price'] + (d[1]['high_price'] - d[1]['low_price']) * 0.5
"""


# 투자할 만한 코인인지 검증(현재 가격이 1차 지지선 ~ 2차 지지선 사이에 있는 코인)
def get_investable_coins(market, market_name):
    candle = pyupbit.get_candle_data(market)

    # 어제 거래량
    yesterday_trade_amount = pyupbit.get_yesterday_trade_amount(candle)
    flag_trade_amount = yesterday_trade_amount >= 1_000_000_000
    yesterday_trade_volume = pyupbit.get_yesterday_trade_volume(candle)
    flag_trade_volume = yesterday_trade_volume >= 500_000_000
    if not flag_trade_amount or flag_trade_volume:
        return None

    # 코인 현재 단가
    current_price = pyupbit.get_current_coin_price(candle)
    # 오늘 시가
    today_open_price = pyupbit.get_today_opening_price(candle)
    # 어제 고가
    prev_high_price = pyupbit.get_yesterday_high_price(candle)
    # 어제 저가
    prev_low_price = pyupbit.get_yesterday_low_price(candle)
    # 기준선
    standard_price = pyupbit.calc_standard_line(prev_high_price, prev_low_price, today_open_price)
    # 1차 지지선
    first_low_price = pyupbit.first_lower_line(standard_price, prev_high_price)
    # 2차 지지선
    second_low_price = pyupbit.second_lower_line(standard_price, prev_high_price, prev_low_price)
    # 1차 저항선
    first_high_price = pyupbit.first_higher_line(standard_price, prev_low_price)
    # 2차 저항선
    second_high_price = pyupbit.second_higher_line(standard_price, prev_high_price, prev_low_price)

    # 오늘 거래량
    today_trade_amount = pyupbit.get_today_trade_amount(candle)

    # 15분단위 캔들 5건 조회 해서 /\/\ 모양인 코인 조회
    # is_profitable = False
    # minute_5_candle_list = pyupbit.get_minute_candle_data(market, 15, 5)
    # prev_trade_price = 0
    # prev_change_ratio = 0
    # change_ratio = 0
    # for idx, data in enumerate(minute_5_candle_list):
    #     if idx == 0:
    #         first_trade_price = data['trade_price']
    #         prev_trade_price = first_trade_price
    #         continue
    #     else:
    #         trade_price = data['trade_price']
    #         if prev_trade_price > 0:
    #             change_ratio = abs(round(100 - trade_price / prev_trade_price * 100, 2))
    #             print(f'index :: {market} / {idx} / {prev_trade_price} / {trade_price} / {change_ratio} / {prev_change_ratio}')
    #             if 0 < prev_change_ratio < change_ratio:
    #                 is_profitable = False
    #                 break
    #             prev_change_ratio = change_ratio
    #
    #         if idx % 2 == 1:
    #             if is_plus_candle(prev_trade_price, trade_price):
    #                 is_profitable = True
    #             else:
    #                 is_profitable = False
    #                 break
    #         else:
    #             if not is_plus_candle(prev_trade_price, trade_price):
    #                 is_profitable = True
    #             else:
    #                 is_profitable = False
    #                 break
    #         prev_trade_price = trade_price

    # 15분 봉 기준 3번 하락 한 코인
    minute_candle_list = pyupbit.get_minute_candle_data(market, 5, 6)
    is_profitable = False
    prev_trade_price = 0
    for idx, data in enumerate(minute_candle_list):
        if idx == 0:
            first_trade_price = data['trade_price']
            prev_trade_price = first_trade_price
            continue
        else:
            trade_price = data['trade_price']
            print(f'index :: {market} / {idx} / {prev_trade_price} / {trade_price}')
            if idx <= 2:
                if is_plus_candle(prev_trade_price, trade_price):
                    is_profitable = True
                else:
                    is_profitable = False
                    break
            else:
                if not is_plus_candle(prev_trade_price, trade_price):
                    is_profitable = True
                else:
                    is_profitable = False
                    break
        prev_trade_price = trade_price

    # 코인 정보
    coin_info = pyupbit.get_coin_info_with_candle(candle, market_name)

    # 1차 저항선을 넘은 코인을 대상으로 한다.
    # 1차 지지선을 넘은 코인을 대상으로 한다.
    flag_price = current_price < second_high_price
    flag_low_price = pyupbit.get_today_opening_price(candle) > 1
    # flag_change_ratio = change_ratio > 0.05

    if flag_low_price and flag_price and is_profitable:
        slack_message = f'투자 대상 코인 : {coin_info}'
        print(slack_message)
        #pyupbit.send_message(pyupbit.get_slack_channel(), slack_message)
        return {market: today_trade_amount}
    else:
        # print(f'근거 :: flag_trade_amount={flag_trade_amount} / flag_price={flag_price} / flag_low_price={flag_low_price} \n비대상 ::: {coin_info}')
        return None


# 매도 시점 스코어 기록기
def new_calc_profit_score(happy_score=0, prev_profit_rate=0, current_profit_rate=0):
    # 플러스 변동폭
    plus_change_rate = current_profit_rate - prev_profit_rate
    # 스코어 계산 하기!
    # 수익률 100% 이상
    if not check_profit_rate_in_red(current_profit_rate) and not check_profit_rate_in_red(prev_profit_rate):
        # 상승중!
        if plus_change_rate >= 0:
            happy_score = happy_score + plus_change_rate / 2
        # 하락중! (안돼!!)
        else:
            happy_score = happy_score + plus_change_rate
    # 수익률 100% 미만
    else:
        happy_score = 0
    slack_message = f':meow_code: 현재 스코어는 ::: {round(happy_score, 2)} / 변동폭은 ::: {round(plus_change_rate, 2)}% / 직전 수익률은 ::: {prev_profit_rate}% / 현재 수익률은 ::: {current_profit_rate}%'
    print(slack_message)

    if not check_profit_rate_in_red(current_profit_rate):
        pyupbit.send_message(pyupbit.get_slack_channel(), slack_message)

    if happy_score < 0:
        happy_score = 0

    prev_profit_rate = current_profit_rate

    return happy_score, prev_profit_rate


# 새로운 투자 로직
def new_working(market, my_investment={}, prev_profit_rate=100, score=0, has_minus_exp=False):
    # 일 캔들 조회
    candle = pyupbit.get_candle_data(market)
    # 내가 매수 한 코인 단가
    buy_unit_price = pyupbit.get_my_coin_unit_price(my_investment)
    # 현재 코인 단가
    current_unit_price = pyupbit.get_current_coin_price(candle)
    # 코인 현재 단가
    current_price = current_unit_price
    # 수익률(100%가 매수 시점 단가)
    profit_rate = pyupbit.get_profit_rate(current_unit_price, buy_unit_price)
    # 오늘 시가
    today_open_price = pyupbit.get_today_opening_price(candle)
    # 어제 고가
    prev_high_price = pyupbit.get_yesterday_high_price(candle)
    # 어제 저가
    prev_low_price = pyupbit.get_yesterday_low_price(candle)
    # 기준선
    standard_price = pyupbit.calc_standard_line(prev_high_price, prev_low_price, today_open_price)
    # 1차 지지선
    first_low_price = pyupbit.first_lower_line(standard_price, prev_high_price)
    # 2차 지지선
    second_low_price = pyupbit.second_lower_line(standard_price, prev_high_price, prev_low_price)
    # 1차 저항선
    first_high_price = pyupbit.first_higher_line(standard_price, prev_low_price)
    # 2차 저항선
    second_high_price = pyupbit.second_higher_line(standard_price, prev_high_price, prev_low_price)
    slack_message = f"코인명 ::: {market}(매수단가 ::: {buy_unit_price}, 현재단가 ::: {current_unit_price}, 수익률 ::: {str(profit_rate)}%"
    print(slack_message)
    # 매도 시점 판단 로직
    """
    스코어 기준 판단? -> 원래 로직임
    지지선, 저항선 기준 판단 -> 신규 로직
    지지선을 넘었다 -> 망함 -> 버티기?
    저항선을 넘었다 -> 좋음 -> 스코어 기준으로 계산 하기
    """
    # 한번이라도 마이너스 수익률이었으면 has_minus_exp 값 변경해 주기
    if profit_rate < 100:
        has_minus_exp = True

    # 스코어 기준 계산 하기(상승시에만 계산하니까 1로 변경)
    #if score >= 1:
    if 100.1 <= profit_rate != prev_profit_rate:
        # pyupbit.sell_all()
        pyupbit.send_message(pyupbit.get_slack_channel(), f':aaw_yeah: [벌었음!!]' + slack_message)
        print('sell!!')

    # 버티기 -> 손절 포인트 -10% (테스트) -> 손절 시 1시간 생각할 시간을 가지게 하고 다시 들어가기.
    if profit_rate < pyupbit.get_force_sell_percent() and profit_rate != prev_profit_rate:
        pyupbit.sell_all()
        slack_message1 = f"""
        ':ahhhhhhhhh: [손절하였습니다...]'
        {slack_message}
        5분 뒤 자동투자를 다시 시작 합니다.
        """
        pyupbit.send_message(pyupbit.get_slack_channel(), slack_message1)
        time.sleep(300)
    else:
        print('thinking...')

    # 스코어(매도시점용)
    score, prev_profit_rate = pyupbit.new_calc_profit_score(score, prev_profit_rate, profit_rate)

    return prev_profit_rate, score, has_minus_exp
