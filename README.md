# py_autoinvestment
파이썬 비트 코인 자동투자 프로젝트입니다. (파이썬 공부하고 있어요.) <br>
업비트 api 를 활용한 자동투자 기능을 구현해 보았습니다.(투자 한개도 몰라요 ㅋㅋ)<br>
원래 자바 개발자고 파이썬은 이번에 처음 해 보는데<br> 
혹시라도 지나가다 보시게 되었다면 많은 가르침(투자 / 파이썬) 주시면 감사하겠습니다~

# 사용 방법
업비트 보안등급 4단계 까지 가시고(kbank 계좌가 없다면 만들어야 할 수도 있습니다.)<br>
원화를 업비트에 입금 한 후 업비트 웹에서 open api 사용 신청 한 다음 <br>
process_check.py 를 실행 하면 됩니다.<br>
프로그램의 사용 및 가공 기타 등등으로 인한 이익이나 손실은 모두 본인의 책임 입니다.

> 프로젝트 root 폴더에 아래의 내용으로 config.json 파일을 생성 해 주세요<br>
> {<br>
  "access_key": "업비트 access_key",<br>
  "secret_key": "업비트 secret_key",<br>
  "site_url": "https://api.upbit.com",<br>
  "slack_token": "슬랙 메시지 발송용 봇 토큰",<br>
  "slack_channel": "메시지 받을 슬랙 채널명",<br>
  "main_script_path": "main.py 가 설치 된 전체 경로"<br>
}