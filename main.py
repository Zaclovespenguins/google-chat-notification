import json
import os
import uuid

from github import Github
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

    for commit in commits:
        body += f"Commit {commit['id'][-7:]} - {commit['message']} \n"

    # {'author': {'email': '105678604+ZacAtPeak@users.noreply.github.com', 'name': 'ZacAtPeak', 'username': 'ZacAtPeak'}, 'committer': {'email': '105678604+ZacAtPeak@users.noreply.github.com', 'name': 'ZacAtPeak', 'username': 'ZacAtPeak'}, 'distinct': True, 'id': '13de7ced3f61f29e7bc5206db77d58459dff9a45', 'message': 'Update notify-chat-test copy.yml', 'timestamp': '2026-01-29T13:27:14-07:00', 'tree_id': '59c54477306f61cc5224e6d669a46be1bf429d9d', 'url': 'https://github.com/gitglacier/conversion-scripts/commit/13de7ced3f61f29e7bc5206db77d58459dff9a45'}

    unique_id = str(uuid.uuid4())

    # author = push_details["head_commit"]["committer"]["name"]
    # added_files = []
    # removed_files = []
    # updated_files = []
    # commit_messages = []

    # for commit in push_details["commits"]:
    #     added_files += commit["added"]
    #     updated_files += commit["modified"]
    #     removed_files += commit["removed"]
    #     commit_messages += f"Commit {commit['id']} - {commit['message']} \n"

    # added_files = set(added_files)
    # removed_files = set(removed_files)
    # updated_files = set(updated_files)
    # commit_messages = set(commit_messages)

    # body = ""

    # if added_files:
    #     body += "\n" + f"{added_files}"
    # if updated_files:
    #     body += "\n" + f"{updated_files}"
    # if removed_files:
    #     body += "\n" + f"{removed_files}"

    # if commit_messages:
    #     body += "\n" + f"{commit_messages}"

    cardV2 = {
        "cardsV2": [
            {
                "cardId": unique_id,
                "card": {
                    "header": {"title": f"{'Zac'} pushed {'6'} new commits"},
                    "sections": [
                        {
                            "header": "Commit Message",
                            "collapsible": "false",
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": "No commit message provided.",
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
                                                    "openLink": {"url": f"{'repo'}"}
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
                                                        "url": f"https://zaclovespenguins.github.io/google-chat-notification/?repo={'REPO'}"
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
