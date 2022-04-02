import pyupbit


class InvestmentService:

    def initalize_investment(self, counter=0):
        # config.json에 설정 된 투자금액 만큼만 투자
        order_money = float(pyupbit.get_my_order_price())
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

        # 처음 시작 / 1일 동안 별 소득 없으면 투자 초기화 동작
        if counter % (3600 * 24) == 0:
            # 수익률 먼저 체크(수익률이 100% 이하인지 확인)
            in_red = pyupbit.check_my_investment()
            print(f'Finding the best coin to invest...(It runs once in a day.) / in_red :: {in_red}')

            # 수익률이 100% 초과면 매도 하고 다른거 찾아서 구매
            self.check_investment_at_first(
                investable_coins_map, all_market_codes, all_market_names, order_money, in_red
            )

            # 스코어 초기화
            score = 0

        # 매수 한 투자 정보 조회
        my_investment = pyupbit.get_my_coin_info()
        if not my_investment:
            # 내 계좌에 코인이 없으면 다시 주문금액 만큼 매수(이 부분 - 전략 적용) TODO 생각날때마다 수정
            pyupbit.init_prepairing(investable_coins_map, all_market_codes, all_market_names, order_money)

            # 스코어 초기화, 재시작 카운터 초기화(매도 했으니 초기화)
            score = 0
            counter = 0
        else:
            # 투자 한 코인 현황 조회
            self.check_my_investment(
                my_investment, prev_profit_rate, recoding_profit_rate, score, has_minus_exp, counter
            )

    def check_investment_at_first(self, investable_coins_map, all_market_codes, all_market_names, order_money,
                                  in_red=False):
        if not in_red:
            if pyupbit.get_my_coin_info() is not None:
                # 투자 중인 코인 전량 매도
                pyupbit.sell_all()
            if pyupbit.get_my_coin_info() is None:
                # 코인 찾아서 매수
                pyupbit.init_prepairing(investable_coins_map, all_market_codes, all_market_names, order_money)
        else:
            slack_message = ':meow_party: 수익률이 100% 이하라서 매도 없이 초기화 시작함.'
            print(slack_message)
            # pyupbit.send_message(pyupbit.get_slack_channel(), slack_message)

    def check_my_investment(self, my_investment, prev_profit_rate, recoding_profit_rate, score, has_minus_exp, counter):
        for market in my_investment.keys():
            # 코인의 현재 수익률을 확인하면서 매도 여부 판단 -> 자동 매도 처리 함(auto_sell 옵션에 따라 동작 - YES/NO)
            prev_profit_rate, score, has_minus_exp = pyupbit.new_working(
                market, my_investment, prev_profit_rate, score, has_minus_exp, counter
            )

            if counter % 10 == 0:
                notice_message = f':quad_parrot: 코인 : {market}, \n수익률 : {prev_profit_rate}%, \n수익률 변동폭 : {round(prev_profit_rate - recoding_profit_rate, 2)}%'
                print(f'send message! / {notice_message} / {counter}')

                pyupbit.send_message(pyupbit.get_slack_channel(), notice_message)
                recoding_profit_rate = prev_profit_rate
