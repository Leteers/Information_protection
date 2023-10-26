from fastapi import FastAPI, Request, Form, Cookie, File, Response, Body, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import subprocess
from typing import List

app = FastAPI()


# Получение открытого ключа для шифрования файла.
@app.post("/get_pk")
def read_root():
    command = '"C:/Program Files/Git/usr/bin/openssl.exe" rsa -pubout -in privatekey.pem -out publickey.pem'
    subprocess.run(command, shell=True, check=True)
    with open('publickey.pem', 'r') as file:
        public_key_str = file.read()
    return {public_key_str}


@app.post("/get_vote")
def authorize(request: Request, message: List[int]):
    p_exponent = get_private_exponent()
    modulus, exponent = get_modulus_and_exponent()
    return(sign_blinded_message(message[0], p_exponent, modulus))


def sign_blinded_message(message, privare_exponent, modulus):
    return pow(message, privare_exponent, modulus)


def get_private_exponent():
    command = '"C:/Program Files/Git/usr/bin/openssl.exe" rsa -inform PEM -text -noout < privatekey.pem'
    completed_process = subprocess.run(
        command, shell=True, check=True, capture_output=True, text=True)
    output = str(completed_process.stdout)
    output = output[output.find("privateExponent:")+16:output.find("prime1:")]
    p_exponent = ''.join(output.split()).replace(':', '')
    p_exponent = int(p_exponent, 16)
    return(p_exponent)


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
    command = '"C:/Program Files/Git/usr/bin/openssl.exe" genpkey -algorithm RSA -out privatekey.pem -pkeyopt rsa_keygen_bits:1024'
    subprocess.run(command, shell=True, check=True)
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
