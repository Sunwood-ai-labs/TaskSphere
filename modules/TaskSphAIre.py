from google.oauth2 import service_account
from googleapiclient.discovery import build
from termcolor import colored
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import json
import sys
from tqdm import tqdm
from time import sleep
from art import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.GithubProject import GithubProject
from modules.GoogleCalendar import GoogleCalendar
from modules.TaskBreakdown import TaskBreakdown
from modules.TaskMarkdownToJson import TaskMarkdownToJson

class TaskSphAIre:
    def __init__(self):
        self.github_project = GithubProject()
        self.google_calendar = GoogleCalendar(calendar_id=os.environ['CALENDAR_ID'])
        self.task_breakdown = TaskBreakdown(
            tmp_folder="tmp/task",
            template_path="template/_prompt_task2subtask.md",
            model_name="anthropic/claude-3-haiku-20240307",
            max_tokens=None,
            temperature=None,
            api_base=None
        )
        self.task_markdown_to_json = TaskMarkdownToJson(
            input_dir="tmp/responses",
            task_dir="tmp/task",
            output_dir="tmp/converted_tasks",
            input_pattern="response_*.md",
            task_pattern="task_*.md",
            output_prefix="response_",
            output_extension=".json"
        )

    def run(self):
        self.github_project.validate_environment_variables()
        project_id = self.github_project.get_project_info()
        self.github_project.get_project_items(project_id)

        self.task_breakdown.process_tasks(task_limit=3)
        self.task_markdown_to_json.process_markdown_files()

        self.process_tasks_to_google_calendar()

    def process_tasks_to_google_calendar(self):
        # 日本時間のタイムゾーンを設定
        jst = ZoneInfo("Asia/Tokyo")

        # 今日の0時（日本時間）を取得
        today = datetime.now(jst).date()
        time_min = datetime.combine(today, datetime.min.time(), tzinfo=jst).isoformat()

        # 今日の終わりを取得
        time_max = datetime.combine(today, datetime.max.time()).isoformat() + 'Z'

        print(colored('Upcoming events:', 'green'))
        upcoming_events = self.google_calendar.get_upcoming_events(time_min=time_min)
        self.google_calendar.print_upcoming_events(upcoming_events)

        # JSONファイルを取得し、作成日時順にソート
        json_files = sorted(os.listdir("tmp/converted_tasks"), key=lambda x: os.path.getctime(os.path.join("tmp/converted_tasks", x)))

        # 開始時刻を設定
        start_time_str = "2024-05-04 00:00"
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M").replace(tzinfo=jst)

        for json_file in tqdm(json_files, desc="Processing JSON files"):
            with open(os.path.join("tmp/converted_tasks", json_file), 'r') as file:
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
                available_start_time = self.google_calendar.find_available_time_slot(start_time, duration, summary)

                if available_start_time is not None:
                    print(colored(f'available_start_time:{available_start_time}', 'red'))
                    created_event = self.google_calendar.create_event(available_start_time, duration, summary, location, description)
                    self.google_calendar.print_event_details(created_event)

                    # 次のタスクの開始時刻を計算
                    start_time = available_start_time + timedelta(minutes=duration)

                    sleep(5)
                else:
                    print(colored(f"Event creation skipped: {summary}", 'red'))

            # ファイル処理の間に1秒の遅延を追加
            sleep(1)

        print(colored('Upcoming events:', 'green'))
        upcoming_events = self.google_calendar.get_upcoming_events(time_min=time_min)
        self.google_calendar.print_upcoming_events(upcoming_events)

if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    tprint(script_name)

    task_sphere_ai = TaskSphAIre()
    task_sphere_ai.run()