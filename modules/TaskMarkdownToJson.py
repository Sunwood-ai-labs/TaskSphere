import os
import glob
import re
import json
from art import *
from termcolor import colored

class TaskMarkdownToJson:
    def __init__(self, input_dir="tmp/responses", task_dir="tmp/task", output_dir="tmp/converted_tasks", input_pattern="response_*.md", task_pattern="task_*.md", output_prefix="response_", output_extension=".json"):
        self.input_dir = input_dir
        self.task_dir = task_dir
        self.output_dir = output_dir
        self.input_pattern = input_pattern
        self.task_pattern = task_pattern
        self.output_prefix = output_prefix
        self.output_extension = output_extension

        # 出力ディレクトリが存在しない場合は作成する
        os.makedirs(self.output_dir, exist_ok=True)

    def parse_markdown(self, markdown_text):
        tasks = []
        current_task = None

        for line in markdown_text.split("\n"):
            if line.startswith("###"):
                if current_task:
                    tasks.append(current_task)
                title_match = re.match(r"###\s*(.*?):\s*\((\d+)分\)", line)
                if title_match:
                    current_task = {
                        "title": title_match.group(1),
                        "duration": int(title_match.group(2)),
                        "subtasks": []
                    }
            elif line.startswith("  -"):
                if current_task:
                    current_task["subtasks"].append(line[3:].strip())

        if current_task:
            tasks.append(current_task)

        return tasks

    def get_parent_title(self, task_file):
        with open(task_file, "r") as infile:
            task_text = infile.read()
            title_match = re.search(r"###\s*Title\s*:\s*(.*)", task_text)

            if title_match:
                return title_match.group(1).strip()
        return None

    def process_markdown_files(self):
        # 入力ディレクトリから指定されたパターンのファイルを取得し、数値順にソート
        markdown_files = sorted(glob.glob(os.path.join(self.input_dir, self.input_pattern)))

        # 各マークダウンファイルを順番に処理
        for markdown_file in markdown_files:
            with open(markdown_file, "r") as infile:
                # マークダウンファイルの内容を読み込む
                markdown_text = infile.read()

                # マークダウンをパースしてタスクのリストを取得
                tasks = self.parse_markdown(markdown_text)

                # タスクIDを取得
                task_id = os.path.splitext(os.path.basename(markdown_file))[0].split("_")[-1]

                # タスクIDに対応するタスクファイルを探す
                task_file = os.path.join(self.task_dir, f"task_PVTI_{task_id}.md")
                print(colored(f"task_file : {task_file} ", "red"))
                # タスクファイルが存在する場合、親タスクのタイトルを取得
                if os.path.exists(task_file):
                    parent_title = self.get_parent_title(task_file)
                    print(colored(f"parent_title : {parent_title} ", "red"))
                    if parent_title:
                        for task in tasks:
                            task["parent_title"] = parent_title

                # タスクをJSONに変換
                json_output = json.dumps(tasks, ensure_ascii=False, indent=2)

                # 出力ファイル名を生成
                output_file = os.path.join(self.output_dir, self.output_prefix + task_id + self.output_extension)

                # JSONを出力ファイルに書き込む
                with open(output_file, "w") as outfile:
                    outfile.write(json_output)

                print(colored(f"タスクが {output_file} に保存されました。", "green"))

if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    tprint(script_name, font="slant")

    # 使用例
    converter = TaskMarkdownToJson()
    converter.process_markdown_files()