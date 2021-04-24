import time
import pyupbit


# 투자 메인 입니다.
def profit_check_and_order():
    # config.json에 있는 투자금액 만큼만 투자
    order_money = float(pyupbit.get_my_order_price())
    # 한시간마다 투자 재시작 시키기 위한 카운터
    counter = 0
    # 직전 수익률
    prev_profit_rate = 100
    # 수익률스코어
    score = 0
    # 마이너스 체험 여부
    has_minus_exp = False
    # 전체 코인 코드
    all_market_codes = pyupbit.all_market_names.view_market_codes()
    # 전체 코인 이름
    all_market_names = pyupbit.all_market_names.view_market_names()
    # 투자 가능한 코인 맵
    investable_coins_map = {}

    # 프로그램 시작
    while True:
        # 처음 시작 / 1일 동안 별 소득 없으면 투자 초기화 동작
        if counter % 17280 == 0:
            # 수익률 먼저 체크(수익률이 100% 이하인지 확인)
            keep_going = pyupbit.check_my_investment()
            print('Finding the best coin to invest...(It runs once in a day.)')
            # 수익률이 100% 초과면 매도 하고 시작
            if not keep_going:
                if pyupbit.get_my_coin_info() is not None:
                    # 전 시간에 투자 한 코인 전량 매도
                    pyupbit.sell_all()
                # 코인 찾아서 매수
                pyupbit.init_prepairing(investable_coins_map, all_market_codes, all_market_names, order_money)
            else:
                slack_message = ':meow_party: 수익률이 100% 이하라서 매도 없이 초기화 시작함.'
                print(slack_message)
                pyupbit.send_message(pyupbit.get_slack_channel(), slack_message)
            # 스코어 초기화
            score = 0

        # 매수 한 투자 정보 조회
        my_investment = pyupbit.get_my_coin_info()
        if my_investment is not None:
            for market in my_investment.keys():
                # 코인의 현재 수익률을 확인하면서 매도 여부 판단 -> 자동 매도 처리 함(auto_sell 옵션에 따라 동작 - YES/NO)
                strategy_report_arr = pyupbit.new_working(market, my_investment, prev_profit_rate, score, has_minus_exp)
                prev_profit_rate = strategy_report_arr[0]
                score = strategy_report_arr[1]
                has_minus_exp = strategy_report_arr[2]
                # 수익률이 애매할 때 슬랙으로 메시지 보내기(5초에 1회)
                if prev_profit_rate > 99 and counter % 5 == 0:
                    notice_message = f'코인 : {market}, 수익률 : {prev_profit_rate}%, 마이너스 다녀온적? : {has_minus_exp}'
                    print(f'send message! / {notice_message} / {counter}')
                    pyupbit.send_message(pyupbit.get_slack_channel(), notice_message)
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

