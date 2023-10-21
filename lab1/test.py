import os
import hashlib
import subprocess

def main():
    try:
        file_path = "C:/Users/fn111/Desktop/Polytech/6/Peresdachi/Information_protection/lab1"
        other_way(file_path)

        git_dir_path = "C:/Users/fn111/Desktop/Polytech/6/Peresdachi/Information_protection/lab1/docs"
        subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst", "-sha1", os.path.join(git_dir_path, "leasing.txt")], cwd=git_dir_path, stdout=subprocess.PIPE)
        file = os.path.join(git_dir_path, "leasing.txt")
        file_size_in_bytes = os.path.getsize(file)
        print(subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst", "-sha1", file], cwd=git_dir_path, stdout=subprocess.PIPE).stdout.decode().strip())
        print(f"Размер исходного файла {file_size_in_bytes} байт")
    except (OSError, subprocess.CalledProcessError) as e:
        print(e)

def process_build(count):
    try:
        new_file_path = f"C:/Users/fn111/Desktop/Polytech/6/Peresdachi/Information_protection/lab1/docs/leasing{count}.txt"
        subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst", "-sha1", new_file_path], cwd=new_file_path, stdout=subprocess.PIPE)
    except (OSError, subprocess.CalledProcessError) as e:
        print(e)

def other_way(file_path):
    try:
        file_name = "/leasing.txt"
        count = 0

        while count < 300:
            space_index = -1
            with open(file_path + file_name, "r", encoding='utf-8') as reader:
                line = reader.readline()
                space_index = line.find(" ", space_index + 1)

                if space_index != -1:
                    count += 1
                    output_file_name = f"/leasing{count}.txt"

                    with open(file_path + output_file_name, "w" ,encoding="utf8") as writer:
                        writer.write(line[:space_index] + "ㅤ" + line[space_index + 1:])
                        writer.write("\n")

                        while True:
                            next_line = reader.readline()
                            if not next_line:
                                break
                            writer.write(next_line)

                    sha1(file_path, output_file_name)
                    file_name = output_file_name

                else:
                    line += "\n" + reader.readline()

    except Exception as e:
        print(e)

def sha1(file_path, output_file_name):
    try:
        sha1_hash = hashlib.sha1()

        with open(file_path + output_file_name, "rb" ) as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                sha1_hash.update(data)

        sha1_hex = sha1_hash.hexdigest()
        file_size_in_bytes = os.path.getsize(file_path + output_file_name)
        print(f"SHA-1 файла {output_file_name}: {sha1_hex}, размер файла {file_size_in_bytes} байт")

        if sha1_hex == "16a811e9c6cafab963b1e35f5c5cb6108dee5b64":
            exit(0)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()