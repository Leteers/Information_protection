from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



if __name__ == 