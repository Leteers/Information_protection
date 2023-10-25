from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
app = FastAPI()
import subprocess

#Получение открытого ключа для шифрования файла.
@app.post("/get_pk")
def read_root():
    command='"C:/Program Files/Git/usr/bin/openssl.exe" rsa -pubout -in privatekey.pem -out publickey.pem'
    subprocess.run(command, shell=True, check=True)
    with open('publickey.pem', 'r') as file:
        public_key_str = file.read()
    return {public_key_str}

if __name__ == "__main__":
    command = '"C:/Program Files/Git/usr/bin/openssl.exe" genpkey -algorithm RSA -out privatekey.pem -pkeyopt rsa_keygen_bits:1024'
    subprocess.run(command, shell=True, check=True)
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)