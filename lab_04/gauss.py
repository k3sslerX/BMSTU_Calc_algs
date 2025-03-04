class GaussMethod:
    """
    Класс для решения СЛАУ методом Гаусса
    """

    def __init__(
            self,
            matrix_slau: list[list[int | float]],
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.matrix_slau: list[list[int | float]] = matrix_slau

    @staticmethod
    def __print_tri_matrix(matrix) -> None:
        """
        Функция выводит матрицу СЛАУ на экран в консоли
        """
        print("Матрица СЛАУ (в верхне треугольной форме):")

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(f"{matrix[i][j]:^10.3f}", end=" ")
            print("\n")

    def gauss(self):
        """
        Решение системы уравнений методом Гаусса
        """
        n = len(self.matrix_slau)

        # Прямой ход метода Гаусса
        for i in range(n):
            pivot = self.matrix_slau[i][i]
            for j in range(i + 1, n):
                ratio = self.matrix_slau[j][i] / pivot
                for k in range(i, n + 1):
                    self.matrix_slau[j][k] -= ratio * self.matrix_slau[i][k]

        self.__print_tri_matrix(matrix=self.matrix_slau)

        # Обратный ход метода Гаусса
        x = [0 for _ in range(n)]

        for i in range(n - 1, -1, -1):
            s = sum(self.matrix_slau[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (self.matrix_slau[i][n] - s) / self.matrix_slau[i][i]

        return x
