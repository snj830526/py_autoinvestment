import time
import pyupbit
from pyupbit import InvestmentService


# 투자 메인 입니다.
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
    prev_profit_rate = 100
    # 비교용 수익률
    recoding_profit_rate = 100
    # 전체 코인 코드, 이름 조회
    all_market_codes, all_market_names = pyupbit.get_all_markets()
    # 투자 가능한 코인 맵
    investable_coins_map = {}

    # 프로그램 시작
    while True:
        # 처음 시작 / 1일 동안 별 소득 없으면 투자 초기화 동작
        InvestmentService().initalize_investment(counter, investable_coins_map, all_market_codes, all_market_names,
                                                 order_money, prev_profit_rate, recoding_profit_rate, score,
                                                 has_minus_exp)

        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)
        counter += 1


if __name__ == '__main__':
    profit_check_and_order()
