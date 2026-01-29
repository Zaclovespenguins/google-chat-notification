from json import dumps
import os
from httplib2 import Http
import uuid

def run(webhook_url, push_details, updated_files, repo_url, commit_url, who_commit):
    unique_id = str(uuid.uuid4())

    author = push_details['head_commit']['committer']['name']
    added_files = []
    removed_files = []
    updated_files = []
    commit_messages = []

    for commit in push_details['commits']:
        added_files += commit['added']
        updated_files += commit['modified']
        removed_files += commit['removed']
        commit_messages += f"Commit {commit['id']} - {commit['message']} \n"

    added_files = set(added_files)
    removed_files = set(removed_files)
    updated_files = set(updated_files)
    commit_messages = set(commit_messages)

    print("TEST")

    body = ""

    if added_files:
        body += "\n" + f"{added_files}"
    if updated_files:
        body += "\n" + f"{updated_files}"
    if removed_files:
        body += "\n" + f"{removed_files}"

    if commit_messages:
        body += "\n" + f"{commit_messages}"

    print(body)

    cardV2 = {
      "cardsV2": [
        {
          "cardId": unique_id,
          "card": {
              "header": {
                "title": f"{author} pushed {len(push_details['commits'])} new commits"
              },
              "sections": [
                {
                  "header": "Commit Message",
                  "collapsible": "false",
                  "widgets": [
                    {
                      "textParagraph": {
                        "text": "No commit message provided.",
                        "maxLines": 2
                      }
                    },
                    {
                      "chipList": {
                        "chips": [
                          {
                            "label": "View Commit on Github",
                            "icon": {
                              "materialIcon": {
                                "name": "search"
                              }
                            },
                            "onClick": {
                              "openLink": {
                                "url": f"{push_details['url']}"
                              }
                            }
                          },
                          {
                            "label": "Open in Github Desktop",
                            "icon": {
                              "materialIcon": {
                                "name": "open_in_new"
                              }
                            },
                            "onClick": {
                              "openLink": {
                                "url": f"https://zaclovespenguins.github.io/google-chat-notification/?repo={repo_url}"
                              }
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              ]
          }
        }
      ]
    }

    # update_files_string = ", ".join(updated_files)
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=webhook_url,
        method="POST",
        headers=message_headers,
        body=dumps(cardV2),
    )
# [Open in GitHub Desktop](x-github-client://openRepo/https://github.com/Zaclovespenguins/google-chat-notification)
# https://zaclovespenguins.github.io/?repo=https://github.com/Zaclovespenguins/google-chat-notification


if __name__ == "__main__":
    webhook_url = os.getenv("INPUT_WEBHOOK_URL")
    push_details = os.getenv("INPUT_PUSH_DETAILS")
    repo_url = os.getenv("INPUT_REPO_URL")
    run(webhook_url, push_details, repo_url)
    # run("https://chat.googleapis.com/v1/spaces/AAQAcy2U53g/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=4Ft202foaB4qk-eCPBKhsCEVFU7iGuSp1jyNdT8Pk1U", push_details, "https://github.com/Zaclovespenguins/google-chat-notification/")
