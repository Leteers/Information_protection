import matplotlib.pyplot as plt
from PIL import Image

width = 200
height = 235
file_path = 'new_image.png'
class GaloisLFSR:
    def __init__(self, initial_state, feedback_polynomial):
        self.state = initial_state
        self.feedback_polynomial = feedback_polynomial
        self.size = len(initial_state)

    def shift(self):
        feedback_bit = sum(int(self.state[i]) * int(self.feedback_polynomial[i]) for i in range(self.size)) % 2
        self.state = self.state[1:] + str(feedback_bit)
        return int(self.state[-1])

    def generate_sequence(self, n):
        return [self.shift() for _ in range(n)]



# Функция для вычисления критерия χ2
def chi_square_test(observed, expected):
    return sum((o - e) ** 2 / e for o, e in zip(observed, expected))

#Получение данных о пикслеях в двоичном представлении.
def read_bmp_pixels_rgb(file_path):
    img = Image.open(file_path)
    pixel_data = list(img.getdata())
    binary_pixel_data = [[format(pixel[0], '08b'), format(
        pixel[1], '08b'), format(pixel[2], '08b')] for pixel in pixel_data]
    return binary_pixel_data

def encode_image(pixel_data, key):
    key = ''.join(map(str, key))
    for pixel in pixel_data:
        pixel[0] = bin(int(pixel[0],2) ^ int(key,2))[2:]
        pixel[1] = bin(int(pixel[1],2) ^ int(key,2))[2:]
        pixel[2] = bin(int(pixel[2],2) ^ int(key,2))[2:]
    return(pixel_data)
#Создание файла по пикселям.
def create_image_from_pixels(pixel_data, width, height, file_path):
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_data[y * width + x]
            pixels[x,  y] = (int(r, 2), int(g, 2), int(b, 2))
    img.save(file_path)
    return 1


if __name__ == "__main__":
    # initial_state = input("Введите начальное значение сдвигового регистра в виде строки битов: ")
    test = '101011'
    # feedback_polynomial = input("Введите образующий многочлен в виде строки битов: ")
    test2='1001001011'
    # lfsr = GaloisLFSR(initial_state, feedback_polynomial)
    lfsr=GaloisLFSR(test,test2)
    sequence_length = 127
    generated_sequence = lfsr.generate_sequence(sequence_length)
    interval_length = 10
    expected_count = sequence_length // interval_length // 2 
    intervals = [generated_sequence[i:i + interval_length] for i in range(0, len(generated_sequence), interval_length)]
    observed_counts = [sum(interval) for interval in intervals]
    expected_counts = [expected_count] * len(intervals)
    # Вычисление критерия χ2
    chi_square_statistic = chi_square_test(observed_counts, expected_counts)
    print("Результаты оценки последовательности критерием χ^2 = " + str(chi_square_statistic))
    # Визуализация точечной диаграммы
    plt.figure(figsize=(10, 6))
    plt.scatter(range(sequence_length), generated_sequence, color='b')
    plt.title('Результаты генерации последовательности битов')
    plt.xlabel('Порядковый номер бита')
    plt.ylabel('Значение бита')
    plt.show()
    p_data= read_bmp_pixels_rgb("tux.png")
    key = lfsr.generate_sequence(8)
    create_image_from_pixels(encode_image(p_data,key),width,height,file_path)