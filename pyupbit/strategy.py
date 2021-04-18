import pyupbit
import time
from datetime import datetime


# 계좌에 보유한 코인이 없는 상태로 만들고 -> 매수 시작!
def init(best_coin=''):
    init_counter = 0
    # 가장 살만할 것 같은 코인 50,000원 어치 매수
    print(f"이번시간에 투자할 코인은? {best_coin}")
    response = pyupbit.order_best_coin(best_coin)
    print(f'주문 결과 ::: {response} / uuid ::: {pyupbit.get_order_bid_uuid(response.json())}')
    if 200 <= response.status_code <= 299:
        # 매수 신청 후 매수 될 때까지 대기
        while pyupbit.get_my_coin_info() is None:
            time.sleep(1)
            init_counter = init_counter + 1
            print('매수 체결 대기 중...')
            if init_counter >= 30:
                print(f'아직 사지지 않았습니다.')
                # 너무 오래 걸리면 주문 취소 후 다시 시도
                pyupbit.cancel_order(pyupbit.get_order_bid_uuid(response.json()))
                time.sleep(30)
                init(best_coin)
    else:
        print(f'재 주문 시도...{response.status_code} / {response.json()}')
        time.sleep(5)
        init(best_coin)


# 빡침 스코어 기록기
def calc_profit_score(rage_score=0, prev_profit_rate=0, current_profit_rate=0):
    # 마이너스 변동폭(마이너스 / 플러스 반대)
    minus_change_rate = prev_profit_rate - current_profit_rate
    # 스코어 계산 하기!
    # 수익률 100% 이상
    if current_profit_rate >= 100:
        if minus_change_rate >= 0:
            rage_score = rage_score + minus_change_rate
        else:
            rage_score = rage_score + minus_change_rate / 2
    # 수익률 100% 미만
    else:
        if minus_change_rate >= 0:
            rage_score = rage_score + minus_change_rate
        else:
            rage_score = rage_score + minus_change_rate
    slack_message = f'현재 점수는 ::: {round(rage_score, 2)} / 변동폭은 ::: {round(-minus_change_rate, 2)}% / 직전 수익률은 ::: {prev_profit_rate}% / 현재 수익률은 ::: {current_profit_rate}%'
    print(slack_message)
    if rage_score >= 5:
        pyupbit.send_message('#myinvestment', slack_message)
    """
    매도 할 타이밍은 스코어가 5점 이상인 경우로 한다.
    1. 절대 수익률이 100% 보다 높은 경우
      - 직전 수익률 보다 떨어졌을 때(+)
        rage_score = rage_score + minus_change_rate
      - 직전 수익률 보다 올라갔을 때(-)
        rage_score = rage_score + minus_change_rate / 2
    2. 절대 수익률이 100% 보다 낮은 경우는 그냥 97% 미만일 때 매도 처리(빡침 스코어는 계산)
      - 직전 수익률 보다 떨어졌을 때(+)
        rage_score = rage_score + minus_change_rate
      - 직전 수익률 보다 올라갔을 때(-)
        rage_score = rage_score + minus_change_rate
    3. 빡침 스코어가 마이너스인 경우 0으로 처리
    """
    if rage_score < 0:
        rage_score = 0
    return rage_score


# 매도 / 매수 로직
def working(market='', my_investment={}, prev_profit_rate=100, score=0):
    # 매수 목표 가격 조회
    target_price = pyupbit.get_target_price_to_buy(market)
    # 해당 코인의 현재 상태(분 캔들) 조회
    coin_candle = pyupbit.view_candle_min(market)
    # 내가 매수 한 코인 단가
    buy_unit_price = pyupbit.get_my_coin_unit_price(my_investment)
    # 내 계좌에 남은 현금
    krw_balance = pyupbit.get_my_krw_balance(my_investment)
    # 내 계좌에 남은 코인 수
    my_coin_balance = pyupbit.get_my_coin_total_amount(my_investment)
    # 현재 코인 단가
    current_unit_price = pyupbit.get_current_coin_price(coin_candle)
    # 수익률(100%가 매수 시점 단가)
    profit_rate = pyupbit.get_profit_rate(current_unit_price, buy_unit_price)
    # 스코어(매도시점용)
    score = calc_profit_score(score, prev_profit_rate, profit_rate)
    slack_message1 = f"코인명 ::: {market}(현재점수:{round(score, 2)}), 매수단가 ::: {buy_unit_price}, 현재단가 ::: {current_unit_price}, 수익률 ::: {str(profit_rate)}%"
    print(slack_message1)
    # 매수할 만 하고 코인 단가가 내가 샀을때 보다 살짝 떨어져 있을 때 추가 매수 -> 일단 막기!!
    if target_price >= current_unit_price and 99 >= profit_rate >= 97:
        if krw_balance >= 10000:
            # 추가 매수 기능 막음
            # available_coin_amount = pyupbit.get_possible_order_volume(coin_candle, 10000)
            # pyupbit.order_10000(market, available_coin_amount, 'bid')
            # pyupbit.send_message('#myinvestment', f'[Buying!!-{str(datetime.today())}]' + slack_message1)
            print('buy!!')
    # 매도 매수 시점 판단 빡침 스코어 기준으로 변경!
    elif score >= 5:
        pyupbit.order_10000(market, my_coin_balance, 'ask')
        pyupbit.send_message('#myinvestment', f'[Selling!!-{str(datetime.today())}]' + slack_message1)
        print('sell!!')
    # 수익률이 너무 떨어질 것 같을때 매도
    elif profit_rate < 97:
        pyupbit.order_10000(market, my_coin_balance, 'ask')
        pyupbit.send_message('#myinvestment', f'[sell_all...-{str(datetime.today())}]' + slack_message1)
        print('sell...')
    # 그 외 상태일 경우
    else:
        print('thinking...')
    # 수익률, 스코어 반환
    return [profit_rate, score]
