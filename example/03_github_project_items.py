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

# アイテム情報を取得するためのGraphQLクエリ
query_items = """
query {
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      items(first: 20) {
        nodes {
          id
          fieldValues(first: 8) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field {
                  ... on ProjectV2FieldCommon {
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field {
                  ... on ProjectV2FieldCommon {
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2FieldCommon {
                    name
                  }
                }
              }
            }
          }
          content {
            ... on DraftIssue {
              title
              body
            }
            ... on Issue {
              title
              assignees(first: 10) {
                nodes {
                  login
                }
              }
            }
            ... on PullRequest {
              title
              assignees(first: 10) {
                nodes {
                  login
                }
              }
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

# アイテム情報を取得するためのクエリ内のプレースホルダーを実際の値に置き換える
query_items = query_items.replace("PROJECT_ID", project_id)

# アイテム情報を取得するためのリクエストデータ
data_items = {
    "query": query_items
}

# アイテム情報を取得するためにGitHub APIにPOSTリクエストを送信
response_items = requests.post("https://api.github.com/graphql", headers=headers, json=data_items)

# レスポンスにエラーがあるかどうかを確認
if "errors" in response_items.json():
    print(f"Error: {response_items.json()['errors'][0]['message']}")
    exit(1)

# レスポンスからアイテム情報を取得
items = response_items.json()["data"]["node"]["items"]["nodes"]

print("---------------------------")
print(colored("Items:", "magenta"))
for item in items:
    print(colored(f"Item ID: {item['id'][:4]}XXXXXXXXXX", "cyan"))
    
    # フィールド値を表示
    field_values = item["fieldValues"]["nodes"]
    for field_value in field_values:
        if "text" in field_value:
            print(colored(f"{field_value['field']['name']}: {field_value['text']}", "yellow"))
        elif "date" in field_value:
            print(colored(f"{field_value['field']['name']}: {field_value['date']}", "yellow"))
        elif "name" in field_value:
            print(colored(f"{field_value['field']['name']}: {field_value['name']}", "yellow"))
    
    # コンテンツの情報を表示
    content = item["content"]
    if "title" in content:
        print(colored(f"Title: {content['title']}", "green"))
    if "body" in content:
        print(colored(f"Body: {content['body']}", "green"))
    if "assignees" in content:
        assignees = [assignee["login"] for assignee in content["assignees"]["nodes"]]
        print(colored(f"Assignees: {', '.join(assignees)}", "green"))
    
    print("---")