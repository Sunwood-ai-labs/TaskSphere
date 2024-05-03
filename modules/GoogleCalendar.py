from google.oauth2 import service_account
from googleapiclient.discovery import build
from termcolor import colored
from datetime import datetime, timedelta

import os
import json
import requests
from termcolor import colored
from art import *


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

if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    tprint(script_name)

    # 環境変数からカレンダーIDを取得
    calendar_id = os.environ['CALENDAR_ID']

    # GoogleCalendarインスタンスを作成
    google_calendar = GoogleCalendar(calendar_id)

    start_time_str = "2024-05-03 00:00"
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    duration = 60
    summary = "TEST01"
    location = "TEST-AAAA"
    description = "TEST---01-text"

    # created_event = google_calendar.create_event(start_time, duration, summary, location, description)
    # google_calendar.print_event_details(created_event)

    print(colored('Upcoming events:', 'green'))
    upcoming_events = google_calendar.get_upcoming_events()
    google_calendar.print_upcoming_events(upcoming_events)