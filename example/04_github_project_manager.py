import os
import requests
from termcolor import colored
from art import *

import pprint

script_name = os.path.basename(__file__)
tprint(script_name)

token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
user_login = os.environ.get("GITHUB_USER_LOGIN")
project_number = os.environ.get("GITHUB_PROJECT_NUMBER")

def validate_environment_variables():
    if token is None or user_login is None or project_number is None:
        print("Error: Required environment variables are not set.")
        exit(1)

def get_project_info():
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
    query_project = query_project.replace("USER_LOGIN", user_login)
    query_project = query_project.replace("NUMBER", project_number)

    data_project = {
        "query": query_project
    }

    response_project = requests.post("https://api.github.com/graphql", headers=headers, json=data_project)

    if "errors" in response_project.json():
        print(f"Error: {response_project.json()['errors'][0]['message']}")
        exit(1)

    project_title = response_project.json()["data"]["user"]["projectV2"]["title"]
    project_id = response_project.json()["data"]["user"]["projectV2"]["id"]

    print(colored(f"Project Title: {project_title}", "green"))
    print(colored(f"Project ID: {project_id}", "cyan"))

    return project_id

def get_project_items(project_id):
    query_items = """
    query {
      node(id: "PROJECT_ID") {
        ... on ProjectV2 {
          items(first: 20) {
            nodes {
              id
              content {
                ... on DraftIssue {
                  title
                  body
                }
                ... on Issue {
                  title
                  number
                  assignees(first: 10) {
                    nodes {
                      login
                    }
                  }
                }
                ... on PullRequest {
                  title
                  number
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
    query_items = query_items.replace("PROJECT_ID", project_id)

    data_items = {
        "query": query_items
    }

    response_items = requests.post("https://api.github.com/graphql", headers=headers, json=data_items)

    if "errors" in response_items.json():
        print(f"Error: {response_items.json()['errors'][0]['message']}")
        exit(1)

    items = response_items.json()["data"]["node"]["items"]["nodes"]

    print("---------------------------")
    print(colored("Items:", "magenta"))
    for item in items:
        print(colored(f"Item ID: {item['id'][:6]}_XXXXXXXXXXXX", "cyan"))

        content = item["content"]
        if "title" in content:
            print(colored(f"Title: {content['title']}", "green"))
        if "body" in content:
            print(colored(f"Body: {content['body']}", "green"))
        if "number" in content:
            print(colored(f"Number: {content['number']}", "green"))
            
            # Get the node_id for the issue or pull request
            if "Issue" in content["__typename"]:
                node_id = requests.get(f"https://api.github.com/repos/{user_login}/{repo_name}/issues/{content['number']}", headers=headers).json()["node_id"]
            elif "PullRequest" in content["__typename"]:
                node_id = requests.get(f"https://api.github.com/repos/{user_login}/{repo_name}/pulls/{content['number']}", headers=headers).json()["node_id"]
            
            print(colored(f"Node ID: {node_id}", "cyan"))
        
        if "assignees" in content:
            assignees = [assignee["login"] for assignee in content["assignees"]["nodes"]]
            print(colored(f"Assignees: {', '.join(assignees)}", "green"))
        
        print("---")

def add_item_to_project(project_id):
    content_id = input("Enter the ID of the content (Issue or Pull Request) to add to the project: ")

    mutation_add_item = """
    mutation {
      addProjectV2ItemById(input: {projectId: "PROJECT_ID", contentId: "CONTENT_ID"}) {
        item {
          id
        }
      }
    }
    """
    mutation_add_item = mutation_add_item.replace("PROJECT_ID", project_id)
    mutation_add_item = mutation_add_item.replace("CONTENT_ID", content_id)

    data_add_item = {
        "query": mutation_add_item
    }

    response_add_item = requests.post("https://api.github.com/graphql", headers=headers, json=data_add_item)

    if "errors" in response_add_item.json():
        print(f"Error: {response_add_item.json()['errors'][0]['message']}")
    else:
        added_item_id = response_add_item.json()["data"]["addProjectV2ItemById"]["item"]["id"]
        print(colored(f"Added item with ID: {added_item_id}", "green"))

def add_draft_issue_to_project(project_id):
    draft_title = input("Enter the title for the new draft issue: ")
    draft_body = input("Enter the body for the new draft issue: ")

    mutation_add_draft_issue = """
    mutation {
      addProjectV2DraftIssue(input: {projectId: "PROJECT_ID", title: "TITLE", body: "BODY"}) {
        projectItem {
          id
        }
      }
    }
    """
    mutation_add_draft_issue = mutation_add_draft_issue.replace("PROJECT_ID", project_id)
    mutation_add_draft_issue = mutation_add_draft_issue.replace("TITLE", draft_title)
    mutation_add_draft_issue = mutation_add_draft_issue.replace("BODY", draft_body)

    data_add_draft_issue = {
        "query": mutation_add_draft_issue
    }

    response_add_draft_issue = requests.post("https://api.github.com/graphql", headers=headers, json=data_add_draft_issue)

    if "errors" in response_add_draft_issue.json():
        print(f"Error: {response_add_draft_issue.json()['errors'][0]['message']}")
    else:
        added_draft_issue_id = response_add_draft_issue.json()["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]
        print(colored(f"Added draft issue with ID: {added_draft_issue_id}", "green"))

if __name__ == "__main__":
    validate_environment_variables()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    project_id = get_project_info()
    get_project_items(project_id)
    # add_item_to_project(project_id)
    add_draft_issue_to_project(project_id)