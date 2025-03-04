from config import PointValues
from math import factorial
from config import accuracy


def cut_data(function_data_list: list[PointValues], user_x: float, nodes: float) -> list[PointValues] | None:
    if nodes % 2 == 0:
        left_shift = nodes // 2
        right_shift = nodes // 2 - 1
    else:
        left_shift = nodes // 2
        right_shift = nodes // 2

    for i in range(len(function_data_list) - 1):
        if function_data_list[i]['x'] <= user_x <= function_data_list[i + 1]['x']:
            if user_x == function_data_list[i + 1]['x']:
                pivot_point = i + 1
            else:
                pivot_point = i

            if pivot_point - left_shift < 0:
                right_shift += abs(pivot_point - left_shift)
                left_shift -= abs(pivot_point - left_shift)
            elif pivot_point + right_shift > len(function_data_list) - 1:
                delta = pivot_point + right_shift - len(function_data_list) + 1
                right_shift -= delta
                left_shift += delta

            return function_data_list[pivot_point - left_shift: pivot_point + right_shift + 1]

    return None


def _pos(number: int):
    if number > 0:
        return number
    else:
        return 0


def find_divided_difference_table(function_data_list: list[PointValues], nodes_count: int, d_count: int) -> list:
    y_values = list()

    for i in range(nodes_count):
        item = function_data_list[i]
        y_values.extend([item['derivatives'][0]] * d_count)

    divided_difference_table = [y_values]
    is_end = False
    iter_number = 1
    while not is_end:
        new_column = _get_new_column(function_data_list, divided_difference_table[-1], iter_number, d_count)
        divided_difference_table.append(new_column)

        if len(new_column) == 1:
            is_end = True
        else:
            iter_number += 1

    return divided_difference_table


def _get_new_column(function_data_list: list[PointValues], prev_column: list, iter_number: int, d_count: int) -> list:
    new_column = list()
    for i in range(len(prev_column) - 1):
        if function_data_list[(i + iter_number) // d_count]['x'] == function_data_list[i // d_count]['x']:
            new_column.append(function_data_list[i // d_count]['derivatives'][iter_number] / factorial(iter_number))
        else:
            new_column.append((prev_column[i + 1] - prev_column[i]) / (function_data_list[(i + iter_number)
                                                                                          // d_count]['x'] -
                                                                       function_data_list[i // d_count]['x']))

    new_column = list(map(lambda x: round(x, accuracy), new_column))

    return new_column


def function_interpolation(z_values: list, divided_difference_table: list, x: float) -> float:
    ans = 0
    k_list = [1]
    current_k = 1

    for current_x in z_values:
        current_k *= (x - current_x)
        k_list.append(current_k)
    # print("--ddt------")
    for i, column in enumerate(divided_difference_table):
        # print(column[0], k_list[i])
        ans += column[0] * k_list[i]
    # print("-----------")

    return ans


def calculate_ans_hermite(data: list[PointValues], current_x: float, current_nodes_count: int) -> float | None:
    derivatives_count = 3

    hermit_data = cut_data(data, current_x, current_nodes_count)
    if hermit_data is None:
        return None

    table = find_divided_difference_table(hermit_data, current_nodes_count, derivatives_count)
    z_values = list()
    for item in hermit_data:
        z_values.extend([item['x']] * derivatives_count)

    ans = function_interpolation(z_values, table, current_x)

    return ans


def calculate_ans_newton(data: list[PointValues], current_x: float, n: int) -> float | None:
    derivatives_count = 1

    newton_data = cut_data(data, current_x, n + 1)
    if newton_data is None:
        return None

    table = find_divided_difference_table(newton_data, n + 1, derivatives_count)

    z_values = list()
    for item in newton_data:
        z_values.extend([item['x']] * derivatives_count)

    ans = function_interpolation(z_values, table, current_x)

    return ans


def newton_reverse_interpolation(data: list[PointValues]) -> float | None:
    reverse_data = list()
    for item in data:
        reverse_data.append(PointValues(x=item['derivatives'][0], derivatives=[item['x']]))

    ans = calculate_ans_newton(reverse_data, 0, 4)

    return ans


def hermite_reverse_interpolation(data: list[PointValues]) -> float | None:
    reverse_data = list()
    for item in data:
        reverse_x = item['derivatives'][0]
        reverse_y = []
        for y in item['derivatives'][1:]:
            if y != 0:
                reverse_y.append(1 / y)
            else:
                reverse_y.append(y)
        # reverse_y = [1 / y for y in item['derivatives'][1:]]
        reverse_y.insert(0, item['x'])

        reverse_data.append(PointValues(x=reverse_x, derivatives=reverse_y))

    ans = calculate_ans_hermite(reverse_data, 0, 4)

    return ans
