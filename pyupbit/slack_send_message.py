import requests
import json
file = open('config.json')
config = json.load(file)

SLACK_BOT_TOKEN = config['slack_token']


def send_message(channel, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + SLACK_BOT_TOKEN
    }
    payload = {
        'channel': channel,
        'text': message
    }
    res = requests.post('https://slack.com/api/chat.postMessage', headers=headers, data=json.dumps(payload))
