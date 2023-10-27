from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import subprocess
import uvicorn
import requests

app = FastAPI()



@app.post("/count")
def vote_count(request: Request, file_keys: List[int]):
    pass
if __name__ == "__main__":

    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
