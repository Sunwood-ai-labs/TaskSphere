from google.oauth2 import service_account
from googleapiclient.discovery import build
from termcolor import colored
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import glob
import json
import requests
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

# 日本時間のタイムゾーンを設定
jst = ZoneInfo("Asia/Tokyo")

# 今日の0時（日本時間）を取得
today = datetime.now(jst).date()
time_min = datetime.combine(today, datetime.min.time(), tzinfo=jst).isoformat()

# 今日の終わりを取得
time_max = datetime.combine(today, datetime.max.time()).isoformat() + 'Z'

print(colored('Upcoming events:', 'green'))
upcoming_events = google_calendar.get_upcoming_events(time_min=time_min)
google_calendar.print_upcoming_events(upcoming_events)

# JSONファイルのパターンを指定
json_pattern = "tmp/converted_tasks/response_*.json"

# JSONファイルを取得し、作成日時順にソート
json_files = sorted(glob.glob(json_pattern), key=os.path.getctime)[1:3]

# 開始時刻を設定
start_time_str = "2024-05-04 00:00"
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M").replace(tzinfo=jst)

for json_file in tqdm(json_files, desc="Processing JSON files"):
    with open(json_file, 'r') as file:
        data = json.load(file)

    for task in data:
        title = task['title']
        duration = task['duration'] + 10
        subtasks = task['subtasks']

        # タスクの詳細を設定
        summary = f"[{task['parent_title'][:2]}] {title}"
        location = ""
        description = "\n".join(subtasks)

        # 空き時間を検索してイベントを作成
        available_start_time = google_calendar.find_available_time_slot(start_time, duration, summary)

        if available_start_time is not None:
            print(colored(f'available_start_time:{available_start_time}', 'red'))
            created_event = google_calendar.create_event(available_start_time, duration, summary, location, description)
            google_calendar.print_event_details(created_event)

            # 次のタスクの開始時刻を計算
            start_time = available_start_time + timedelta(minutes=duration)

            sleep(5)
        else:
            print(colored(f"Event creation skipped: {summary}", 'red'))
        



    raise
    # ファイル処理の間に1秒の遅延を追加
    sleep(1)

tprint("-- Result --", font="small")
print(colored('Upcoming events:', 'green'))
upcoming_events = google_calendar.get_upcoming_events(time_min=time_min)
google_calendar.print_upcoming_events(upcoming_events)