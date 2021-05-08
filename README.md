# py_autoinvestment
파이썬 비트 코인 자동투자 프로젝트입니다. (파이썬 공부하고 있어요.) <br>
업비트 api 를 활용한 자동투자 기능을 구현해 보았습니다.(투자 한개도 몰라요 ㅋㅋ)<br>
원래 자바 개발자고 파이썬은 이번에 처음 해 보는데<br> 
혹시라도 지나가다 보시게 되었다면 많은 가르침(투자 / 파이썬) 주시면 감사하겠습니다~

# 사용 방법
* 업비트 계정 및 계좌 설정<br>
업비트 보안등급 4단계 까지 가시고(kbank 계좌가 없다면 만들어야 할 수도 있습니다.)<br>
원화를 업비트에 입금 한 후 업비트 웹에서 open api 사용 신청 <br><br>

* 프로그램 실행 설정<br>
  본인 계정의 슬랙 워크스페이스와 파이썬에서 보낸 메시지를 받을 슬랙 봇을 만들어 둡니다.<br>
  autoinvest 프로그램만으로도 자동투자는 가능하지만 <br>
  옆 프로젝트(py_invest_helper)와 연동 하여 쓰시면<br>
  슬랙을 이용한 수동 매도도 가능합니다.<br>
  프로그램 실행은 파이썬 3.9, 각종 패키지 설치 후 <br>
  process_check.py 를 실행 하면 됩니다.<br>
  * <b>프로그램의 사용 및 가공 기타 등등으로 인한 이익이나 손실은 모두 본인의 책임 입니다.<b>

> 프로젝트 root 폴더에 아래의 내용으로 config.json 파일을 생성 해 주세요<br>
> {<br>
  "access_key": "업비트 access_key",<br>
  "secret_key": "업비트 secret_key",<br>
  "site_url": "https://api.upbit.com",<br>
  "slack_token": "슬랙 메시지 발송용 봇 토큰",<br>
  "slack_channel": "메시지 받을 슬랙 채널명",<br>
  "main_script_path": "main.py 가 설치 된 전체 경로"<br>
  "my_order_price": "자동투자에 쓸 투자금(고정값 - 10000원 부터 하세요)",<br>
  "auto_sell": "YES/NO",<br>
  "force_sell_percent": 95 무조건 손절 할 수익률 값 입니다.<br>
}