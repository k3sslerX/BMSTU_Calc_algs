from copy import deepcopy
from math import pow


class CubicSplineInterpolation():

    def __init__(self, argument_x: float, list_points: list, boundary_conditions: tuple):
        self.argument_x = argument_x
        self.list_points = deepcopy(list_points)
        self.conditions1, self.conditions2 = boundary_conditions

        self.index = 0
        self.number_nodes = 0
        self.value_y = 0

        self.list_x = list()
        self.list_y = list()

        self.list_A_components = list()
        self.list_B_components = list()
        self.list_D_components = list()
        self.list_F_components = list()

        self.list_h_variables = list()
        self.list_ksi_variables = list()
        self.list_eta_variables = list()

        self.list_a_coefficients = list()
        self.list_b_coefficients = list()
        self.list_c_coefficients = list()
        self.list_d_coefficients = list()

    def interpolate(self):
        self._listXFill()
        self._listYFill()

        self.index = self._configurationSet()
        self.number_nodes = self._numberNodes()

        self._listHVariablesFill()

        self._listAComponentsFill()
        self._listBComponentsFill()
        self._listDComponentsFill()
        self._listFComponentsFill()

        self._listKsiVariablesFill()
        self._listEtaVariablesFill()

        self._listCCoefficientsFill()
        self._listACoefficientsFill()
        self._listBCoefficientsFill()
        self._listDCoefficientsFill()

        self.value_y = self._yValue()

    def _numberPlots(self) -> int:
        number_plots = len(self.list_points) - 1

        return number_plots

    def _numberNodes(self) -> int:
        number_nodes = len(self.list_x)

        return number_nodes

    def _configurationSet(self) -> int:
        i = 0
        while self.list_points[i][0] < self.argument_x:
            i += 1

        return i

    def _yValue(self):
        a = self.list_a_coefficients[self.index]
        b = self.list_b_coefficients[self.index]
        c = self.list_c_coefficients[self.index]
        d = self.list_d_coefficients[self.index]

        xi = self.list_x[self.index - 1]
        y = a + b * (self.argument_x - xi) + c * pow(self.argument_x - xi, 2) + d * pow(self.argument_x - xi, 3)

        return y

    def _listXFill(self):
        for i in range(len(self.list_points)):
            self.list_x.append(self.list_points[i][0])

    def _listYFill(self):
        for i in range(len(self.list_points)):
            self.list_y.append(self.list_points[i][1])

    def _listHVariablesFill(self):
        self.list_h_variables.append(0)

        for i in range(1, self.number_nodes):
            h = self.list_x[i] - self.list_x[i - 1]

            self.list_h_variables.append(h)

    def _listAComponentsFill(self):
        self.list_A_components.append(0)

        for i in range(1, len(self.list_h_variables)):
            A = self.list_h_variables[i - 1]
            self.list_A_components.append(A)

    def _listBComponentsFill(self):
        self.list_B_components.append(0)
        self.list_B_components.append(0)

        for i in range(2, len(self.list_h_variables)):
            B = -2 * (self.list_h_variables[i - 1] + self.list_h_variables[i])
            self.list_B_components.append(B)

    def _listDComponentsFill(self):
        self.list_D_components.append(0)
        self.list_D_components.append(0)

        for i in range(2, len(self.list_h_variables)):
            D = self.list_h_variables[i]
            self.list_D_components.append(D)

    def _listFComponentsFill(self):
        self.list_F_components.append(0)
        self.list_F_components.append(0)

        for i in range(2, len(self.list_h_variables)):
            F = -3 * ((self.list_y[i] - self.list_y[i - 1]) / self.list_h_variables[i] -
                      (self.list_y[i - 1] - self.list_y[i - 2]) / self.list_h_variables[i - 1])
            self.list_F_components.append(F)

    def _listKsiVariablesFill(self):
        self.list_ksi_variables = [0 for i in range(self.number_nodes + 1)] # Начальная инициализация списка нулями.
        self.list_ksi_variables[1] = self.conditions1 / 2

        for i in range(2, self.number_nodes):
            ksi = (self.list_D_components[i] /
                   (self.list_B_components[i] - self.list_A_components[i] * self.list_ksi_variables[i]))
            self.list_ksi_variables[i + 1] = ksi

    def _listEtaVariablesFill(self):
        self.list_eta_variables = [0 for i in range(self.number_nodes + 1)]  # Начальная инициализация списка нулями.
        self.list_eta_variables[1] = self.conditions1 / 2

        for i in range(2, self.number_nodes):
            eta = ((self.list_F_components[i] + self.list_A_components[i] * self.list_eta_variables[i]) /
                   (self.list_B_components[i] - self.list_A_components[i] * self.list_ksi_variables[i]))
            self.list_eta_variables[i + 1] = eta


    def _listACoefficientsFill(self):
        self.list_a_coefficients.append(0)

        for i in range(1, self.number_nodes):
            self.list_a_coefficients.append(self.list_y[i - 1])


    def _listCCoefficientsFill(self):
        self.list_c_coefficients = [0 for i in range(self.number_nodes + 1)]  # Начальная инициализация списка нулями.
        self.list_c_coefficients[-1] = self.conditions2 / 2

        for i in range(self.number_nodes - 1, -1, -1):
            self.list_c_coefficients[i] = (self.list_ksi_variables[i + 1] * self.list_c_coefficients[i + 1]
                                           + self.list_eta_variables[i + 1])

    def _listBCoefficientsFill(self):
        self.list_b_coefficients.append(0)

        for i in range(1, self.number_nodes):
            b = ((self.list_y[i] - self.list_y[i - 1]) / self.list_h_variables[i] -
                 self.list_h_variables[i] * (self.list_c_coefficients[i + 1] + 2 * self.list_c_coefficients[i]) / 3)
            self.list_b_coefficients.append(b)

    def _listDCoefficientsFill(self):
        self.list_d_coefficients.append(0)

        for i in range(1, self.number_nodes):
            d = (self.list_c_coefficients[i + 1] - self.list_c_coefficients[i]) / (3 * self.list_h_variables[i])
            self.list_d_coefficients.append(d)


if __name__ == "__main__":
    argument_x = 6.8
    boundary_conditions = (0, 0)

    list_points = list()
    with open("files/file1.txt", "r") as file:
        for line in file:
            point = tuple(map(float, line.split()))
            list_points.append(point)


    cubicspline = CubicSplineInterpolation(argument_x, list_points, boundary_conditions)
    cubicspline.interpolate()
    print(cubicspline.value_y)
