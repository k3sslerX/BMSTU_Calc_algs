# Вторая формула Рунге, в основе лежит правосторонняя формула
def runge_right(y_cur, y_next, y_next_next, step):
    return (4 * y_next - 3 * y_cur - y_next_next) / (2 * step)


# Вторая формула Рунге, в основе лежит левосторонняя формула
def runge_left(y_cur, y_prev, y_prev_prev, step):
    return (3 * y_cur - 4 * y_prev + y_prev_prev) / (2 * step)


def RightRunge(ydata, step):
    result = []
    for i in range(len(ydata) - 2):
        result.append("{:.3f}".format(runge_right(ydata[i], ydata[i + 1], ydata[i + 2], step)))

    result.append("-")
    result.append("-")

    return result


def LeftRunge(ydata, step):
    result = ["-", "-"]
    for i in range(2, len(ydata)):
        result.append("{:.3f}".format(runge_left(ydata[i], ydata[i - 1], ydata[i - 2], step)))

    return result

# Центральная формула Рунге
def runge_center(y_prev, y_next, step):
    return (y_next - y_prev) / (2 * step)

def CenterRunge(ydata, step):
    # Добавляем символы "-" для первых двух точек
    result = ["-", "-"]
    # Вычисляем производные только для точек в центре (для третьей и четвёртой)
    result.append("{:.3f}".format(runge_center(ydata[1], ydata[3], step)))
    result.append("{:.3f}".format(runge_center(ydata[2], ydata[4], step)))
    # Добавляем символы "-" для последних двух точек
    result.append("-")
    result.append("-")
    return result
