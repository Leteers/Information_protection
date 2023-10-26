from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
import secrets
import math
import subprocess


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def start_page_get(request: Request):
    return templates.TemplateResponse('message.html', {'request': request})
 
@app.post("/send_vote",response_class=HTMLResponse)
async def send_vote(request: Request, select : str = Form()):
    message = int.from_bytes(select.encode(), byteorder='big')
    modulus, exponent=get_modulus_and_exponent()
    r=get_r(modulus)
    message_to_send = blind_message(message,r,exponent,modulus)
    req = requests.post("http://localhost:5000/get_vote", json = [message_to_send])

    message_unblind= unblind_signature(int(req.json()),r,modulus)

    message_results=[]
    message_results.append(message)
    message_results.append(message_unblind)

    req = requests.post("http://localhost:5001/count", json = message_results)
    return templates.TemplateResponse('table.html', {'request': request, 'data': req.json()})

def get_r(m):
    r = secrets.randbits(m.bit_length())
    while r>=m or math.gcd(r, m) != 1:
        r = secrets.randbits(m.bit_length())
    return(r)   

def blind_message(message, r, e, n):
    return (message * pow(r, e, n)) % n

def unblind_signature(message, r, n):
    return (message * pow(r, -1, n)) % n


def get_modulus_and_exponent():
    command= '"C:/Program Files/Git/usr/bin/openssl.exe" rsa -pubin -inform PEM -text -noout < publickey.pem'
    completed_process=subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    output = completed_process.stdout
    start_modulus = output.rfind("s:")
    end_modulus = output.find("Exponent:")
    start_exponent = output.find("nt:")
    end_exponent = output.find("CompletedProcess")

    modulus_hex = output[start_modulus+2:end_modulus]
    exponent = output[start_exponent+3:end_exponent-10]
    modulus = ''.join(modulus_hex.split()).replace(':', '')
    exponent.replace(" ", "")

    modulus=int(modulus,16)
    exponent=int(exponent)

    return(modulus,exponent)
if __name__ == "__main__":
    r = requests.post("http://localhost:5000/get_pk")
    with open('publickey.pem', 'w') as file:
        file.write(str(r.json()[0]))

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

