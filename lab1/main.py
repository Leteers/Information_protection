import os
import subprocess
rel_path = "docs/leasing.txt"
hsh = subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst",
                     "-sha1", rel_path], stdout=subprocess.PIPE).stdout.decode().strip()
hsh = hsh[hsh.find(" ")+1:]


def main():
    args = init()
    new_sha1 = args[0]
    counter = args[1]
    while counter < 300 and new_sha1 != hsh:
        with open(f"docs/leasing{counter-1}.txt", "r", encoding='utf-8') as f:
            with open(f"docs/leasing{counter}.txt", "w", encoding='utf-8') as wrt:
                wrt.write("\n")
                a = f.readline()
                while a:
                    wrt.write(a)
                    a = f.readline()
                wrt.close()
        f.close()
        new_sha1 = subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst",
                                   "-sha1", f"docs/leasing{counter}.txt"], stdout=subprocess.PIPE).stdout.decode().strip()
        new_sha1 = new_sha1[new_sha1.find(" ")+1:]
        print(f"leasing{counter}.txt " + new_sha1 + " " +
              str(os.path.getsize(f"docs/leasing{counter}.txt")) + " bytes. Size difference: " + str(os.path.getsize(f"docs/leasing{counter}.txt") - os.path.getsize("docs/leasing.txt")) + " bytes.")
        counter += 1


def init():
    with open(rel_path, "r", encoding='utf-8') as f:
        with open("docs/leasing0.txt", "w", encoding='utf-8') as wrt:
            wrt.write("\n")
            a = f.readline()
            while a:
                wrt.write(a)
                a = f.readline()
            wrt.close()
        f.close()
    new_sha1 = subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst",
                              "-sha1", 'docs/leasing0.txt'], stdout=subprocess.PIPE).stdout.decode().strip()
    new_sha1 = new_sha1[new_sha1.find(" ")+1:]
    counter = 1
    return[new_sha1, counter]


if __name__ == "__main__":
    main()
