import hashlib
with open("leasing.txt",'rb') as f:
    hash_object = hashlib.sha1(f.read())
    hex_dig = hash_object.hexdigest()
 
print('16a811e9c6cafab963b1e35f5c5cb6108dee5b64'==hex_dig)
import os
import subprocess

print("Starting startfile method")
os.startfile('openssl.exe', arguments='')
