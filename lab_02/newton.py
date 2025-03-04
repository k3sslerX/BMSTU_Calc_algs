class NewtonInterpolation():

    def __init__(self, polynomial_degree: int, argument_x: float, list_points: list):
        self.polynomial_degree = polynomial_degree
        self.argument_x = argument_x
        self.list_points = list_points[:]

        self.start_index = 0
        self.polynomial_value = 0

        self.list_div_diff = list()

    def interpolate(self):
        self.start_index = self._configurationSet()

        self._listDividedDiffInput()

        self.polynomial_value = self._polynomialValue()

    def _configurationSet(self) -> int:
        i = 0

        while self.list_points[i][0] < self.argument_x:
            i += 1

        start_index = i - (self.polynomial_degree + 1) // 2  # Вычисление индекса начала сегмента конфигурации.
        if start_index < 0:
            start_index = 0
        if start_index + (self.polynomial_degree + 1) >= len(self.list_points):
            start_index -= (start_index + (self.polynomial_degree + 1) - len(self.list_points))

        return start_index

    def _dividedDiff(self, point1: tuple, point2: tuple) -> float:
        div_diff = (point1[1] - point2[1]) / (point1[0] - point2[0])

        return div_diff

    def _listDividedDiffInput(self):
        for i in range(self.polynomial_degree + 1):
            self.list_div_diff.append([self.list_points[i + self.start_index][1]])

        for i in range(1, self.polynomial_degree + 1):
            for j in range(self.polynomial_degree + 1 - i):
                point1 = (self.list_points[j + self.start_index][0], self.list_div_diff[j][i - 1])
                point2 = (self.list_points[i + j + self.start_index][0], self.list_div_diff[j + 1][i - 1])

                div_diff = self._dividedDiff(point1, point2)

                self.list_div_diff[j].append(div_diff)

    def _polynomialValue(self) -> float:
        polynomial_value = 0.0

        for i in range(self.polynomial_degree + 1):
            monomial_value = self.list_div_diff[0][i]

            for j in range(i):
                monomial_value *= self.argument_x - self.list_points[j + self.start_index][0]

            polynomial_value += monomial_value

        return polynomial_value

    def twoDerivativeThirdPolynomialDegree(self, argument_x: float) -> float:
        two_derivative = (2 * self.list_div_diff[0][2] + 6 * self.list_div_diff[0][3] * argument_x -
                          2 * self.list_div_diff[0][3] * self.list_points[self.start_index + 2][0] -
                          2 * self.list_div_diff[0][3] * self.list_points[self.start_index + 1][0] -
                          2 * self.list_div_diff[0][3] * self.list_points[self.start_index + 1][0])

        return two_derivative


if __name__ == "__main__":
    polynomial_degree = 3
    argument_x = 3.3

    list_points = list()
    with open("files/file1.txt", 'r') as file:
        for line in file:
            point = tuple(map(float, line.split()))
            list_points.append(point)

    polynomial = NewtonInterpolation(polynomial_degree, argument_x, list_points)
    polynomial.interpolate()
    print(polynomial.polynomial_value)
