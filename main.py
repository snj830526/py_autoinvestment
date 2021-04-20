import time
import pyupbit
import json

file = open('config.json')
config = json.load(file)

slack_channel = config['slack_channel']


# 가즈아!
def profit_check_and_order():
    # 한시간마다 투자 재시작 시키기 위한 카운터
    counter = 0
    # 직전 수익률
    prev_profit_rate = 100
    # 수익률스코어
    score = 0
    # 전체 코인 코드
    all_market_codes = pyupbit.all_market_names.view_market_codes()
    # 전체 코인 이름
    all_market_names = pyupbit.all_market_names.view_market_names()
    # 투자 가능한 코인 맵
    investable_coins_map = {}
    # 이전에 조회 한 투자할만한 코인 맵
    prev_coins_map = {}
    # 프로그램 시작
    while True:
        # 처음 시작 / 1시간 동안 별 소득 없으면 투자 초기화 동작
        if counter % 720 == 0:
            print('Finding the best coin to invest...(It runs once in an hour.)')
            print('계좌에 보유한 코인이 없는 상태로 만들고 -> 매수 시작!')
            # 전 시간에 투자 한 코인 전량 매도
            if pyupbit.get_my_coin_info() is not None:
                pyupbit.sell_all()
            if dict(investable_coins_map):
                prev_coins_map = investable_coins_map
            else:
                prev_coins_map = pyupbit.get_investable_coin_map(all_market_codes, all_market_names)
            investable_coins_map = pyupbit.get_investable_coin_map(all_market_codes, all_market_names)
            slack_message = f"""
                현재코인수익률 ::: {investable_coins_map}
                직전코인수익률 ::: {prev_coins_map}
            """
            pyupbit.send_message(slack_channel, slack_message)
            best_coin = pyupbit.get_best_coin_name(investable_coins_map, prev_coins_map)
            pyupbit.init(best_coin)
            score = 0
        # 매수 한 투자 정보 조회
        my_investment = pyupbit.get_my_coin_info()
        if my_investment is not None:
            for market in my_investment.keys():
                strategy_report_arr = pyupbit.working(market, my_investment, prev_profit_rate, score)
                prev_profit_rate = strategy_report_arr[0]
                score = strategy_report_arr[1]
        else:
            # 내 계좌에 코인이 없으면 다시 50000원 어치 매수
            if dict(investable_coins_map):
                prev_coins_map = investable_coins_map
            else:
                prev_coins_map = pyupbit.get_investable_coin_map(all_market_codes, all_market_names)
            investable_coins_map = pyupbit.get_investable_coin_map(all_market_codes, all_market_names)
            slack_message = f"""
                현재코인수익률 ::: {investable_coins_map}
                직전코인수익률 ::: {prev_coins_map}
            """
            pyupbit.send_message(slack_channel, slack_message)
            best_coin = pyupbit.get_best_coin_name(investable_coins_map, prev_coins_map)
            pyupbit.init(best_coin)
            # 스코어 초기화
            score = 0
            # 재시작 카운터 초기화
            counter = 1
        counter = counter + 1
        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)


if __name__ == '__main__':
    profit_check_and_order()

