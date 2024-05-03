from google.oauth2 import service_account
from googleapiclient.discovery import build
from termcolor import colored
from datetime import datetime, timedelta
import os
import glob
import json
import os
import json
import requests
from termcolor import colored
from art import *
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.GithubProject import GithubProject
from modules.GoogleCalendar import GoogleCalendar
from tqdm import tqdm
from time import sleep

script_name = os.path.basename(__file__)
tprint(script_name)

# 環境変数からカレンダーIDを取得
calendar_id = os.environ['CALENDAR_ID']

# GoogleCalendarインスタンスを作成
google_calendar = GoogleCalendar(calendar_id)

# JSONファイルのパターンを指定
json_pattern = "tmp/converted_tasks/response_*.json"

# JSONファイルを取得し、作成日時順にソート
json_files = sorted(glob.glob(json_pattern), key=os.path.getctime)[:1]

# 開始時刻を設定
start_time_str = "2024-05-03 00:00"
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")

for json_file in tqdm(json_files, desc="Processing JSON files"):
    with open(json_file, 'r') as file:
        data = json.load(file)

    for task in data:
        title = task['title']
        duration = task['duration']
        subtasks = task['subtasks']

        # タスクの詳細を設定
        summary = title
        location = ""
        description = "\n".join(subtasks)

        # タスクをGoogleカレンダーに送信
        created_event = google_calendar.create_event(start_time, duration, summary, location, description)
        google_calendar.print_event_details(created_event)

        # 次のタスクの開始時刻を計算
        start_time += timedelta(minutes=duration)

    # ファイル処理の間に1秒の遅延を追加
    sleep(1)

print(colored('Upcoming events:', 'green'))
upcoming_events = google_calendar.get_upcoming_events()
google_calendar.print_upcoming_events(upcoming_events)