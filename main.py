import time
import pyupbit
from pyupbit import InvestmentService


# 투자 메인 입니다.
def profit_check_and_order():
    counter = 0

    # 프로그램 시작
    while True:
        InvestmentService().initalize_investment(counter)

        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)
        counter += 1


if __name__ == '__main__':
    profit_check_and_order()
