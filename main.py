import time
from datetime import datetime
import pyupbit


def profit_check_and_order():
    # 한시간마다 투자 재시작 시키기 위한 카운터
    counter = 0
    # 프로그램 시작
    while True:
        # 처음 시작 / 한시간 후 카운터 동작
        if counter % 720 == 0:
            print('Finding the best coin to invest...(It runs once in an hour.)')
            # 전 시간에 투자 한 코인 전량 매도
            pyupbit.sell_all()
            # 가장 살만할 것 같은 코인 50,000원 어치 매수
            best_coin = pyupbit.get_best_coin_name()
            print(f"이번시간에 투자할 코인은? {best_coin}")
            pyupbit.order_best_coin(best_coin)
            # 매수 신청 후 매수 될 때까지 대기
            while pyupbit.get_my_coin_info() is None:
                time.sleep(1)
        # 매수 한 투자 정보 조회
        my_investment = pyupbit.get_my_coin_info()
        if my_investment is not None:
            for market in my_investment.keys():
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
                slack_message1 = f"코인명 ::: {market}, 매수단가 ::: {buy_unit_price}, 현재단가 ::: {current_unit_price}, 수익률 ::: {str(profit_rate)}%"
                print(slack_message1)
                # 매수할 만 하고 코인 단가가 내가 샀을때 보다 살짝 떨어져 있을 때 추가 매수
                if target_price >= current_unit_price and 97 >= profit_rate > 95:
                    if krw_balance >= 10000:
                        available_coin_amount = pyupbit.get_possible_order_volume(coin_candle, 10000)
                        pyupbit.order_10000(market, available_coin_amount, 'bid')
                        pyupbit.send_message('#myinvestment', f'[Buying!!-{str(datetime.today())}]' + slack_message1)
                        print('buy!!')
                # 수익률이 일정 수준에 도달 했을때 매도
                elif profit_rate > 105.0:
                    pyupbit.order_10000(market, my_coin_balance, 'ask')
                    pyupbit.send_message('#myinvestment', f'[Selling!!-{str(datetime.today())}]' + slack_message1)
                    print('sell!!')
                # 수익률이 너무 떨어질 것 같을때 매도
                elif profit_rate < 95:
                    pyupbit.order_10000(market, my_coin_balance, 'ask')
                    pyupbit.send_message('#myinvestment', f'[sell_all...-{str(datetime.today())}]' + slack_message1)
                    print('sell!!')
                # 그 외 상태일 경우
                else:
                    print('thinking...')
        else:
            # 내 계좌에 코인이 없으면 다시 10000원 어치 매수
            best_coin = pyupbit.get_best_coin_name()
            pyupbit.order_best_coin(best_coin)
        counter = counter + 1
        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)


if __name__ == '__main__':
    profit_check_and_order()

