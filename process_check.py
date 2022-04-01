import os
import time
import pyupbit


def check():
    counter = 0
    while True:
        process_read = os.popen("ps -ef | grep /autoinvest/main.py | grep -v 'grep'").readlines()
        check_process = str(process_read)
        if counter == 0:
            slack_message = ":meow_whacky_rainbow: 프로그램 시작합니다."
            start_investment_process(slack_message, 0)
        if check_process.find('main.py') == -1:
            slack_message = ":meow_whacky_rainbow: 프로그램이 중지되었습니다. 5초 뒤 재시작 합니다."
            start_investment_process(slack_message, 5)
        else:
            print('process running...')
        counter = counter + 1
        time.sleep(10)


def start_investment_process(slack_message, sleep_time):
    print(f'process stopped... {slack_message}')
    pyupbit.send_message(pyupbit.get_slack_channel(), slack_message)
    time.sleep(sleep_time)
    os.system(f"python {pyupbit.get_script_path()}")


if __name__ == '__main__':
    check()
