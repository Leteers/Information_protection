import os
import subprocess
import time
rel_path = "tux.png"


def main():
    subprocess.run('"C:/Program Files/Git/usr/bin/openssl.exe" rand -hex 16 > key.bin',
                   shell=True, stdout=subprocess.PIPE)
    start=time.time()
    subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "enc",
                    "-aes-256-ecb", "-in", rel_path, "-out", "new_ecb.txt","-pbkdf2", "-pass", "file:key.bin"], stdout=subprocess.PIPE)
    finish=time.time()
    print("ECB: "+str(finish-start) + "secs. Size: " + str(os.path.getsize("new_ecb.txt")) + " bytes.")
    start = time.time()
    subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "enc",
                    "-aes-256-cbc", "-in", rel_path, "-out", "new_cbc.txt","-pbkdf2", "-pass", "file:key.bin"], stdout=subprocess.PIPE)
    finish = time.time()
    print("CBC: "+str(finish-start) + "secs. Size: " + str(os.path.getsize("new_cbc.txt")) + " bytes.")
    start = time.time()
    subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "enc",
                    "-aes-256-cfb", "-in", rel_path, "-out", "new_cfb.txt", "-pbkdf2", "-pass", "file:key.bin"], stdout=subprocess.PIPE)
    finish= time.time()
    print("CFB: "+str(finish-start) + "secs. Size: " + str(os.path.getsize("new_cfb.txt")) + " bytes.")
    start=time.time()
    subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "enc",
                    "-aes-256-ofb", "-in", rel_path, "-out", "new_ofb.txt", "-pbkdf2", "-pass", "file:key.bin"], stdout=subprocess.PIPE)
    finish= time.time()
    print("OFB: "+str(finish-start) + "secs. Size: " + str(os.path.getsize("new_ofb.txt")) + " bytes.")
    

def decode(path, type):
    type = str.lower(type)
    subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "enc", "-d",
                    f"-aes-256-{type}", "-in", path, "-out", f"new_{type}.png", "-pbkdf2", "-pass", "file:key.bin"], stdout=subprocess.PIPE)

if __name__ == "__main__":
    main()
    decode("new_ecb.txt", "ECB")