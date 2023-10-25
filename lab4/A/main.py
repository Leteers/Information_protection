from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def start_page_get(request: Request):

    
    return templates.TemplateResponse('message.html', {'request': request})



if __name__ == "__main__":
    r = requests.post("http://localhost:5000/get_pk")
    with open('publickey.pem', 'w') as file:
        file.write(str(r.json()[0]))
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)