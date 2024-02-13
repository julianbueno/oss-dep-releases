import json
import requests
import os


def send_message_to_webhook(message):
    """
    Send a message to a slack webhook
    """

    webhook_url = os.environ["SLACK_HOOK"]
    slack_data = {'text': message}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(f"Request returned an error {response.status_code},"
                         f"the response is:\n{response.text}'s")
