import os
import glob
import re
import json

class TaskMarkdownToJson:
    def __init__(self, input_dir="tmp/responses", output_dir="tmp/converted_tasks", input_pattern="response_*.md", output_prefix="response_", output_extension=".json"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_pattern = input_pattern
        self.output_prefix = output_prefix
        self.output_extension = output_extension

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

    def process_markdown_files(self):
        # 入力ディレクトリから指定されたパターンのファイルを取得し、数値順にソート
        markdown_files = sorted(glob.glob(os.path.join(self.input_dir, self.input_pattern)), key=lambda x: int(x.split("_")[-1].split(".")[0]))

        # 各マークダウンファイルを順番に処理
        for markdown_file in markdown_files:
            with open(markdown_file, "r") as infile:
                # マークダウンファイルの内容を読み込む
                markdown_text = infile.read()

                # マークダウンをパースしてタスクのリストを取得
                tasks = self.parse_markdown(markdown_text)

                # タスクをJSONに変換
                json_output = json.dumps(tasks, ensure_ascii=False, indent=2)

                # 出力ファイル名を生成
                output_file = os.path.join(self.output_dir, self.output_prefix + os.path.splitext(os.path.basename(markdown_file))[0].split("_")[-1] + self.output_extension)

                # JSONを出力ファイルに書き込む
                with open(output_file, "w") as outfile:
                    outfile.write(json_output)

                print(f"タスクが {output_file} に保存されました。")


if __name__ == "__main__":
    # 使用例
    converter = TaskMarkdownToJson()
    converter.process_markdown_files()