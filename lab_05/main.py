import numpy as np
import matplotlib.pyplot as plt
from MathMethod import *
from numpy import linspace, exp, sqrt
from math import pi
import plotly.express as px


# import plotly.express as px

def gaussElim(a, b):
    n = len(b)
    for k in range(0, n - 1):
        for i in range(k + 1, n):
            if a[i, k] != 0.0:
                lam = a[i, k] / a[k, k]
                a[i, k + 1:n] = a[i, k + 1:n] - lam * a[k, k + 1:n]
                b[i] = b[i] - lam * b[k]
    for k in range(n - 1, -1, -1):
        b[k] = (b[k] - np.dot(a[k, k + 1:n], b[k + 1:n])) / a[k, k]

    return b


def system_solution(x_start, eps=1e-4):
    x = x_start[0]  # count step s = 1
    y = x_start[1]
    z = x_start[2]

    matrix = np.array(
        [
            [2 * x, 2 * y, 2 * z],
            [4 * x, 2 * y, -4],
            [6 * x, -4, 2 * z]
        ]
    )

    b = np.array(
        [
            1 - (x ** 2 + y ** 2 + z ** 2),
            4 * z - y ** 2 - 2 * x ** 2,
            4 * y - 3 * x ** 2 - z ** 2
        ]
    )

    delt_x, delt_y, delt_z = gaussElim(matrix, b)

    cur_x = x + delt_x  # values on s step
    cur_y = y + delt_y
    cur_z = z + delt_z

    x = cur_x
    y = cur_y
    z = cur_z

    while (abs(max([delt_x / cur_x, delt_y / cur_y, delt_z / cur_z])) >= eps):
        matrix = np.array([
            [2 * x, 2 * y, 2 * z],
            [4 * x, 2 * y, -4],
            [6 * x, -4, 2 * z]
        ])

        b = np.array([
            1 - (x ** 2 + y ** 2 + z ** 2),
            4 * z - y ** 2 - 2 * x ** 2,
            4 * y - 3 * x ** 2 - z ** 2
        ])

        delt_x, delt_y, delt_z = gaussElim(matrix, b)

        cur_x = x + delt_x
        cur_y = y + delt_y
        cur_z = z + delt_z

        x = cur_x
        y = cur_y
        z = cur_z

    return (cur_x, cur_y, cur_z)


def func(x):
    return 2 / np.sqrt(2 * np.pi) * np.exp(-x ** 2 / 2)


def count_integral(x, n=1000):
    N = 2 * n
    steps = [x / N * i for i in range(N + 1)]

    h = x / N

    s1 = 2 * np.sum([func(steps[2 * j]) for j in range(1, N // 2)])
    s2 = 4 * np.sum([func(steps[2 * j - 1]) for j in range(1, N // 2 + 1)])

    return h / 3 * (func(steps[0]) + s1 + s2 + func(steps[N]))


def find_root(fx, eps=1e-6):
    # bisection
    # 0 - fx

    def f(x):
        return fx - count_integral(x)

    left_bound = 0
    right_bound = 5

    if f(left_bound) == 0:
        return left_bound

    if f(right_bound) == 0:
        return right_bound

    if f(right_bound) < f(left_bound):
        left_bound, right_bound = right_bound, left_bound

    x = left_bound + (right_bound - left_bound) / 2

    while abs((right_bound - left_bound)) > eps * x + eps / 2:

        x = (left_bound + right_bound) / 2
        if (np.sign(f(left_bound)) != np.sign(f(x))):
            right_bound = x
        else:
            left_bound = x

    return x


def der_equation_solution(n=100):
    # Краевые условия
    x0 = 0
    y0 = 1
    x1 = 1
    y1 = 3

    # Количество отрезков и шаг по x
    N = 100
    step = (x1 - x0) / (N)

    # Массив x
    x = linspace(x0, x1, N + 1)

    # Функция генерации якобиана для уравнения y'' - y^3 = x^2, при замене второй производной по разностной схеме для всех точек x
    # y - Массив текущих приближённых значений
    def jacobian(*y):
        N = len(y)
        res = []
        res.append([1] + [0] * (N - 1))
        for i in range(1, N - 1):
            res.append([0] * (i - 1) + [1 / step ** 2] + [-2 / step ** 2 - 3 * y[i] ** 2] + [1 / step ** 2] + [0] * (
                        N - i - 2))
        res.append([0] * (N - 1) + [1])
        return res

    # Функция для генерации n - ой функции в системе нелинейных уравнений при разложении по разностной схеме.
    def f(n):
        if n == 0:
            def resf(*y):
                return y[0] - y0
        elif n == N:
            def resf(*y):
                return y[n] - y1
        else:
            def resf(*y):
                return (y[n - 1] + -2 * y[n] + y[n + 1]) / step ** 2 - y[n] ** 3 - x[n] ** 2
        return resf

    funcs = [f(i) for i in range(N + 1)]

    def starty(x):
        return 2 * x + 1  # Удовлетворяет краевым условиям

    # Начальное приближение y
    y = [starty(xp) for xp in x]

    # res - Найденное методом ньютона значение
    res, iters = NewtonSystem(jacobian, funcs, y, maxIter=30, epsilon=1e-9)
    print(f"Начальное приближение y[-2]: {y[-2]}")
    print(f"Найденный y[-2]: {res[-2]}")  # Значение функции в предпоследней точке
    print(f"Число итераций: {iters}")
    fig = px.line(x=x, y=res)

    fig.show()


def main():
    print("Решения системы: ")
    print("Корень №1: ", tuple(
        map(lambda x: round(x, 6), system_solution(x_start=[+1, 0.1, 0.1]))))
    print("Корень №2: ", tuple(
        map(lambda x: round(x, 6), system_solution(x_start=[-1, 0.1, 0.1]))))

    fx = float(input("Введите данное значение функции: "))
    assert (fx < 1 and fx > -1)
    print("Значение х для интеграла: ", find_root(fx))

    # x = np.linspace(-20, 20, 100)
    # y = [count_integral(i) for i in x]

    # plt.plot(x, y)
    # plt.grid(True)
    # plt.show()

    der_equation_solution()


if __name__ == "__main__":
    main()
