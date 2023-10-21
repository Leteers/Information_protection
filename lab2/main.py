from PIL import Image
import subprocess
import random
rel_path = "leasing.txt"
hsh = subprocess.run(["C:/Program Files/Git/usr/bin/openssl.exe", "dgst",
                     "-sha1", rel_path], stdout=subprocess.PIPE).stdout.decode().strip()
hsh = hsh[hsh.find(" ")+1:]
hsh = bin(int(hsh, 16))[2:]


def keygen(file_width, file_height, sha_len):
    a = []
    for i in range(len(sha_len)):
        rx = random.randrange(0, file_width*file_height)
        ry = random.randrange(0, 2)
        while [rx, ry] in a:
            print(rx)
            print(a)
            rx = random.randrange(0, file_width, file_height)
            ry = random.randrange(0, 2)
        else:
            a.append([rx, ry])
    with open('key.txt', 'w') as f:
        f.write(str(a))
    return(a)


def read_bmp_pixels_rgb(file_path):
    with open(file_path, 'rb') as bmp_file:
        binary_data = bmp_file.read()

    pixel_data = []

    if len(binary_data)%3==0:
        start=0
    else:
        start=122

    for i in range(start, len(binary_data), 3):
        r, g, b = binary_data[i], binary_data[i + 1], binary_data[i + 2]
        r_bits = format(r, '08b')
        g_bits = format(g, '08b')
        b_bits = format(b, '08b')
        pixel_data.append([r_bits, g_bits, b_bits])

    return pixel_data


def create_image_from_pixels(pixel_data, width, height, file_path):
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixel_data[y * width + x]
            pixels[x, height - y - 1] = (int(r, 2), int(g, 2), int(b, 2))
    img.save(file_path)


def LSB_Replacement(file_width, file_height, sha, pixel_data):
    key = keygen(file_width, file_height, sha)
    # Ключ хранит в себе значения переменных pixel_data в которых хранятся хеш значения. Слева направа.
    for i in range(len(key)):
        # print(pixel_data[key[i][0]][key[i][1]])
        # print(int(sha[i]))
        pixel_data[key[i][0]][key[i][1]] = bin(
            (int(pixel_data[key[i][0]][key[i][1]], 2) & ~1) | int(sha[i]))[2:]  # Перевожу значения в инт чтобы было более понятно, что происходит.
        # print(pixel_data[key[i][0]][key[i][1]])
    create_image_from_pixels(pixel_data, file_width,
                             file_height, output_file_path)


def return_sha1_hash(pixel_data):
    fin=""
    with open("key.txt", "r") as f:
        key= f.readline()
    key = eval(key)
    for i in range(len(key)):
        a = bin(int(pixel_data[key[i][0]][key[i][1]], 2) & 1)
        a = a[len(a)-1:]
        fin+=str(a)
    return(fin)
path = "28.bmp"
a = read_bmp_pixels_rgb(path)

width = 431
height = 378
output_file_path = 'output.bmp'
new_file= read_bmp_pixels_rgb(output_file_path)
# LSB_Replacement(width, height, hsh, a)
# keygen(width,height,hsh)

print(return_sha1_hash(new_file))
print(hsh)
