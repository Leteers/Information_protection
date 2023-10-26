from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import subprocess
import uvicorn
import requests
from database import Connection
app = FastAPI()


choice = {f'{int.from_bytes("Алексей".encode(), byteorder="big")}':"Алексей", f'{int.from_bytes("Иван".encode(), byteorder="big")}':"Иван", f'{int.from_bytes("Анастасия".encode(), byteorder="big")}':"Анастасия"}

@app.post("/count")
def vote_count(request: Request, file_keys: List[int]):
    moodulus, exponent = get_modulus_and_exponent()
    connection = Connection()
    if verify_signature(file_keys[1], file_keys[0], exponent, moodulus):
        connection.push(choice[str(file_keys[0])],file_keys[1])
    res = connection.get_results()
    ret=[]
    for i in range(len(res)):
        ret.append({'name': res[i][0],'votes':res[i][1]})
    return ret

def verify_signature(signed_m, m, e, n):
    return pow(signed_m, e, n) == m


def get_modulus_and_exponent():
    command = '"C:/Program Files/Git/usr/bin/openssl.exe" rsa -pubin -inform PEM -text -noout < publickey.pem'
    completed_process = subprocess.run(
        command, shell=True, check=True, capture_output=True, text=True)
    output = completed_process.stdout
    start_modulus = output.rfind("s:")
    end_modulus = output.find("Exponent:")
    start_exponent = output.find("nt:")
    end_exponent = output.find("CompletedProcess")
    modulus_hex = output[start_modulus+2:end_modulus]
    exponent = output[start_exponent+3:end_exponent-10]
    modulus = ''.join(modulus_hex.split()).replace(':', '')
    exponent.replace(" ", "")
    modulus = int(modulus, 16)
    exponent = int(exponent)

    return(modulus, exponent)


if __name__ == "__main__":
    r = requests.post("http://localhost:5000/get_pk")
    with open('publickey.pem', 'w') as file:
        file.write(str(r.json()[0]))
    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
