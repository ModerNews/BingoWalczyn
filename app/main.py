from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json

from bingo import *

app = FastAPI()
# {"Player_name": Bingo object}
__players__: dict[str, Bingo] = {}

app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory='../templates')

@app.get("/")
async def root():
    with open("../index.html") as file:
        html_content = file.read()
    return HTMLResponse(html_content)
    # return {'message': 'running'}


@app.get("/bingo")
async def bingo(request: Request):
    data = generate_bingo('words.txt')
    return templates.TemplateResponse('bingo.html', {"request": request, "bingo": data})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = json.load(data)
        if data['event'] == 'register_user':
            __players__[data['username']] = Bingo()

        elif data['event'] == 'update_user'
