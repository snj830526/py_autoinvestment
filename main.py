import time
import pyupbit


# 투자 메인 입니다.
from pyupbit import StaticProperties, InvestmentService


def profit_check_and_order():
    # config.json에 설정 된 투자금액 만큼만 투자
    order_money = float(pyupbit.get_my_order_price())

    # 한시간마다 투자 재시작 시키기 위한 카운터
    counter = 0
    # 수익률스코어
    score = 0
    # 마이너스 체험 여부
    has_minus_exp = False
    # 직전 수익률
    prev_profit_rate = StaticProperties.STANDARD_PROFIT_RATE
    # 비교용 수익률
    recoding_profit_rate = StaticProperties.STANDARD_PROFIT_RATE
    # 전체 코인 코드, 이름 조회
    all_market_codes, all_market_names = pyupbit.get_all_markets()
    # 투자 가능한 코인 맵
    investable_coins_map = {}
    investment_service_ins = InvestmentService()

    # 프로그램 시작
    while True:
        # 처음 시작 / 1일 동안 별 소득 없으면 투자 초기화 동작
        if counter % (3600 * 24) == 0:
            # 수익률 먼저 체크(수익률이 100% 이하인지 확인)
            keep_going = pyupbit.check_my_investment()
            print(f'Finding the best coin to invest...(It runs once in a day.) / keep going :: {keep_going}')

            # 수익률이 100% 초과면 매도 하고 시작
            investment_service_ins.init_investment(
                investable_coins_map, all_market_codes, all_market_names, order_money, keep_going
            )

            # 스코어 초기화
            score = 0

        # 매수 한 투자 정보 조회
        my_investment = pyupbit.get_my_coin_info()
        if my_investment is not None:
            investment_service_ins.check_my_investment(
                my_investment, prev_profit_rate, recoding_profit_rate, score, has_minus_exp, counter
            )
        else:
            # 내 계좌에 코인이 없으면 다시 주문금액 만큼 매수
            pyupbit.init_prepairing(investable_coins_map, all_market_codes, all_market_names, order_money)
            # 스코어 초기화
            score = 0
            # 재시작 카운터 초기화(매도 했으니 초기화)
            counter = 0

        counter = counter + 1
        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)


if __name__ == '__main__':
    profit_check_and_order()
