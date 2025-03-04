from approx import ApproxOneVar, ApproxTwoVar
from diff_equ import DiffEqu


class Task:
    """
    Класс для решения поставленной задачи
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """
        self.approx_1var = None
        self.approx_2var = None

        self.diff_equ = DiffEqu()

        self.handler()

    @staticmethod
    def print_menu() -> None:
        """
        Метод выводит меню взаимодействия с программой
        """
        print("1. Сгенерировать таблицу для одномерной аппроксимации;",
              "2. Сгенерировать таблицу для двумерной аппроксимации;",
              "3. Вывести таблицу для одномерной аппроксимации;",
              "4. Вывести таблицу для двумерной аппроксимации;",
              "5. Изменить вес точки в таблице для одномерной аппроксимации;",
              "6. Решить задачу для одномерной аппроксимации и построить график;",
              "7. Решить задачу для двумерной аппроксимации и построить график;",
              "8. Решить дифференциальное уравнение;",
              sep='\n')

    @staticmethod
    def choose_menu_item() -> int:
        """
        Метод для выбора пункта меню
        """

        return int(input("Введите пункт меню: "))

    def gen_table_1var(self) -> None:
        """
        Метод обертка для генерации таблицы функции 1-й переменной
        """
        x_start = float(input("Введите начало интервала x_start: "))
        x_end = float(input("Введите конец интервала x_end: "))
        count_points = int(input("Введите количество точек: "))

        self.approx_1var = ApproxOneVar(
            x_start,
            x_end,
            count_points
        )

        self.approx_1var.gen_table()

    def gen_table_2var(self) -> None:
        """
        Метод обертка для генерации таблицы функции 1-й переменной
        """
        x_start = float(input("Введите начало интервала x_start: "))
        x_end = float(input("Введите конец интервала x_end: "))
        count_x = int(input("Введите количество точек count_x: "))

        y_start = float(input("Введите начало интервала y_start: "))
        y_end = float(input("Введите конец интервала y_end: "))
        count_y = int(input("Введите количество точек count_y: "))

        self.approx_2var = ApproxTwoVar(
            x_start,
            x_end,
            y_start,
            y_end,
            count_x,
            count_y
        )

        self.approx_2var.gen_table()

    def print_table_1var(self) -> None:
        """
        Функция выводит таблицу значений для функций 1-й переменной
        """
        if self.approx_1var is None:
            print("Таблица значений еще не получена!")
            return

        self.approx_1var.print_data_table()

    def print_table_2var(self) -> None:
        """
        Функция выводит таблицу значений для функций 1-й переменной
        """
        if self.approx_2var is None:
            print("Таблица значений еще не получена!")
            return

        self.approx_2var.print_data_table()

    def change_p_1var(self) -> None:
        """
        Метод обертка для изменения веса точки в таблице функции
        1-й переменной
        """
        if self.approx_1var is None:
            print("Таблица значений еще не получена!")
            return

        self.approx_1var.change_p()

    def approximation_1var(self) -> None:
        """
        Метод обертка для решения задачи аппроксимации
        функции 1-й переменной
        """
        if self.approx_1var is None:
            print("Таблица значений еще не получена!")
            return

        self.approx_1var.approx_and_plot()

    def approximation_2var(self) -> None:
        """
        Метод обертка для решения задачи аппроксимации
        функции 2-х переменных
        """
        if self.approx_2var is None:
            print("Таблица значений еще не получена!")
            return

        self.approx_2var.approx_and_plot()

    def get_solve_diff_equ(self) -> None:
        """
        Метод позволяет получить решение
        дифференциального уравнения
        """
        self.diff_equ.approx_and_plot()

    def handler(self) -> None:
        """
        Метод для обработки действий пользователя
        """

        while True:

            self.print_menu()
            menu_item = self.choose_menu_item()

            match menu_item:
                case 1:
                    self.gen_table_1var()
                case 2:
                    self.gen_table_2var()
                case 3:
                    self.print_table_1var()
                case 4:
                    self.print_table_2var()
                case 5:
                    self.change_p_1var()
                case 6:
                    self.approximation_1var()
                case 7:
                    self.approximation_2var()
                case 8:
                    self.get_solve_diff_equ()
                case _:
                    print("Неверный пункт меню!")
                    return
