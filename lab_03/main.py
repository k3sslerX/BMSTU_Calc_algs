from newton import NewtonInterpolation
from cubicspline import CubicSplineInterpolation


class App:
    """Модель программы для лабораторной работы №3"""
    file_name = "files/file1.txt"  # Файл с данными

    list_matrices = list()  # Список матриц из файла с данными

    list_x = list(range(0, 5))
    list_y = list(range(0, 5))
    list_z = list(range(0, 5))

    argument_x = 0  # Аргумент x для которого выполняется Интерполяция.
    argument_y = 0  # Аргумент y для которого выполняется Интерполяция.
    argument_z = 0  # Аргумент z для которого выполняется Интерполяция.

    polyn_degree_x = 2  # Степень x аппроксимирующего полинома (при использовании полинома Ньютона).
    polyn_degree_y = 2  # Степень y аппроксимирующего полинома (при использовании полинома Ньютона).
    polyn_degree_z = 2  # Степень z аппроксимирующего полинома (при использовании полинома Ньютона).

    boundary_conditions = (0, 0)  # Краевые условия для кубического сплайна.

    def work(self):
        self._readDataFromFile()

        print("Выберите способ интерполяции:")
        print("1 - Полином Ньютона")
        print("2 - Кубический сплайн")
        print("3 - Смешанная")

        number = self._inputMenuNumber()

        self._inputArgumetX()
        self._inputArgumetY()
        self._inputArgumetZ()

        if number == 1:
            self._inputPolynDegreeX()
            self._inputPolynDegreeY()
            self._inputPolynDegreeZ()

            value = self._multidimensionalNewtonInterpolation()
        elif number == 2:
            value = self._multidimensionalCubicSplineInterpolation()
        else:
            self._inputPolynDegreeY()

            value = self._multidimensionalMixInterpolation()

        print(f"Результат интерполяции - {value}")

    def _inputMenuNumber(self) -> int:
        number = int(input("Способ интерполяции - "))

        return number

    def _setArgumentX(self, x: float):
        """Устанавливает значение аргумента x для которого выполняется Интерполяция."""
        self.argument_x = x

    def _setArgumentY(self, y: float):
        """Устанавливает значение аргумента y для которого выполняется Интерполяция."""
        self.argument_y = y

    def _setArgumentZ(self, z: float):
        """Устанавливает значение аргумента z для которого выполняется Интерполяция."""
        self.argument_z = z

    def _setPolynDegreeX(self, x: int):
        """Устанавливает значение степени x аппроксимирующего полинома."""
        self.polyn_degree_x = x

    def _setPolynDegreeY(self, y: int):
        """Устанавливает значение степени y аппроксимирующего полинома."""
        self.polyn_degree_y = y

    def _setPolynDegreeZ(self, z: int):
        """Устанавливает значение степени z аппроксимирующего полинома."""
        self.polyn_degree_z = z

    def _inputArgumetX(self):
        """Считывает значения аргумента x для которого выполняется Интерполяция."""
        x = float(input("Введите аргумент x - "))
        self._setArgumentX(x)

    def _inputArgumetY(self):
        """Считывает значения аргумента y для которого выполняется Интерполяция."""
        y = float(input("Введите аргумент y - "))
        self._setArgumentY(y)

    def _inputArgumetZ(self):
        """Считывает значения аргумента z для которого выполняется Интерполяция."""
        z = float(input("Введите аргумент z - "))
        self._setArgumentZ(z)

    def _inputPolynDegreeX(self):
        """Считывает значение степени x для аппроксимирующего полинома."""
        x_degree = int(input("Введите степень x для аппроксимирующего полинома - "))
        self._setPolynDegreeX(x_degree)

    def _inputPolynDegreeY(self):
        """Считывает значение степени y для аппроксимирующего полинома."""
        y_degree = int(input("Введите степень y для аппроксимирующего полинома - "))
        self._setPolynDegreeY(y_degree)

    def _inputPolynDegreeZ(self):
        """Считывает значение степени z для аппроксимирующего полинома."""
        z_degree = int(input("Введите степень z для аппроксимирующего полинома - "))
        self._setPolynDegreeZ(z_degree)

    def _readDataFromFile(self):
        """Чтение данных из файла."""
        with open(self.file_name, "r") as file:
            matrix = list()
            i = 1

            for line in file:
                list_values = list(map(float, line.split()))
                matrix.append(list_values)

                if i % 5 == 0:
                    self.list_matrices.append(matrix.copy())
                    matrix.clear()

                i += 1

    def _createListPoint(self, list1: list, list2: list) -> list:
        """Формирует список узлов и их значений."""
        list_points = list()
        for i in range(len(list1)):
            list_points.append((list1[i], list2[i]))

        return list_points

    def _newtonInterpolation(self, polyn_degree: int, argument: float, list_points: list):
        """Интерполяция с помощью полинома Ньютона."""
        newton_polyn = NewtonInterpolation(polyn_degree, argument, list_points)
        newton_polyn.interpolate()

        return newton_polyn.value_y

    def _multidimensionalNewtonInterpolation(self) -> float:
        """Многомерная интерполяция полиномом Ньютона."""
        list_final_values = list()

        for matrix in self.list_matrices:
            list_values = list()

            for string in matrix:
                list_points = self._createListPoint(self.list_x, string)
                value = self._newtonInterpolation(self.polyn_degree_x, self.argument_x, list_points)
                list_values.append(value)

            list_points = self._createListPoint(self.list_y, list_values)
            value = self._newtonInterpolation(self.polyn_degree_y, self.argument_y, list_points)
            list_final_values.append(value)

        list_points = self._createListPoint(self.list_z, list_final_values)
        value = self._newtonInterpolation(self.polyn_degree_z, self.argument_z, list_points)

        return value

    def _cubicSplineInterpolation(self, argument: float, list_points: list, boundary_conditions: tuple):
        """Интерполяция с помощью кубического сплайна."""
        cubic_spline = CubicSplineInterpolation(argument, list_points, boundary_conditions)
        cubic_spline.interpolate()

        return cubic_spline.value_y

    def _multidimensionalCubicSplineInterpolation(self):
        """Многомерная интерполяция с помощью кубического сплайна."""
        list_final_values = list()

        for matrix in self.list_matrices:
            list_values = list()

            for string in matrix:
                list_points = self._createListPoint(self.list_x, string)
                value = self._cubicSplineInterpolation(self.argument_x, list_points, self.boundary_conditions)
                list_values.append(value)

            list_points = self._createListPoint(self.list_y, list_values)
            value = self._cubicSplineInterpolation(self.argument_y, list_points, self.boundary_conditions)
            list_final_values.append(value)

        list_points = self._createListPoint(self.list_z, list_final_values)
        value = self._cubicSplineInterpolation(self.argument_z, list_points, self.boundary_conditions)

        return value

    def _multidimensionalMixInterpolation(self):
        """Многомерная смешанная интерполяция."""
        list_final_values = list()

        for matrix in self.list_matrices:
            list_values = list()

            for string in matrix:
                list_points = self._createListPoint(self.list_x, string)
                value = self._cubicSplineInterpolation(self.argument_x, list_points, self.boundary_conditions)
                list_values.append(value)

            list_points = self._createListPoint(self.list_y, list_values)
            value = self._newtonInterpolation(self.polyn_degree_y, self.argument_y, list_points)
            list_final_values.append(value)

        list_points = self._createListPoint(self.list_z, list_final_values)
        value = self._cubicSplineInterpolation(self.argument_z, list_points, self.boundary_conditions)

        return value


if __name__ == "__main__":
    app = App()
    app.work()
