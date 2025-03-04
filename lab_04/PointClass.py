class Point:
    """
    Точка
    """

    def __init__(
            self,
            x: int | float,
            y: int | float,
            p: float = 1,
            z: int | float = 0,
            color: str = 'red',
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.x: int | float = x
        self.y: int | float = y
        self.z: int | float = z
        self.color: str = color
        self.p = p

    def __eq__(self, other: 'Point') -> bool:
        """
        Проверка на равенство точек
        """
        is_eq = \
            self.x == other.x and self.y == other.y and \
            self.z == other.z and self.color == self.color

        return is_eq

    def __str__(self) -> str:
        """
        Вывод информации о точке в виде строки
        """
        return f"Point({self.x}, {self.y}, {self.y} {self.color})"

    def set_x(self, x_value: int | float) -> None:
        """
        Метод позволяет изменить значение абсциссы
        """
        self.x = x_value

    def set_y(self, y_value: int | float) -> None:
        """
        Метод позволяет изменить значение ординаты
        """
        self.y = y_value

    def set_z(self, z_value: int | float) -> None:
        """
        Метод позволяет изменить значение аппликаты
        """
        self.z = z_value

    def set_color(self, color: str) -> None:
        """
        Изменение цвета точки
        """
        self.color = color

    def get_x(self) -> int | float:
        """
        Метод позволяет получить значение абсциссы
        """

        return self.x

    def get_y(self) -> int | float:
        """
        Метод позволяет получить значение ординаты
        """

        return self.y

    def get_z(self) -> int | float:
        """
        Метод позволяет получить значение аппликаты
        """

        return self.z

    def get_color(self) -> str:
        """
        Изменение цвета точки
        """

        return self.color

    def distance_to(self, other: 'Point') -> float:
        """
        Вычисление расстояния между двумя точками
        """
        dx = self.x - other.x
        dy = self.y - other.y

        return ((dx ** 2) + (dy ** 2)) ** 0.5

    def move(self, dx: int | float, dy: int | float) -> None:
        """
        Смещение точки на заданное расстояние по осям x и y
        """
        self.x += dx
        self.y += dy

    def info(self) -> None:
        """
        Вывод координат точки и ее цвета
        """
        print(f"Координаты: ({self.x}, {self.y}, {self.z})",
              f"Цвет: {self.color}", sep='\n')
