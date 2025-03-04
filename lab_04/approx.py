import numpy as np
from random import randint
import matplotlib.pyplot as plt
from typing import Callable

from PointClass import Point
from gauss import GaussMethod


class ApproxOneVar:
    """
    Класс функции от 1-й переменной и ее аппроксимации
    """
    SIZE_TABLE_VALUE = 66

    def __init__(
            self,
            x_start: int | float,
            x_end: int | float,
            count_points: int
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.x_start: int | float = x_start
        self.x_end: int | float = x_end
        self.count_points: int = count_points
        self.n: int = 0  # степень полинома
        self.h: int = 1  # число уравнений в СЛАУ
        self.data_table: list[Point] = []

        # по тз надо обязательно строить аппроксимацию при n = 1 и n = 2
        self.approx_n_eq_1: list[Point] = []
        self.approx_n_eq_2: list[Point] = []

        # по тз надо еще по введенной пользователем n строить аппроксимацию
        self.approx_n_eq_n: list[Point] = []
        self.approx_n_eq_n_p_mode: list[Point] = []

    def gen_table(self) -> list[Point]:
        """
        Метод позволяет сгенерировать таблицу точек
        функции от 1-й переменной
        """

        # если уже генерировали, то надо очистить
        self.data_table.clear()

        x_values = np.linspace(self.x_start, self.x_end, self.count_points)

        for x in x_values:
            point = Point(x=x, y=self.__func(x), p=randint(1, 5))
            self.data_table.append(point)

        return self.data_table

    def change_p(self) -> None:
        """
        Метод позволяет изменить вес точки
        """
        self.print_data_table()

        num_point = int(input("Введите номер точки: "))
        new_p = int(input("Введите новый вес для точки: "))

        self.data_table[num_point - 1].p = new_p

    @staticmethod
    def __func(x: int | float) -> int | float:
        """
        Функция от 1-й переменной
        """

        return x ** 2

    @staticmethod
    def __input_n() -> int:
        """
        Метод позволяет пользователю ввести степень аппроксимации,
        тобишь какой функцией будем аппроксимировать
        """

        return int(input("Введите степень аппроксимации: "))

    def __get_matrix_slau(self, p_mode: bool = False) -> list[list[float]]:
        """
        Метод позволяет получить матрицу СЛАУ
        """
        matrix_slau = [[0.0 for _ in range(self.h + 1)] for _ in range(self.h)]

        for k in range(self.h):
            for m in range(self.h):
                # сумма по всем точкам при фиксированном k
                # и изменяющемся при нем m
                # считали левую часть системы
                sum_s = 0
                for point in self.data_table:
                    p = point.p if not p_mode else 1
                    sum_s += p * point.x ** (k + m)
                matrix_slau[k][m] = sum_s

            # сумма по всем точкам при фиксированном k
            # считали правую часть системы
            sum_s = 0
            for point in self.data_table:
                p = point.p if not p_mode else 1
                sum_s += p * point.y * point.x ** k
            matrix_slau[k][self.h] = sum_s

        self.__print_matrix_slau(matrix_slau)

        return matrix_slau

    @staticmethod
    def __print_matrix_slau(matrix_slau) -> None:
        """
        Функция выводит матрицу СЛАУ на экран в консоли
        """
        print("Матрица СЛАУ (аппроксимация функции от 1-й переменной):")

        for i in range(len(matrix_slau)):
            for j in range(len(matrix_slau[0])):
                print(f"{matrix_slau[i][j]:^10.3f}", end=" ")
            print("\n")

    @staticmethod
    def __print_a_k(a_k: list[float]) -> None:
        """
        Функция выводит посчитанные коэффициенты
        """
        print("Посчитанные результирующие коэффициенты:")

        for i in range(len(a_k)):
            print("a" + str(i) + " = {:<10.6g}".format(a_k[i]))

    def __get_approx_func(self, n: int, p_mode: bool = False):
        """
        Метод позволяет получить функцию аппроксимации
        n - степень полинома (аппроксимации)
        """
        self.n = n

        # у полинома n-й степени n + 1 уравнений в системе
        self.h = self.n + 1

        matrix_slau = self.__get_matrix_slau(p_mode=p_mode)

        # решили систему методом гаусса, получили значения коэффиц. а_k
        gauss_method = GaussMethod(matrix_slau)
        a_k = gauss_method.gauss()

        self.__print_a_k(a_k)

        def closure_approx_func(x):
            """
            Функция-замыкание аппроксимирующей заданной функцией
            """
            y = 0

            for i in range(len(a_k)):
                y += a_k[i] * x ** i

            return y

        return closure_approx_func

    def __approximation(self) -> int:
        """
        Метод для аппроксимации таблично заданной функции
        """

        # почистим если уже ранее делали
        self.approx_n_eq_1.clear()
        self.approx_n_eq_2.clear()
        self.approx_n_eq_n.clear()

        # по тз надо отобразить
        func_approx_n_eq_1 = self.__get_approx_func(1, p_mode=True)
        func_approx_n_eq_2 = self.__get_approx_func(2, p_mode=True)

        # по введенному пользователем надо отобразить
        n = self.__input_n()
        func_approx_n_eq_n = self.__get_approx_func(n, p_mode=False)
        func_approx_n_eq_n_p_mode = self.__get_approx_func(n, p_mode=True)

        x_min, x_max = self.data_table[0].x, self.data_table[-1].x
        x_values = np.linspace(x_min, x_max)

        for x in x_values:
            new_point1 = Point(x=x, y=func_approx_n_eq_1(x))
            new_point2 = Point(x=x, y=func_approx_n_eq_2(x))
            new_pointn = Point(x=x, y=func_approx_n_eq_n(x))
            new_pointn_p_mode = Point(x=x, y=func_approx_n_eq_n_p_mode(x))

            self.approx_n_eq_1.append(new_point1)
            self.approx_n_eq_2.append(new_point2)
            self.approx_n_eq_n.append(new_pointn)
            self.approx_n_eq_n_p_mode.append(new_pointn_p_mode)

        return n

    @staticmethod
    def __convert_for_two_arr(points: list[Point]):
        """
        Метод разделяет значения x и y в два массива
        """
        x_values = list()
        y_values = list()

        for point in points:
            x_values.append(point.x)
            y_values.append(point.y)

        return x_values, y_values

    def approx_and_plot(self):
        """
        Метод аппроксимирует и строит графики
        """
        n = self.__approximation()

        plt.figure("Аппроксимация")
        plt.title("Аппроксимация функции от 1-й переменной")
        plt.xlabel("X")
        plt.ylabel("Y")

        # отображаем исходные точки
        for point in self.data_table:
            plt.plot(point.x, point.y, marker='x', color='red')

        x_values, y_values = self.__convert_for_two_arr(self.approx_n_eq_1)
        plt.plot(x_values, y_values, ls='--', color='b', label=f"n = 1, p all = 1")

        x_values, y_values = self.__convert_for_two_arr(self.approx_n_eq_2)
        plt.plot(x_values, y_values, ls='-.', color='g', label=f"n = 2, p all = 1")

        x_values, y_values = self.__convert_for_two_arr(self.approx_n_eq_n)
        plt.plot(x_values, y_values, ls='-', color='m', label=f"n = {n}, p свои")

        x_values, y_values = self.__convert_for_two_arr(self.approx_n_eq_n_p_mode)
        plt.plot(x_values, y_values, ls='-', color='k', label=f"n = {n}, p all = 1")

        plt.legend()
        plt.show()

    def print_data_table(self) -> None:
        """
        Функция выводит на экран таблицу значений
        """
        if len(self.data_table) == 0:
            print("Таблица значений еще не была получена!")
            return

        print("|" + self.SIZE_TABLE_VALUE * "-" + "|")
        print(f"|{'№ точки':^12s}|{'x':^18s}|{'y = f(x)':^17s}|{'p':^16s}|")
        print("|" + self.SIZE_TABLE_VALUE * "-" + "|")

        for ind, point in enumerate(self.data_table):
            print("| {:^10d} | {:^16f} | {:^15.7f} | {:^14.7f} |".format(
                ind + 1,
                point.x,
                point.y,
                point.p)
            )

        print("|" + self.SIZE_TABLE_VALUE * "-" + "|")


class ApproxTwoVar:
    """
    Класс функции от 2-й переменной и ее аппроксимации
    """
    SIZE_TABLE_VALUE = 84

    def __init__(
            self,
            x_start: int | float,
            x_end: int | float,
            y_start: int | float,
            y_end: int | float,
            count_x: int,
            count_y: int
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.x_start: int | float = x_start
        self.x_end: int | float = x_end
        self.y_start: int | float = y_start
        self.y_end: int | float = y_end
        self.count_x: int = count_x
        self.count_y: int = count_y

        self.n: int = 0  # степень полинома

        self.data_table: list[Point] = []

        # по тз надо еще по введенной пользователем n строить аппроксимацию
        self.approx_n_eq_n: list = list()

    @staticmethod
    def func(x: int | float, y: int | float) -> int | float:
        """
        Функция от 2-x переменных
        """

        return x ** 2 + y ** 2

    def gen_table(self) -> list[Point]:
        """
        Метод позволяет сгенерировать таблицу точек
        функции от 1-й переменной
        """

        # если уже генерировали, то надо очистить
        self.data_table.clear()

        x_values = np.linspace(self.x_start, self.x_end, self.count_x)
        y_values = np.linspace(self.y_start, self.y_end, self.count_y)

        for x in x_values:
            for y in y_values:
                point = Point(x=x, y=y, z=self.func(x, y), p=randint(1, 10))
                self.data_table.append(point)

        return self.data_table

    @staticmethod
    def __input_n() -> int:
        """
        Метод позволяет пользователю ввести степень аппроксимации,
        тобишь какой функцией будем аппроксимировать
        """

        return int(input("Введите степень аппроксимации: "))

    def __get_matrix_slau(self) -> list[list[float]]:
        """
        Метод позволяет получить матрицу СЛАУ для функции 2-х переменных
        """
        # a - матрица левых частей уравнений в СЛАУ
        # b - матрица правых частей уравнений в СЛАУ
        a, b = list(), list()

        for u in range(self.n + 1):
            for v in range(self.n + 1 - u):
                a_row = list()
                for j in range(self.n + 1):  # включительно до n
                    for k in range(self.n + 1 - j):  # внутр. сумма до n - j
                        sum_elem = 0  # сумма для элемента строки матрицы левых частей
                        for point in self.data_table:
                            sum_elem += point.p * point.x ** (j + u) * point.y ** (k + v)
                        a_row.append(sum_elem)
                a.append(a_row)

                # сумма для правой части
                sum_elem = 0
                for point in self.data_table:
                    sum_elem += point.p * point.z * point.x ** u * point.y ** v
                b.append(sum_elem)

        matrix_slau = list()

        for i in range(len(a)):
            matrix_slau.append(a[i])
            matrix_slau[i].append(b[i])

        self.__print_matrix_slau(matrix_slau)

        return matrix_slau

    def __get_approx_func(self, n: int):
        """
        Метод позволяет получить функцию аппроксимации
        n - степень полинома (аппроксимации)
        """
        self.n = n
        # у двумерного полинома n-й степени (n + 1) * (n + 2) / 2 уравнений в системе

        matrix_slau = self.__get_matrix_slau()

        # решили систему методом гаусса, получили значения коэффиц. а_k
        gauss_method = GaussMethod(matrix_slau)
        a_uv = gauss_method.gauss()

        self.__print_a_uv(a_uv)

        def closure_approx_func(x: int | float, y: int | float) -> int | float:
            """
            Функция-замыкание аппроксимирующей заданной функцией
            """
            z = 0
            count = 0
            for i in range(self.n + 1):
                for j in range(self.n + 1 - i):
                    z += a_uv[count] * x ** i * y ** j
                    count += 1

            return z

        return closure_approx_func

    def __get_interval_x(self) -> (int | float, int | float):
        """
        Метод находит максимальное и минимальное значение абсциссы в таблице
        """
        curr_min = self.data_table[0].x
        curr_max = self.data_table[0].x

        for point in self.data_table:
            x = point.x

            if x > curr_max:
                curr_max = x
            if x < curr_min:
                curr_min = x

        return curr_min, curr_max

    def __get_interval_y(self) -> (int | float, int | float):
        """
        Метод находит максимальное и минимальное значение ординаты в таблице
        """
        curr_min = self.data_table[0].y
        curr_max = self.data_table[0].y

        for point in self.data_table:
            y = point.y

            if y > curr_max:
                curr_max = y
            if y < curr_min:
                curr_min = y

        return curr_min, curr_max

    @staticmethod
    def __make_matrix_grid(
            x_values, y_values,
            approx_func: Callable[[int | float, int | float], int | float]
    ):
        """
        Функция создает двумерную матрицу-сетку
        """
        x_grid, y_grid = np.meshgrid(x_values, y_values)

        # В узлах рассчитываем значение функции
        z_grid = np.zeros((len(y_values), len(x_values)))
        for j in range(len(x_values)):
            for i in range(len(y_values)):
                z_grid[i][j] = approx_func(x_grid[i][j], y_grid[i][j])

        return x_grid, y_grid, z_grid

    @staticmethod
    def __convert_for_three_arr(points: list[Point]):
        """
        Метод разделяет значения x и y в два массива
        """
        x_values = list()
        y_values = list()
        z_values = list()

        for point in points:
            x_values.append(point.x)
            y_values.append(point.y)
            z_values.append(point.z)

        return x_values, y_values, z_values

    def __approximation(self) -> int:
        """
        Метод для аппроксимации таблично заданной функции
        """

        # почистим если уже ранее делали
        self.approx_n_eq_n.clear()

        # по введенному пользователем надо отобразить
        n = self.__input_n()
        func_approx_n_eq_n = self.__get_approx_func(n)

        x_min, x_max = self.__get_interval_x()
        y_min, y_max = self.__get_interval_y()

        x_values = np.linspace(x_min, x_max)
        y_values = np.linspace(y_min, y_max)

        x_grid, y_grid, z_grid = self.__make_matrix_grid(x_values, y_values, func_approx_n_eq_n)

        self.approx_n_eq_n.append(x_grid)
        self.approx_n_eq_n.append(y_grid)
        self.approx_n_eq_n.append(z_grid)

        return n

    def approx_and_plot(self):
        """
        Метод аппроксимирует функцию 2-х переменных и строит графики
        """
        self.__approximation()
        x_points, y_points, z_points = self.__convert_for_three_arr(self.data_table)

        fig = plt.figure("Аппроксимация функции от 2-х переменных")
        axes = fig.add_subplot(projection='3d')

        axes.scatter(x_points, y_points, z_points, c='red')  # отображаем исходные точки
        axes.set_xlabel('OX')
        axes.set_ylabel('OY')
        axes.set_zlabel('OZ')

        x_values, y_values, z_values = self.approx_n_eq_n

        axes.plot_surface(x_values, y_values, z_values)
        plt.show()

    @staticmethod
    def __print_matrix_slau(matrix_slau) -> None:
        """
        Функция выводит матрицу СЛАУ на экран в консоли
        """
        print("Матрица СЛАУ (аппроксимация функции от 2-х переменных):")

        for i in range(len(matrix_slau)):
            for j in range(len(matrix_slau[0])):
                print(f"{matrix_slau[i][j]:^10.3f}", end=" ")
            print("\n")

    @staticmethod
    def __print_a_uv(a_uv: list[float]) -> None:
        """
        Функция выводит посчитанные коэффициенты
        """
        print("Посчитанные результирующие коэффициенты:")

        for i in range(len(a_uv)):
            print("a" + str(i) + " = {:<10.6g}".format(a_uv[i]))

    def print_data_table(self) -> None:
        """
        Функция выводит на экран таблицу значений
        """
        if len(self.data_table) == 0:
            print("Таблица значений еще не была получена!")
            return

        print("|" + self.SIZE_TABLE_VALUE * "-" + "|")
        print(f"|{'№ точки':^12s}|{'x':^18s}|{'y':^17s}|{'z = f(x,y)':^17s}|{'p':^16s}|")
        print("|" + self.SIZE_TABLE_VALUE * "-" + "|")

        for ind, point in enumerate(self.data_table):
            print("| {:^10d} | {:^16f} | {:^15.7f} | {:^15.7f} | {:^14.7f} |".format(
                ind + 1,
                point.x,
                point.y,
                point.z,
                point.p)
            )

        print("|" + self.SIZE_TABLE_VALUE * "-" + "|")
