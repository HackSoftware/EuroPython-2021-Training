import hmac
import hashlib

from pprint import pprint

import requests

from benedict import benedict

from dotenv import dotenv_values

from fastapi import Body, FastAPI, Request, Response, status

config = dotenv_values(".env")

app = FastAPI()


# This token can be obtained from the `OAuth Tokens for Your Workspace` section
# In `OAuth & Permissions` in the bot settings
BOT_TOKEN = config["BOT_TOKEN"]
SIGNING_SECRET = config["SIGNING_SECRET"]


def slack_validate_request(timestamp, body, slack_signature):
    sig_basestring = 'v0:' + timestamp + ':' + body

    signature = 'v0=' + hmac.new(
        SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature == slack_signature


@app.post("/echo")
async def echo(request: Request, response: Response, data=Body(...)):
    raw_body = await request.body()
    body = raw_body.decode("utf-8")

    # We are following the guide from here:
    # https://api.slack.com/authentication/verifying-requests-from-slack
    slack_timestamp = request.headers['x-slack-request-timestamp']
    slack_signature = request.headers['x-slack-signature']

    is_valid = slack_validate_request(slack_timestamp, body, slack_signature)

    if not is_valid:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    # We need to add the `channels:read` scope
    # From the `OAuth & Permissions` section in the bot settings
    # This will give us `data.event.channel`, which is the channe id,
    # So we can post back a message
    pprint(data)

    payload = benedict(data)

    event_type = payload.get("event.type")
    channel_id = payload.get("event.channel")
    thread_ts = payload.get("event.thread_ts")

    if event_type == "app_mention":
        send_message_payload = {
            "channel": channel_id,
            "text": "Pinging back in the channel"
        }

        if thread_ts is not None:
            send_message_payload["thread_ts"] = thread_ts
            send_message_payload["text"] = "Replying back in a thread"

        headers = {
            "Authorization": f"Bearer {BOT_TOKEN}"
        }

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json=send_message_payload
        )
        # We do that to debug any incoming errors from Slack
        pprint(response.text)

    return {
        "data": data,
        "raw_body": body,
        "headers": request.headers
    }
