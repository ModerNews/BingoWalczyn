from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from bingo import *

app = FastAPI()

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
    # return {'message': 'running'}