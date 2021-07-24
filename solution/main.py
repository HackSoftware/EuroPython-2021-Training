from pprint import pprint

from benedict import benedict

from fastapi import Body, FastAPI, Request, Response

app = FastAPI()


@app.post("/echo")
async def echo(request: Request, response: Response, data=Body(...)):
    raw_body = await request.body()
    body = raw_body.decode("utf-8")

    # We need to add the `channels:read` scope
    # From the `OAuth & Permissions` section in the bot settings
    # This will give us `data.event.channel`, which is the channe id,
    # So we can post back a message
    pprint(data)

    payload = benedict(data)

    event_type = payload.get("event.type")
    channel_id = payload.get("event.channel")

    if event_type == "app_mention":
        # Send the message here
        print(channel_id)

    return {
        "data": data,
        "raw_body": body,
        "headers": request.headers
    }
