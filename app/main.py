from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from logging.config import dictConfig
import logging
from config import LogConfig

import json
import hashlib

from bingo import *
from Models import *

app = FastAPI()
# {"Player_name": Bingo object}
__players__: dict[str, Bingo] = {}
# {hashed login: "Player_name"}
__hashes__: dict[str, str] = {}
global winner
winner = None

app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory='../templates')

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")


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

@app.get("/game-end")
async def game_end(request: Request):
    return templates.TemplateResponse('winner.html', {"request": request})

@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data['event'] == 'register_user':
            __players__[data['username']] = Bingo()
            __hashes__[hashlib.sha256(data["username"].encode()).hexdigest()] = data['username']
            await websocket.send_json({"event": "user_registry", "username": data["username"],
                                       "hash": hashlib.sha256(data["username"].encode()).hexdigest()})

        elif data['event'] == 'update_user':
            data = Update.parse_obj(data)
            __players__[__hashes__[data.hash]][data.column][data.row] = 1
            if __players__[__hashes__[data.hash]].check_winner():
                await websocket.send_json({'event': "game_end",
                                           'user': __hashes__[data.hash]})
                logger.info(f'Winner is {__hashes__[data.hash]}')
            logger.warning(f'Updated {data.column}.{data.row} for {__hashes__[data.hash]}')
