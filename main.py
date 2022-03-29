import time
import pyupbit
from pyupbit import InvestmentService


# 투자 메인 입니다.
def profit_check_and_order():
    # 한시간마다 투자 재시작 시키기 위한 카운터
    counter = 0

    # 프로그램 시작
    while True:
        # 처음 시작 / 1일 동안 별 소득 없으면 투자 초기화 동작
        InvestmentService().initalize_investment(counter)

        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)
        counter += 1


if __name__ == '__main__':
    profit_check_and_order()
