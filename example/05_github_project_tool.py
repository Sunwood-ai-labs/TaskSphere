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
    query_items = query_items.replace("PROJECT_ID", project_id)

    data_items = {
        "query": query_items
    }

    response_items = requests.post("https://api.github.com/graphql", headers=headers, json=data_items)

    if "errors" in response_items.json():
        print(f"Error: {response_items.json()['errors'][0]['message']}")
        exit(1)

    items = response_items.json()["data"]["node"]["items"]["nodes"]
    fields = response_items.json()["data"]["node"]["fields"]["nodes"]

    print("---------------------------")
    print(colored("Items:", "magenta"))
    for item in items:
        print(colored(f"Item ID: {item['id']}_XXXXXXXXXXXX", "cyan"))

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

    print("---------------------------")
    print(colored("Fields:", "magenta"))
    for field in fields:
        print(colored(f"Field ID: {field['id']}", "cyan"))
        print(colored(f"Field Name: {field['name']}", "green"))
        
        if "configuration" in field:
            iterations = field["configuration"]["iterations"]
            for iteration in iterations:
                print(colored(f"Iteration ID: {iteration['id']}", "cyan"))
                print(colored(f"Iteration Start Date: {iteration['startDate']}", "green"))
        
        if "options" in field:
            options = field["options"]
            for option in options:
                print(colored(f"Option ID: {option['id']}", "cyan"))
                print(colored(f"Option Name: {option['name']}", "green"))
        
        print("---")

def update_item_field_value(project_id, item_id, field_id, field_type, field_value):
    mutation_update_field = """
    mutation {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: "PROJECT_ID"
          itemId: "ITEM_ID"
          fieldId: "FIELD_ID"
          value: {
            FIELD_TYPE: FIELD_VALUE
          }
        }
      ) {
        projectV2Item {
          id
        }
      }
    }
    """
    mutation_update_field = mutation_update_field.replace("PROJECT_ID", project_id)
    mutation_update_field = mutation_update_field.replace("ITEM_ID", item_id)
    mutation_update_field = mutation_update_field.replace("FIELD_ID", field_id)
    mutation_update_field = mutation_update_field.replace("FIELD_TYPE", field_type)
    mutation_update_field = mutation_update_field.replace("FIELD_VALUE", field_value)

    data_update_field = {
        "query": mutation_update_field
    }

    response_update_field = requests.post("https://api.github.com/graphql", headers=headers, json=data_update_field)

    if "errors" in response_update_field.json():
        print(f"Error: {response_update_field.json()['errors'][0]['message']}")
    else:
        updated_item_id = response_update_field.json()["data"]["updateProjectV2ItemFieldValue"]["projectV2Item"]["id"]
        print(colored(f"Updated item field with ID: {updated_item_id}", "green"))

if __name__ == "__main__":
    validate_environment_variables()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    project_id = get_project_info()
    get_project_items(project_id)


    item_id = input("Enter the ID of the item to update: ")
    field_id = input("Enter the ID of the field to update: ")
    field_type = input("Enter the type of the field (text, number, date): ")

    if field_type == "text":
        field_value = f'"{input("Enter the new text value: ")}"'
    elif field_type == "number":
        field_value = input("Enter the new number value: ")
    elif field_type == "date":
        field_value = f'"{input("Enter the new date value (YYYY-MM-DD): ")}"'
    else:
        print("Invalid field type.")
        exit(1)

    update_item_field_value(project_id, item_id, field_id, field_type, field_value)