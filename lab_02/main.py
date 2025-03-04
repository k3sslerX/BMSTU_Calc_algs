from newton import NewtonInterpolation
from cubicspline import CubicSplineInterpolation


class App:
    file_name = "files/data.txt"
    list_points = list()
    argument_x = None

    def work(self):
        self._fillListPointsWithDataFromFile()

        self._outputUserMenu()
        number_menu = self._inputMenuNumber()

        while number_menu != 4:
            if number_menu == 0:
                self._outputListPointInTableForm()
            elif number_menu < 4:
                self._inputArgumetX()

                if number_menu == 1:
                    cubicspline = CubicSplineInterpolation(self.argument_x, self.list_points, (0, 0))
                elif number_menu == 2:
                    polynomial = NewtonInterpolation(3, self.argument_x, self.list_points)
                    polynomial.interpolate()
                    two_der1 = polynomial.twoDerivativeThirdPolynomialDegree(self.list_points[0][0])

                    cubicspline = CubicSplineInterpolation(self.argument_x, self.list_points, (two_der1, 0))
                else:
                    polynomial = NewtonInterpolation(3, self.argument_x, self.list_points)
                    polynomial.interpolate()
                    two_der1 = polynomial.twoDerivativeThirdPolynomialDegree(self.list_points[0][0])
                    two_der2 = polynomial.twoDerivativeThirdPolynomialDegree(self.list_points[-1][0])

                    print(two_der1, two_der2)

                    cubicspline = CubicSplineInterpolation(self.argument_x, self.list_points, (two_der1, two_der2))

                cubicspline.interpolate()
                print(f"--------\ny = {cubicspline.value_y}\n--------")
            elif number_menu == 4:
                break

            self._outputUserMenu()
            number_menu = self._inputMenuNumber()

    def _fillListPointsWithDataFromFile(self):
        with open(self.file_name, "r") as file:
            for line in file:
                point = tuple(map(float, line.split()))
                self.list_points.append(point)

    def _outputListPointInTableForm(self):
        print("-" * 33)
        print("|   №   |     X     |     Y     |")
        print("-" * 33)

        for i in range(len(self.list_points)):
            x, y = self.list_points[i]

            print(f"| {i}", " " * (4 - len(str(i))), "| ", end="")
            print(f"{format(x, '.3f')}", end="")
            print("     | ", end="")
            print(f"{format(y, '.3f')}", end="")
            print("     |")

        print("-" * 33, "\n")


    def _outputUserMenu(self):
        print("0 - Вывести таблицу с данными.")
        print("1 - 1-ый вариант интерполяции (x0 = 0, xn = 0).")
        print("2 - 2-ый вариант интерполяции (x0 = p\", xn = 0).")
        print("3 - 3-ый вариант интерполяции (x0 = p\", xn = p\").")
        print("4 - Выход.")
        print("Введите действие: ")

    def _setArgumentX(self, x: float):
        self.argument_x = x

    def _inputArgumetX(self):
        x = float(input("Введите аргумент x - "))
        self._setArgumentX(x)

    def _inputMenuNumber(self) -> int:
        number = int(input())

        return number


if __name__ == "__main__":
    app = App()
    app.work()
