from google.oauth2 import service_account
from googleapiclient.discovery import build
from termcolor import colored
from datetime import datetime, timedelta

import os
import json
import requests
from termcolor import colored
from art import *
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.GithubProject import GithubProject
from modules.GoogleCalendar import GoogleCalendar

class GithubToGoogleCalendar:
    def __init__(self):
        self.github_project = GithubProject()
        self.google_calendar = GoogleCalendar(os.environ['CALENDAR_ID'])

    def run(self):
        self.github_project.validate_environment_variables()
        project_id = self.github_project.get_project_info()
        items = self.github_project.get_project_items(project_id)

        start_time = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=1)
        duration = 120  # 2 hours
        interval = 30  # 1 hour

        for item in items:
            summary = item['content']['title']
            location = 'Sample-location'
            description = item['content']['body'] if 'body' in item['content'] else 'Sample-Body'
            if(description == ""):
                description = 'Sample-Body'
                
            event = self.google_calendar.create_event(start_time, duration, summary, location, description)
            self.google_calendar.print_event_details(event)

            start_time += timedelta(minutes=interval+duration)


if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    tprint(script_name)

    github_to_google_calendar = GithubToGoogleCalendar()
    github_to_google_calendar.run()