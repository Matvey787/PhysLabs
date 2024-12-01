import os
import matplotlib.pyplot as plt
from numpy.ma.extras import average
import sys

colors = ['orange', 'blue', 'green', 'red', 'yellow']


def calculate_coefficient(data_x, data_y, method='method1'):
    """
    Вычисляет коэффициент аппроксимирующей прямой одним из двух методов.
    
    :param data_x: список значений X
    :param data_y: список значений Y
    :param method: метод вычисления ('method1' или 'method2')
    :return: коэффициент аппроксимирующей прямой
    """
    if method == 'method1':
        numerator = sum(map(lambda x, y: x * y, data_x, data_y)) / len(data_x)
        denominator = sum(map(lambda x: pow(x, 2), data_x)) / len(data_x)
        return numerator / denominator
    elif method == 'method2':
        mean_x = sum(data_x) / len(data_x)
        mean_y = sum(data_y) / len(data_y)
        numerator = sum(map(lambda x, y: x * y, data_x, data_y)) / len(data_x) - mean_x * mean_y
        denominator = sum(map(lambda x: pow(x, 2), data_x)) / len(data_x) - mean_x ** 2
        return numerator / denominator
    else:
        raise ValueError("Неверный метод вычислений.")


def plot_line(data_x, data_y, color, label):
    """
    Построение линии с заданными параметрами.
    
    :param data_x: список значений X
    :param data_y: список значений Y
    :param color: цвет линии
    :param label: подпись линии
    """
    plt.plot(data_x, data_y, c=color, label=label)


def create_approximate_line(data_x, data_y, color_index, method='method1', label='', coeff=False):
    """
    Создание аппроксимирующей прямой с использованием выбранного метода.
    
    :param data_x: список значений X
    :param data_y: список значений Y
    :param color_index: индекс цвета для построения линии
    :param method: метод вычисления ('method1' или 'method2')
    :param label: подпись линии
    :param coeff: булевый параметр, определяющий, нужно ли добавлять коэффициент в подпись
    """
    calculated_coeff = calculate_coefficient(data_x, data_y, method)
    print(f"Коэффициент аппроксимации ({method}):", calculated_coeff)
    new_data_x = [min(data_x), max(data_x)]
    new_data_y = [calculated_coeff * min(data_x), calculated_coeff * max(data_x)]
    if coeff:
        plot_line(new_data_x, new_data_y, colors[color_index], f"{label}, k={calculated_coeff:.2f}")
    else:
        plot_line(new_data_x, new_data_y, colors[color_index], label)


def plot_scatter(data_x, data_y, error_x=None, error_y=None):
    """
    Отображение точек данных с возможностью добавления погрешностей.
    
    :param data_x: список значений X
    :param data_y: список значений Y
    :param error_x: погрешность по оси X (по умолчанию None)
    :param error_y: погрешность по оси Y (по умолчанию None)
    """
    plt.scatter(data_x, data_y, s=10, c='black')  # Отображаем точки данных
    if error_x is not None and error_y is not None:
        plt.errorbar(data_x, data_y, xerr=error_x, yerr=error_y, fmt='none', ecolor='gray', elinewidth=0.7, capsize=0, zorder=-1)


def root_mean_square_value(array):
    """
    Среднее квадратичное значение массива.
    
    :param array: массив чисел
    :return: среднее квадратичное значение
    """
    return sum(list(map(lambda x: x ** 2, array))) / len(array)


def root_mean_arithmetic_value(array):
    """
    Среднее арифметическое значение массива.
    
    :param array: массив чисел
    :return: среднее арифметическое значение
    """
    return sum(array) / len(array)


os.system("rm -rf Laba\ 1.4.8/graphs")
os.system("mkdir -p Laba\ 1.4.8/graphs")

data_pltDataXY = {  
    "plt1": {
            "dataY": [[0, 3.13, 6.49, 9.74, 12.98, 16.25]],
            "dataX": [[0, 1, 2, 3, 4, 5]],
            "names": ["Медь"]
            },
    "plt2": {
            "dataY": [[0, 4.01, 8.15, 12.05, 16.08, 20.11]],
            "dataX": [[0, 1, 2, 3, 4, 5]],
            "names": ["Аллюминий"]
    },
    "plt3": {
            "dataY": [[0, 4.13, 8.27, 12.39, 16.53, 20.65]],
            "dataX": [[0, 1, 2, 3, 4, 5]],
            "names": ["Сталь"]
    }
}
for i in range(1, len(data_pltDataXY)+1):
    for j in range(len(data_pltDataXY.get("plt" + str(i)).get("dataY"))):
        dataY = data_pltDataXY.get("plt" + str(i)).get("dataY")[j]
        dataX = data_pltDataXY.get("plt" + str(i)).get("dataX")[j]
        names = data_pltDataXY.get("plt" + str(i)).get("names")
        plot_scatter(dataX, dataY, 0, 0.01)
        print(j)
        create_approximate_line(dataX, dataY, j, method='method1', label=names[j], coeff=True)

        print(root_mean_square_value(dataY), root_mean_arithmetic_value(dataY),
        root_mean_square_value(dataX), root_mean_arithmetic_value(dataX))

    plt.ylabel('f, кГц')
    plt.xlabel('n')
    plt.title('Зависимость f(n)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Laba 1.4.8/graphs/figure{i}")
    plt.show()
