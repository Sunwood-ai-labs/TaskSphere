import os
import glob
from litellm import completion
from art import *
from termcolor import colored

class TaskBreakdown:
    def __init__(self, tmp_folder, template_path="template/_prompt_task2subtask.md", model_name="groq/llama3-70b-8192", max_tokens=None, temperature=None, api_base=None):
        self.tmp_folder = tmp_folder
        self.save_folder = "tmp"
        self.template_path = template_path
        self.prompt_folder = os.path.join(self.save_folder, "prompts")
        self.response_folder = os.path.join(self.save_folder, "responses")
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.api_base = api_base
        self.create_folders()
        self.load_template()

    def create_folders(self):
        os.makedirs(self.prompt_folder, exist_ok=True)
        os.makedirs(self.response_folder, exist_ok=True)

    def load_template(self):
        with open(self.template_path, "r", encoding="utf-8") as file:
            self.template = file.read()

    def get_task_files(self, task_limit=3):
        task_files = glob.glob(os.path.join(self.tmp_folder, "task_*.md"))[:task_limit]
        return task_files

    def read_task_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            task_content = file.read()
        return task_content

    def save_prompt(self, task_id, prompt):
        prompt_file = os.path.join(self.prompt_folder, f"prompt_{task_id}.md")
        with open(prompt_file, "w", encoding="utf-8") as file:
            file.write(prompt)

    def save_response(self, task_id, response):
        response_file = os.path.join(self.response_folder, f"response_{task_id}.md")
        with open(response_file, "w", encoding="utf-8") as file:
            file.write(response)

    def generate_response(self, prompt):
        print(colored(f"Model: {self.model_name}", "cyan"))
        print(colored(f"Prompt: {prompt}", "yellow"))
        response = completion(
            model=self.model_name,
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            api_base=self.api_base
        )
        return response['choices'][0].message.content.strip()

    def process_tasks(self, task_limit=3):
        task_files = self.get_task_files(task_limit)
        for task_file in task_files:
            print(colored(f"Processing task file: {task_file}", "magenta"))
            task_content = self.read_task_file(task_file)
            task_id = os.path.splitext(os.path.basename(task_file))[0].split("task_")[1]
            prompt = self.template.format(TASK=task_content)
            self.save_prompt(task_id, prompt)
            response = self.generate_response(prompt)
            self.save_response(task_id, response)
            print(colored(response, "green"))
            print("-------------------")
            
if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    tprint(script_name)

    task_breakdown = TaskBreakdown(
        tmp_folder="tmp/task",
        template_path="template/_prompt_task2subtask.md",
        model_name="anthropic/claude-3-haiku-20240307",
        max_tokens=None,
        temperature=None,
        api_base=None
    )
    task_breakdown.process_tasks(task_limit=3)