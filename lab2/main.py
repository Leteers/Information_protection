from PIL import Image
import subprocess
import random


path = "28.bmp"
width = 431
height = 378
output_file_path = 'output.bmp'
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
    img = Image.open(file_path)
    pixel_data = list(img.getdata())
    binary_pixel_data = [[format(pixel[0], '08b'), format(
        pixel[1], '08b'), format(pixel[2], '08b')] for pixel in pixel_data]
    return binary_pixel_data


def create_image_from_pixels(pixel_data, width, height, file_path):
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_data[y * width + x]
            pixels[x,  y] = (int(r, 2), int(g, 2), int(b, 2))
    img.save(file_path)
    return 1


def LSB_Replacement(file_width, file_height, sha, pixel_data, output_file_path):
    key = keygen(file_width, file_height, sha)
    # Ключ хранит в себе значения переменных pixel_data в которых хранятся хеш значения. Слева направа.
    for i in range(len(key)):
        pixel_data[key[i][0]][key[i][1]] = bin(
            (int(pixel_data[key[i][0]][key[i][1]], 2) & ~1) | int(sha[i]))[2:]  # Перевожу значения в инт чтобы было более понятно, что происходит.
    create_image_from_pixels(pixel_data, file_width,
                             file_height, output_file_path)


def return_sha1_hash(pixel_data):
    fin = ""
    with open("key.txt", "r") as f:
        key = f.readline()
    key = eval(key)

    for k in range(len(key)):
        a = pixel_data[key[k][0]][key[k][1]]
        a = a[len(a)-1:]
        fin += str(a)
    return(fin)


if __name__ == '__main__':
    a = read_bmp_pixels_rgb(path)
    LSB_Replacement(width, height, hsh, a, output_file_path)
    new_file = read_bmp_pixels_rgb(output_file_path)
    print(return_sha1_hash(new_file))
    print(return_sha1_hash(new_file) == hsh)
