import pyupbit


class InvestmentService:

    def init_investment(self, investable_coins_map, all_market_codes, all_market_names, order_money, keep_going=False):

        if not keep_going:
            if pyupbit.get_my_coin_info() is not None:
                # 전 시간에 투자 한 코인 전량 매도
                pyupbit.sell_all()
            if pyupbit.get_my_coin_info() is None:
                # 코인 찾아서 매수
                pyupbit.init_prepairing(investable_coins_map, all_market_codes, all_market_names, order_money)
        else:
            slack_message = ':meow_party: 수익률이 100% 이하라서 매도 없이 초기화 시작함.'
            print(slack_message)
            pyupbit.send_message(pyupbit.get_slack_channel(), slack_message)

    def check_my_investment(self, my_investment, prev_profit_rate, recoding_profit_rate, score, has_minus_exp, counter):
        for market in my_investment.keys():
            # 코인의 현재 수익률을 확인하면서 매도 여부 판단 -> 자동 매도 처리 함(auto_sell 옵션에 따라 동작 - YES/NO)
            strategy_report_arr = pyupbit.new_working(market, my_investment, prev_profit_rate, score, has_minus_exp)
            prev_profit_rate = strategy_report_arr[0]
            score = strategy_report_arr[1]
            has_minus_exp = strategy_report_arr[2]
            # 수익률이 애매할 때 슬랙으로 메시지 보내기(30초에 1회)
            if prev_profit_rate > 100 and counter % 30 == 0:
                notice_message = f':quad_parrot: 코인 : {market}, \n수익률 : {prev_profit_rate}%, \n수익률 변동폭 : {round(prev_profit_rate - recoding_profit_rate, 2)}%, \n마이너스 다녀온적? : {has_minus_exp}'
                print(f'send message! / {notice_message} / {counter}')
                pyupbit.send_message(pyupbit.get_slack_channel(), notice_message)
                recoding_profit_rate = prev_profit_rate
