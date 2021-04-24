import json

file = open('config.json')
config = json.load(file)


# 슬랙 채널명
def get_slack_channel():
    return config['slack_channel']


# access key
def get_access_key():
    return config['access_key']


# secret_key
def get_secret_key():
    return config['secret_key']


# site_url
def get_site_url():
    return config['site_url']


# slack token
def get_slack_token():
    return config['slack_token']


# main.py path
def get_script_path():
    return config['main_script_path']


# slack bot token(invest_helper)
def get_slack_bot_token():
    return config['slack_bot_token']