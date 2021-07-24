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
