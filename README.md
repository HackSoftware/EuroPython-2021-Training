# EuroPython 2021 Training

This is the repository with materials for the [Building a practical Slack bot with Python & FastAPI
](https://ep2021.europython.eu/talks/9xzPSHe-building-a-practical-slack-bot-with-python-fastapi-training/) training.

[Slides can be found here](https://docs.google.com/presentation/d/1h3mHULQQrtyvmiTPuneqhpEH3l9yzpLIgL-r_bUCHSg/edit?usp=sharing)

## Overview

![Slack Chat Bot@2x](https://user-images.githubusercontent.com/387867/126901049-4a965bad-41b4-4168-8ba7-05cc4322dee3.png)

## Step 0 - OS setup

This training is using the following OS tools:

1. `curl` - for making HTTP calls.
1. `jq` - for pretty printing JSON results.

But in case you don't have them, it's not a problem and we don't need them for the final solution.

## Step 1 - Python setup

To run everything from here, we recommend the following Python setup:

1. Use the latest Python version (`3.9.6` by the time of writing).
1. Create a fresh virtual environment for the training.
1. Create a fresh directory to contain everything for this training.

To achieve the points above, use the tools that you use everyday.

We recommend using:

1. [pyenv](https://github.com/pyenv/pyenv)
1. [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## Step 2 - Slack setup

We are going to need a test Slack workspace for this training.

The best approach here is to create a brand new one, but feel free to reuse already existing one.

## Step 3 - FastAPI setup

Now, we are going to create one small FastAPI app and expose an endpoint to test with.

First, we need to install the dependencies:

```
pip install fastapi
pip install uvicorn[standard] # or uvicorn\[standard\] depending on your shell
```

Then, in the working directory, create a file called `main.py` with the following contents:

```python
from fastapi import Body, FastAPI, Request, Response

app = FastAPI()


@app.post("/echo")
async def echo(request: Request, response: Response, data=Body(...)):
    raw_body = await request.body()
    body = raw_body.decode("utf-8")

    print(data)

    return {
        "data": data,
        "raw_body": body,
        "headers": request.headers
    }
```

Now, lets run our server:

```
uvicorn main:app --reload
```

And test it by issuing a POST request via `curl` (or any other HTTP client that you find suitable):

```bash
curl -s -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://localhost:8000/echo
```

Few things to note:

1. We are using `-s` for a "silent" curl output, skipping the progress bar.
1. We are sending the `Content-Type` header, set to `application/json`, because this triggers FastAPI to parse the JSON into the `body` argument.

An example response would look like that:

```json
{
  "data": {
    "key": "value"
  },
  "raw_body": "{\"key\": \"value\"}",
  "headers": {
    "host": "localhost:8000",
    "user-agent": "curl/7.58.0",
    "accept": "*/*",
    "content-type": "application/json",
    "content-length": "16"
  }
}
```

## Step 4 - Slack app setup

Now, we are going to setup an app within our new Slack workspace, so we can start communicating with our server.

1. Navigate to <https://api.slack.com/>
1. Click on the `Create an app` button
1. Click on the `Create New App` button
1. Select `From scratch`
1. Type `EuroPython Bot` in the `App Name` field
1. Select your newly created workspace

After following those steps, you should end up with a screen that looks something like that:

![image](https://user-images.githubusercontent.com/387867/126795187-59ed6d31-e0a2-4ebe-9713-727a525b4762.png)

Before we continue further, we'll need 1 more thing.

## Step 5 - ngrok setup

Since we are going to listen for events from Slack & those events are going to be HTTP POST requests, we need a way to tell Slack how to find our `localhost:8000` server.

One way of doing this is using [`ngrok`](https://ngrok.com/) - a piece of software that's going to create a tunnel to our localhost & give us a public url, that we'll post in Slack.

Navigate to the [download page](https://ngrok.com/download) and download ngrok for you OS & platform.

Once extracted, in a new shell, while our FastAPI server is running, type:

```
./ngrok http 8000
```

This will run `ngrok` and present us with the public url. Copy that url.

## Step 6 - Testing if we have integrated correctly

Now, back to Slack setup:

1. Go to the `Event Subscriptions` option.
1. Turn it on.
1. Paste your `ngrok` url, pointing to the `/echo` endpoint. In my case, that's `https://c153a68641fd.ngrok.io/echo`
1. If our server & `ngrok` are running, you'll see a green `Verified` in Slack. Check the `ngrok` shell - you should see a request there.
1. Now click on `Subscribe to bot events`, click `Add Bot User Event` and select `app_mention`.
1. Hit `Save Changes`.
1. Leave the page open, since we'll come back here to add additional things.

Now, lets wire everything together, so we can start developing:

1. In the app settings, navigate to `Settings` -> `Basic Information`
1. Click the `Install to Workspace` button.
1. Click `Allow`.
1. Every time we change the permissions or scopes, we'll have to redo this entire process.

Now, open up the Slack workspace:

1. Add the bot (type `/add` in the channel & click on the action item) to a random channel.
1. `@` the bot and write something.
1. Check your FastAPI console.

The event payload that we received should look something like that:

```json
{
    "token": "C2lhacRaergBLDrNglaNtVYQ",
    "team_id": "T028KF61U7R",
    "api_app_id": "A0290D2N9B4",
    "event": {
        "client_msg_id": "7f025cc5-2f1c-41c9-9ad9-f78d86c13b49",
        "type": "app_mention",
        "text": "<@U0290LLS803> hello :wave:",
        "user": "U028TEER6KY",
        "ts": "1627050528.001000",
        "team": "T028KF61U7R",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "UBr7f",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "user",
                                "user_id": "U0290LLS803"
                            },
                            {
                                "type": "text",
                                "text": " hello "
                            },
                            {
                                "type": "emoji",
                                "name": "wave"
                            }
                        ]
                    }
                ]
            }
        ],
        "channel": "C028TEHTWKG",
        "event_ts": "1627050528.001000"
    },
    "type": "event_callback",
    "event_id": "Ev029Q5P36BA",
    "event_time": 1627050528,
    "authorizations": [
        {
            "enterprise_id": null,
            "team_id": "T028KF61U7R",
            "user_id": "U0290LLS803",
            "is_bot": true,
            "is_enterprise_install": false
        }
    ],
    "is_ext_shared_channel": false,
    "event_context": "3-app_mention-T028KF61U7R-A0290D2N9B4-C028TEHTWKG"
}
```

This means we are now ready with our setup and can start adding funcitonality back.

## Step 7 - Implementing bot behavior (TASKS START HERE)

Now, it's time for our tasks.

**We want to implement the following general behavior:**

1. Whenever someone mentions our bot, we want to reply in the channel with a message.
1. Whenever someone mentions our bot **in a thread**, we want to reply in the same thread with a message.
1. **[BONUS TASK]** Whenever someone mentions our bot, start a new thread by replying to that user.

In order to do that, we want to be making HTTP calls to the Slack API via `requests`, so we need to do:

```
pip install requests
```

### Documentation links to help

Extracted documentation links to help you navigate to the proper stuff to look at:

1. [What is a Slack app?](https://api.slack.com/authentication/basics#start)
1. [Listening to the `app_mention` event](https://api.slack.com/events/app_mention)
1. [Sending messages](https://api.slack.com/messaging/sending)
1. [Retrieving individual messages](https://api.slack.com/messaging/retrieving#individual_messages)


### Hints

Making a call to Slack requires obtaining `Bot User OAuth Token` from the settings page:

![europython](https://user-images.githubusercontent.com/387867/126901159-808b77db-04f2-4b3d-85d0-e6a851155959.png)

Since this is a secret, in order to manage secrets for our app, we recommend using `.env` file and <https://github.com/theskumar/python-dotenv> for parsing it:

```python
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
```

## Step 8 - Validate Slack requests

Everything is great, but our API is public, meaning anyone can call it and start sending messages to our Slack.

**We want to prevent this & your next task is to implement request verification!**

### Documentation links to help

1. [Verifying requests from Slack](https://api.slack.com/authentication/verifying-requests-from-slack)


## Step 9 - Wrapping it up and further references

That's about it.

Materials for further references:

1. Since we are using FastAPI with `async`, you can go & replace `requests` with something that's async, like <https://docs.aiohttp.org/en/stable/>
1. There's an offical [Python Slack SDK](https://github.com/slackapi/python-slack-sdk) that you can use.
1. You can also use [`bolt-python`](https://github.com/slackapi/bolt-python) which is a framework for building Slack apps.
1. [The official documentation, of course](https://api.slack.com/)

