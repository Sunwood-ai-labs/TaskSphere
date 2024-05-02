import os
import requests
from termcolor import colored
from art import *
import pprint

script_name = os.path.basename(__file__)
tprint(script_name)

# 環境変数からGitHubのPersonal Access Tokenを取得
token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
user_login = os.environ.get("GITHUB_USER_LOGIN")
project_number = os.environ.get("GITHUB_PROJECT_NUMBER")

# トークンが設定されていない場合はエラーを表示して終了
if token is None or user_login is None or project_number is None:
    print("Error: Required environment variables are not set.")
    exit(1)

# プロジェクト情報を取得するためのGraphQLクエリ
query_project = """
query {
  user(login: "USER_LOGIN") {
    projectV2(number: NUMBER) {
      title
      id
    }
  }
}
"""

# フィールド情報を取得するためのGraphQLクエリ
query_fields = """
query {
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2Field {
            id
            name
          }
          ... on ProjectV2IterationField {
            id
            name
            configuration {
              iterations {
                startDate
                id
              }
            }
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

# クエリ内のプレースホルダーを実際の値に置き換える
query_project = query_project.replace("USER_LOGIN", user_login)
query_project = query_project.replace("NUMBER", project_number)

# リクエストヘッダー
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# プロジェクト情報を取得するためのリクエストデータ
data_project = {
    "query": query_project
}

# プロジェクト情報を取得するためにGitHub APIにPOSTリクエストを送信
response_project = requests.post("https://api.github.com/graphql", headers=headers, json=data_project)

# レスポンスにエラーがあるかどうかを確認
if "errors" in response_project.json():
    print(f"Error: {response_project.json()['errors'][0]['message']}")
    exit(1)

# レスポンスからプロジェクトのタイトルとIDを取得
project_title = response_project.json()["data"]["user"]["projectV2"]["title"]
project_id = response_project.json()["data"]["user"]["projectV2"]["id"]

print(colored(f"Project Title: {project_title}", "green"))
print(colored(f"Project ID: {project_id[:4]}XXXXXXXXXX", "cyan"))

# フィールド情報を取得するためのクエリ内のプレースホルダーを実際の値に置き換える
query_fields = query_fields.replace("PROJECT_ID", project_id)

# フィールド情報を取得するためのリクエストデータ
data_fields = {
    "query": query_fields
}

# フィールド情報を取得するためにGitHub APIにPOSTリクエストを送信
response_fields = requests.post("https://api.github.com/graphql", headers=headers, json=data_fields)

# レスポンスにエラーがあるかどうかを確認
if "errors" in response_fields.json():
    print(f"Error: {response_fields.json()['errors'][0]['message']}")
    exit(1)

# レスポンスからフィールド情報を取得
fields = response_fields.json()["data"]["node"]["fields"]["nodes"]

# pprint.pprint(fields)
print("---------------------------")
print(colored("Fields:", "magenta"))
for field in fields:
    print(colored(f"- {field['name']}", "yellow"))
    print(colored(f"  ID: {field['id'][:4]}XXXXXXXXXX", "cyan"))
    if "options" in field:
        print(colored("  Options:", "green"))
        for option in field["options"]:
            print(colored(f"    - {option['name']}", "yellow"))
            print(colored(f"      ID: {option['id']}", "cyan"))
    if "configuration" in field:
        print(colored("  Iterations:", "green"))
        for iteration in field["configuration"]["iterations"]:
            print(colored(f"    - Start Date: {iteration['startDate']}", "yellow"))
            print(colored(f"      ID: {iteration['id']}", "cyan"))