import matplotlib.pyplot as plt

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_points(a, b, p):
    points = []
    for x in range(p):
        for y in range(p):
            if (y**2) % p == (x**3 + a * x + b) % p:
                points.append((x, y))
    return points

def plot_points(points):
    x, y = zip(*points)
    plt.scatter(x, y, color='b')
    plt.show()


def add_points(p1, p2, a, p):
    x1, y1 = p1
    x2, y2 = p2

    if p1 == p2:
        m = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return x3, y3

def double_point(p, a, p1):
    x, y = p1
    m = (3 * x**2 + a) * pow(2 * y, -1, p) % p
    x3 = (m**2 - 2 * x) % p
    y3 = (m * (x - x3) - y) % p
    return x3, y3

p = 17  # простое число
a = 2
b = 2
if is_prime(p):
    points = generate_points(a, b, p)
    print("Сгенерированные точки: ", points)
    plot_points(points)
else:
    print("p не является простым числом.")


p1 = (0, 6)
p2 = (3, 1)
print("Сумма точек p1 и p2:", add_points(p1, p2, a, p))
print("Удвоение точки p1:", double_point(p, a, p1))
