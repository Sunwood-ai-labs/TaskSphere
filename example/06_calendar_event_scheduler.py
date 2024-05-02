import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

from art import *
from termcolor import colored

import pprint

script_name = os.path.basename(__file__)
tprint(script_name)

SCOPES = ['https://www.googleapis.com/auth/calendar']

# 環境変数からサービスアカウントキーのファイルパスを取得
service_account_file = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

# 環境変数からカレンダーIDを取得
calendar_id = os.environ['CALENDAR_ID']

# イベントデータを作成
event = {
    'summary': 'Google 2019',
    'location': '800 Howard ',
    'description': 'A chance to hear more about Google',
    'start': {
        'dateTime': '2024-05-25T00:00:00-07:00',
    },
    'end': {
        'dateTime': '2024-05-25T01:00:00-07:00',
    },
}

# イベントを追加
created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

# 登録したイベントの情報を表示
print(colored('Event details:', 'green'))
print(colored('Summary: ', 'yellow') + colored(created_event['summary'], 'cyan'))
print(colored('Location: ', 'yellow') + colored(created_event['location'], 'cyan'))
print(colored('Description: ', 'yellow') + colored(created_event['description'], 'cyan'))
print(colored('Start: ', 'yellow') + colored(created_event['start']['dateTime'], 'cyan'))
print(colored('End: ', 'yellow') + colored(created_event['end']['dateTime'], 'cyan'))
print(colored('Event URL: ', 'yellow') + colored(created_event['htmlLink'], 'cyan'))