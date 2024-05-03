import os
import json
import requests
from termcolor import colored
from art import *

class GithubProject:
    def __init__(self):
        self.token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.user_login = os.environ.get("GITHUB_USER_LOGIN")
        self.project_number = os.environ.get("GITHUB_PROJECT_NUMBER")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.tmp_folder = "tmp"
        self.create_tmp_folder()

    def create_tmp_folder(self):
        if not os.path.exists(self.tmp_folder):
            os.makedirs(self.tmp_folder)

    def validate_environment_variables(self):
        if self.token is None or self.user_login is None or self.project_number is None:
            print("Error: Required environment variables are not set.")
            exit(1)

    def get_project_info(self):
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
        query_project = query_project.replace("USER_LOGIN", self.user_login)
        query_project = query_project.replace("NUMBER", self.project_number)

        data_project = {
            "query": query_project
        }

        response_project = requests.post("https://api.github.com/graphql", headers=self.headers, json=data_project)

        if "errors" in response_project.json():
            print(f"Error: {response_project.json()['errors'][0]['message']}")
            exit(1)

        project_title = response_project.json()["data"]["user"]["projectV2"]["title"]
        project_id = response_project.json()["data"]["user"]["projectV2"]["id"]

        print(colored(f"Project Title: {project_title}", "green"))
        print(colored(f"Project ID: {project_id}", "cyan"))

        return project_id


    def get_project_items(self, project_id):
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
        query_items = query_items.replace("PROJECT_ID", project_id)

        data_items = {
            "query": query_items
        }

        response_items = requests.post("https://api.github.com/graphql", headers=self.headers, json=data_items)

        if "errors" in response_items.json():
            print(f"Error: {response_items.json()['errors'][0]['message']}")
            exit(1)

        items = response_items.json()["data"]["node"]["items"]["nodes"]

        self.save_json_to_file("items.json", items)
        self.print_items(items)

        return items

    def save_json_to_file(self, filename, data):
        file_path = os.path.join(self.tmp_folder, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


    def save_task_to_file(self, item):
        template_path = "template/_task.md"
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()

        content = item["content"]
        title = content.get("title", "")
        body = content.get("body", "")
        url = "-- Nothing --"

        field_values = item["fieldValues"]["nodes"]
        for field_value in field_values:
            field_name = field_value["field"]["name"]
            if field_name == "URL" and "text" in field_value:
                url = field_value["text"]
                break

        status = ""
        for field_value in field_values:
            field_name = field_value["field"]["name"]
            if field_name == "Status":
                if "name" in field_value:
                    status = field_value["name"]
                break

        task_content = template.format(Title=title, body=body, Status=status, URL=url)

        task_id = item["id"]
        file_name = f"task_{task_id}.md"
        file_path = os.path.join(self.tmp_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(task_content)

    def print_items(self, items):
        print("---------------------------")
        print(colored("Items:", "magenta"))
        for item in items:
            print(colored(f"Item ID: {item['id']}", "cyan"))

            content = item["content"]
            if "title" in content:
                print(colored(f"Title: {content['title']}", "green"))
            if "body" in content:
                print(colored(f"Body: {content['body']}", "green"))
            
            if "assignees" in content:
                assignees = [assignee["login"] for assignee in content["assignees"]["nodes"]]
                print(colored(f"Assignees: {', '.join(assignees)}", "green"))
            
            field_values = item["fieldValues"]["nodes"]
            for field_value in field_values:
                field_name = field_value["field"]["name"]
                if "text" in field_value:
                    field_value = field_value["text"]
                elif "date" in field_value:
                    field_value = field_value["date"]
                elif "name" in field_value:
                    field_value = field_value["name"]
                print(colored(f"{field_name}: {field_value}", "green"))
            
            self.save_task_to_file(item)
            
            print("---")
        
    def print_fields(self, fields):
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

    def update_item_field_value(self, project_id, item_id, field_id, field_type, field_value):
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

        response_update_field = requests.post("https://api.github.com/graphql", headers=self.headers, json=data_update_field)

        if "errors" in response_update_field.json():
            print(f"Error: {response_update_field.json()['errors'][0]['message']}")
        else:
            updated_item_id = response_update_field.json()["data"]["updateProjectV2ItemFieldValue"]["projectV2Item"]["id"]
            print(colored(f"Updated item field with ID: {updated_item_id}", "green"))

if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    tprint(script_name)

    github_project = GithubProject()
    github_project.validate_environment_variables()

    project_id = github_project.get_project_info()
    github_project.get_project_items(project_id)