import time
import pyupbit


# 투자!
def profit_check_and_order():
    # 한시간마다 투자 재시작 시키기 위한 카운터
    counter = 0
    # 수익률
    prev_profit_rate = 100
    # 수익률스코어
    score = 0
    # 전체 코인 코드
    all_market_codes = pyupbit.all_market_names.view_market_codes()
    # 전체 코인 이름
    all_market_names = pyupbit.all_market_names.view_market_names()
    # 투자 가능한 코인 맵
    investable_coins_map = {}
    prev_coins_map = {}
    # 프로그램 시작
    while True:
        # 처음 시작 / 30분 후 카운터 동작
        if counter % 360 == 0:
            print('Finding the best coin to invest...(It runs once in an hour.)')
            if dict(investable_coins_map):
                prev_coins_map = investable_coins_map
            investable_coins_map = pyupbit.get_investable_coin_map(all_market_codes, all_market_names)
            best_coin = pyupbit.get_best_coin_name(investable_coins_map)
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
            investable_coins_map = pyupbit.get_investable_coin_map(all_market_codes, all_market_names)
            best_coin = pyupbit.get_best_coin_name(investable_coins_map)
            pyupbit.init(best_coin)
            score = 0
        counter = counter + 1
        # 위의 프로세스는 5초에 1회 동작
        time.sleep(5)


if __name__ == '__main__':
    profit_check_and_order()

