import json
import os
import uuid

from httplib2 import Http


def run():
    webhook_url = os.getenv("INPUT_WEBHOOK_URL")
    event_path = os.getenv("GITHUB_EVENT_PATH")
    with open(event_path, "r") as f:
        event_data = json.load(f)

    name = event_data.get("pusher", {}).get("name")
    ref = event_data.get("ref")  # e.g., 'refs/heads/main'
    commits = event_data.get("commits", {})

    body = ""

    # Creating body based on number of commits
    if len(commits) == 1:
        title = f"{name} pushed a new commit"
    else:
        title = f"{name} pushed {len(commits)} new commits"

    for commit in commits:
        body += f"Commit [{commit['id'][-7:]}]({commit_url}) - {commit['message']} \n"

    commit_url = event_data.get("head_commit", {}).get("url")
    repo_url = commit_url.split("commit")[0]
    
    unique_id = str(uuid.uuid4())

    cardV2 = {
        "cardsV2": [
            {
                "cardId": unique_id,
                "card": {
                    "header": {"title": f"{title}"},
                    "sections": [
                        {
                            "header": "Commit Message",
                            "collapsible": "false",
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"{body}",
                                        "maxLines": 2,
                                    }
                                },
                                {
                                    "chipList": {
                                        "chips": [
                                            {
                                                "label": "View Commit on Github",
                                                "icon": {
                                                    "materialIcon": {"name": "search"}
                                                },
                                                "onClick": {
                                                    "openLink": {"url": f"{commit_url}"}
                                                },
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
                                                },
                                            },
                                        ]
                                    }
                                },
                            ],
                        }
                    ],
                },
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
        body=json.dumps(cardV2),
    )


# [Open in GitHub Desktop](x-github-client://openRepo/https://github.com/Zaclovespenguins/google-chat-notification)
# https://zaclovespenguins.github.io/?repo=https://github.com/Zaclovespenguins/google-chat-notification


if __name__ == "__main__":
    run()
    # run("https://chat.googleapis.com/v1/spaces/AAQAcy2U53g/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=4Ft202foaB4qk-eCPBKhsCEVFU7iGuSp1jyNdT8Pk1U", push_details, "https://github.com/Zaclovespenguins/google-chat-notification/")
