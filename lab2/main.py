import hashlib
with open("leasing.txt",'rb') as f:
    hash_object = hashlib.sha1(f.read())
    hex_dig = hash_object.hexdigest()

print('16a811e9c6cafab963b1e35f5c5cb6108dee5b64'==hex_dig)
import os
import hashlib
import subprocess
a=subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst", "-sha1", 'leasing.txt'], stdout=subprocess.PIPE).stdout.decode().strip()
print(a[a.find(" ")+1:])