import numpy as np
from scipy.misc import derivative
import matplotlib.pyplot as plt
from gauss import GaussMethod

from PointClass import Point


class DiffEqu:
    """
    Класс для нахождения приближенного решения дифференциального
    уравнения второго порядка методом наименьших квадратов
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """
        # имеется уравнение y" + x * y' + y = 2 * x
        # y(0) = 1, y(1) = 0
        # решение ищется в виде, определенном в тз
        # в качестве базисных функций я взял функции вида x^k * (1 - x), где k = 0,...,m

        # для дискретного варианта метода наименьших квадратов необходимо, чтобы
        #  неизвестные коэффициенты c1,...,cm
        #  должны обеспечивать минимум суммы квадратов значений невязки в заданном наборе точек x1,...,xn; n>=m
        # , то есть xi принадлежит (a,b), i=1,...,n:
        # в моем уравнении a = 0, b = 1
        # создадим набор из n точек из диапазона (a, b)
        self.n = 20
        self.x_n = list(np.linspace(0, 1, self.n))

        self.approx_points_m_eq_2: list = list()
        self.approx_points_m_eq_3: list = list()
        self.approx_points_m_eq_m: list = list()

        # зададим переменную m, которая будет отвечать за число базисных функций,
        # начиная с 1 до m
        self.m = 2  # оно же число строк в системе

    @staticmethod
    def __input_m() -> int:
        """
        Метод позволяет пользователю ввести степень аппроксимации,
        тобишь какой функцией будем аппроксимировать
        """

        return int(input("Введите m: "))

    @staticmethod
    def u_0(x: int | float) -> int | float:
        """
        Функция u0
        """

        return 1 - x

    @staticmethod
    def f(x):
        """
        Правая часть дифференциального уравнения второго порядка из тз в общем виде
        """

        return 2 * x

    def f_minus_lu_0(self, x):
        """
        Для правой части системы уравнений
        """
        res = self.f(x) - self.lin_operator(self.u_0)(x)

        return res

    @staticmethod
    def lin_operator(u):
        """
        Пробую сделать линейный оператор через замыкание
        """

        def lu(x):
            """
            Действие линейного оператора
            """
            y__ = derivative(u, x, n=2, dx=1e-6)
            y_ = derivative(u, x, n=1, dx=1e-7)
            y = u(x)

            result = y__ + x * y_ + y

            return result

        return lu

    def __get_matrix_slau(self) -> list[list[float]]:
        """
        Метод получает матрицу СЛАУ дифференциального уравнения
        """
        # m + 1, потому что еще столбец решений
        matrix_slau = [[0.0 for _ in range(self.m + 1)] for _ in range(self.m)]

        for i in range(self.m):
            def u_i(x):  # та, что меняется по строкам
                return (x ** (i + 1)) * (1 - x)

            lu_i = self.lin_operator(u_i)  # ее линейный оператор

            for j in range(self.m):
                def u_j(x):  # та, что меняется по столбцам
                    return (x ** (j + 1)) * (1 - x)

                lu_j = self.lin_operator(u_j)  # ее линейный оператор

                sum_elem = 0
                for x_val in self.x_n:
                    sum_elem += lu_j(x_val) * lu_i(x_val)
                matrix_slau[i][j] = sum_elem

            # сумма по всем точкам при фиксированном i
            # считали правую часть системы
            sum_elem = 0
            for x_val in self.x_n:
                sum_elem = self.f_minus_lu_0(x_val) * lu_i(x_val)
            matrix_slau[i][self.m] = sum_elem

        self.__print_matrix_slau(matrix_slau)

        return matrix_slau

    def __get_approx_func(self, m: int):
        """
        Метод позволяет получить решение,
        используя метод наименьших квадратов
        """
        self.m = m

        matrix_slau = self.__get_matrix_slau()

        gauss_method = GaussMethod(matrix_slau)
        c_k = gauss_method.gauss()

        self.__print_c_k(c_k)

        def closure_approx_func(x):
            """
            Функция-замыкание аппроксимирующей заданной функцией
            """
            y = self.u_0(x)

            for i in range(len(c_k)):
                y += c_k[i] * (x ** (i + 1)) * (1 - x)

            return y

        return closure_approx_func

    def __approximation(self) -> int:
        """
        Метод для аппроксимации таблично заданной функции
        """

        # почистим если уже ранее делали
        self.approx_points_m_eq_2.clear()
        self.approx_points_m_eq_3.clear()
        self.approx_points_m_eq_m.clear()

        func_approx_m_eq_2 = self.__get_approx_func(2)
        func_approx_m_eq_3 = self.__get_approx_func(3)

        m = self.__input_m()
        func_approx_m_eq_m = self.__get_approx_func(m)

        x_min, x_max = self.x_n[0], self.x_n[-1]
        x_values = np.linspace(x_min, x_max)

        for x in x_values:
            new_point_m2 = Point(x=x, y=func_approx_m_eq_2(x))
            new_point_m3 = Point(x=x, y=func_approx_m_eq_3(x))
            new_point_m = Point(x=x, y=func_approx_m_eq_m(x))

            self.approx_points_m_eq_2.append(new_point_m2)
            self.approx_points_m_eq_3.append(new_point_m3)
            self.approx_points_m_eq_m.append(new_point_m)

        return m

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
        m = self.__approximation()

        plt.figure("Дифференциальное уравнение")
        plt.title("График решения дифф-го уравнения при различных m")
        plt.xlabel("X")
        plt.ylabel("Y")

        x_values, y_values = self.__convert_for_two_arr(self.approx_points_m_eq_2)
        plt.plot(x_values, y_values, ls='--', color='b', label=f"m = 2")

        x_values, y_values = self.__convert_for_two_arr(self.approx_points_m_eq_3)
        plt.plot(x_values, y_values, ls='-.', color='g', label=f"m = 3")

        x_values, y_values = self.__convert_for_two_arr(self.approx_points_m_eq_m)
        plt.plot(x_values, y_values, ls='-', color='r', label=f"m = {m}")

        plt.legend()
        plt.show()

    @staticmethod
    def __print_c_k(c_k: list[float]) -> None:
        """
        Функция выводит посчитанные коэффициенты
        """
        print("Посчитанные результирующие коэффициенты:")

        for i in range(len(c_k)):
            print("c" + str(i + 1) + " = {:<10.6g}".format(c_k[i]))

    @staticmethod
    def __print_matrix_slau(matrix_slau) -> None:
        """
        Функция выводит матрицу СЛАУ на экран в консоли
        """
        print("Матрица СЛАУ (дифференциальное уравнение):")

        for i in range(len(matrix_slau)):
            for j in range(len(matrix_slau[0])):
                print(f"{matrix_slau[i][j]:^10.3f}", end=" ")
            print("\n")
