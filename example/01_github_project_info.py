import os
import requests
from termcolor import colored
from art import *

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

# GraphQLクエリ
query = """
query {
  user(login: "USER_LOGIN") {
    projectV2(number: NUMBER) {
      title
      id
    }
  }
}
"""

# クエリ内のプレースホルダーを実際の値に置き換える
query = query.replace("USER_LOGIN", user_login)
query = query.replace("NUMBER", project_number)

# リクエストヘッダー
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# リクエストデータ
data = {
    "query": query
}

# GitHub APIにPOSTリクエストを送信
response = requests.post("https://api.github.com/graphql", headers=headers, json=data)

# レスポンスにエラーがあるかどうかを確認
if "errors" in response.json():
    print(f"Error: {response.json()['errors'][0]['message']}")
    exit(1)

# レスポンスからプロジェクトのタイトルとIDを取得
project_title = response.json()["data"]["user"]["projectV2"]["title"]
project_id = response.json()["data"]["user"]["projectV2"]["id"]

print(colored(f"Project Title: {project_title}", "green"))
print(colored(f"Project ID: {project_id[:4]}XXXXXXXXXX", "cyan"))