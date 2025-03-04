from config import PointValues, accuracy


def read_data_from_file(filename: str) -> list[PointValues]:
    function_data = list()

    with open(filename, "r") as file:
        for line in file.readlines():
            line_values = list(map(float, line.split()))
            line_data = PointValues(x=line_values[0], derivatives=line_values[1:])

            function_data.append(line_data)
    
    return function_data


def input_value(prompt: str, value_type: type, greater_then_zero: bool):
    while True:
        try:
            n = value_type(input(prompt))
        except ValueError:
            print("Invalid input\n")
        else:
            if greater_then_zero and n < 0:
                print("Expected value higher then 0\n")
            else:
                return n


def input_data():
    n = input_value("Enter Newton polynomial power: ", int, True)
    nodes_count = input_value("Enter Hermite polynomial nodes number: ", int, True)
    x = input_value("Enter x: ", float, False)

    return n, nodes_count, x


def print_ans(ans: float, type: int):
    print(f"{'Newton: ' if type == 1 else 'Hermite: '}\nf(x) = {round(ans, accuracy)}")


def __input_data_filename__() -> str:
    while True:
        filename = input("Input data file name: ")
        try:
            file = open(filename, "r")
        except (FileNotFoundError, FileExistsError) as exception:
            print(f"\n---- {exception} ----\n")
        else:
            return filename
