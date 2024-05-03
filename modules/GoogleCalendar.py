from google.oauth2 import service_account
from googleapiclient.discovery import build
from termcolor import colored
from datetime import datetime, timedelta

import os
import json
import requests
from termcolor import colored
from art import *
from zoneinfo import ZoneInfo

class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self.service = self.authorize()

    def authorize(self):
        # 環境変数からサービスアカウントキーのファイルパスを取得
        service_account_file = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

        creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=self.SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        return service

    def create_event(self, start_time, duration, summary, location, description):
        end_time = start_time + timedelta(minutes=duration)

        event_data = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Tokyo',
            },
        }

        return self.service.events().insert(calendarId=self.calendar_id, body=event_data).execute()

    def get_upcoming_events(self, max_results=10, time_min=None, time_max=None):
        if time_min is None:
            time_min = datetime.utcnow().isoformat() + 'Z'
        if time_max is None:
            time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'

        events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=time_min,
                                                   timeMax=time_max, maxResults=max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def print_event_details(self, event):
        print(colored('Event details:', 'green'))
        print(colored('Summary: ', 'yellow') + colored(event['summary'], 'cyan'))
        print(colored('Location: ', 'yellow') + colored(event.get('location', ''), 'cyan'))
        print(colored('Description: ', 'yellow') + colored(event.get('description', ''), 'cyan'))
        print(colored('Start: ', 'yellow') + colored(event['start']['dateTime'], 'cyan'))
        print(colored('End: ', 'yellow') + colored(event['end']['dateTime'], 'cyan'))
        print(colored('Event URL: ', 'yellow') + colored(event['htmlLink'], 'cyan'))

    def print_upcoming_events(self, events):
        if not events:
            print('No upcoming events found.')
        for event in events:
            self.print_event_details(event)
            print()

    def find_available_time_slot(self, start_time, duration):
        time_min = start_time.astimezone(ZoneInfo("UTC")).isoformat()
        time_max = (start_time + timedelta(days=1)).astimezone(ZoneInfo("UTC")).isoformat()
        print(colored(f'time_min:{time_min} ', 'yellow'))
        print(colored(f'time_max:{time_max} ', 'yellow'))
        events = self.get_upcoming_events(time_min=time_min, time_max=time_max)

        if not events:
            return start_time

        latest_end_time = start_time.astimezone(ZoneInfo("UTC"))
        for event in events:
            event_start_time = datetime.fromisoformat(event['start']['dateTime'])
            event_end_time = datetime.fromisoformat(event['end']['dateTime'])
            print(colored(f'event_start_time:{event_start_time} ', 'magenta'))
            print(colored(f'event_end_time:{event_end_time} ', 'red'))
            print(colored(f'latest_end_time:{latest_end_time} ', 'blue'))
            
            if event_start_time <= latest_end_time + timedelta(minutes=duration):
                latest_end_time = event_end_time

        # イベント間の間隔を10分に設定
        buffer_time = timedelta(minutes=0)
        latest_end_time += buffer_time

        return latest_end_time.astimezone(ZoneInfo("Asia/Tokyo"))

if __name__ == '__main__':
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

    start_time_str = "2024-05-03 00:00"
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M").replace(tzinfo=jst)
    duration = 60
    summary = "TEST01"
    location = "TEST-AAAA"
    description = "TEST---01-text"

    available_start_time = google_calendar.find_available_time_slot(start_time, duration)
    
    print(colored(f'available_start_time:{available_start_time}', 'red'))
    created_event = google_calendar.create_event(available_start_time, duration, summary, location, description)
    google_calendar.print_event_details(created_event)