from prettytable import PrettyTable

from comp_functions import *
from io_functions import *


def action_input() -> int:
    while True:
        try:
            action = int(input("Enter action: "))
        except ValueError:
            print("Invalid input")
        else:
            if action < 0 or action > 4:
                print("Wrong action passed")
            else:
                return action


def print_menu():
    print("-----------------------")
    print("1) Hermite & Newton interpolations\n2) Compare polynomials\n"
          "3) Count function root\n4) Count system of equations\n0) Exit")
    print("-----------------------")


def task_1(data: list[PointValues]):
    n, nodes_count, x = input_data()

    if nodes_count > len(data):
        print("Too many nodes for given data, can't build an answer")
    elif n + 1 > len(data):
        print("Too high power number for given data, can't build an answer")
    elif x < data[0]['x'] or x > data[-1]['x']:
        print("Passed argument is out of range, can't build an answer")
    else:
        ans_hermit = calculate_ans_hermite(data, x, nodes_count)
        ans_newton = calculate_ans_newton(data, x, n)

        print_ans(ans_hermit, 2)
        print_ans(ans_newton, 1)


def task_2(data: list[PointValues]):
    user_x = input_value("Enter x: ", float, False)

    table = PrettyTable()
    table.field_names = ['n', 'hermite', 'newton']

    for n in range(1, 6):
        table.add_row([n, round(calculate_ans_hermite(data, user_x, n), accuracy),
                       round(calculate_ans_newton(data, user_x, n), accuracy)])

    print(table)


def task_3(data: list[PointValues]):
    print(f"Newton polynomial answer: {newton_reverse_interpolation(data)}")
    print(f"Hermite polynomial answer: {hermite_reverse_interpolation(data)}")


def task_4(data_1: list[PointValues], data_2: list[PointValues]):
    new_data_table = list()
    for current_point in data_1:
        current_x = current_point['x']
        y_1 = current_point['derivatives'][0]
        y_2 = calculate_ans_newton(data_2, current_x, 4)

        new_data_table.append(PointValues(x=current_x, derivatives=[y_2 - y_1]))

    ans_x = newton_reverse_interpolation(new_data_table)
    ans_y = calculate_ans_newton(data_1, ans_x, 4)

    print(f"Answer: ({ans_x}, {ans_y})\n")


def main_menu():
    function_data_from_file = read_data_from_file('data/data_1.txt')
    task_3_data_1 = read_data_from_file('data/data_2.txt')
    task_3_data_2 = read_data_from_file('data/data_3.txt')

    while True:
        print_menu()
        action = action_input()
        if action == 1:
            task_1(function_data_from_file)
        elif action == 2:
            task_2(function_data_from_file)
        elif action == 3:
            task_3(function_data_from_file)
        elif action == 4:
            task_4(task_3_data_1, task_3_data_2)
        elif action == 0:
            print("Exiting programm")
            break


if __name__ == "__main__":
    main_menu()
