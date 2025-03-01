import os
import math
import matplotlib.pyplot as plt
from numpy.ma.extras import average
import numpy as np
from scipy.interpolate import interp1d
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
    if method == 'approx1':
        numerator = sum(map(lambda x, y: x * y, data_x, data_y)) / len(data_x)
        denominator = sum(map(lambda x: pow(x, 2), data_x)) / len(data_x)
        return numerator / denominator
    elif method == 'approx2':
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


def create_approximate_line(data_x, data_y, color_index, type='approx1', label='', coeff=False):
    """
    Создание аппроксимирующей прямой с использованием выбранного метода.
    
    :param data_x: список значений X
    :param data_y: список значений Y
    :param color_index: индекс цвета для построения линии
    :param type: метод вычисления ('approx1' или 'approx2')
    :param label: подпись линии
    :param coeff: булевый параметр, определяющий, нужно ли добавлять коэффициент в подпись
    """
    if type == "curve":
        new_data_x = np.linspace(min(data_x), max(data_x), 100)
        cubic_interpolation_model = interp1d(data_x, data_y, kind = "cubic")
        new_data_y = cubic_interpolation_model(new_data_x)
    else:
        calculated_coeff = calculate_coefficient(data_x, data_y, type)
        print(f"Коэффициент аппроксимации ({type}):", calculated_coeff)
        offset = sum(data_y) / len(data_y) - calculated_coeff * sum(data_x) / len(data_x)
        print(f"Смещение: {offset}")
        new_data_x = [0, max(data_x)]
        new_data_y = [offset, offset + calculated_coeff * max(data_x)]

    if coeff and type != "curve":
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


os.system("rm -rf Laba\ 2.2.3/graphs")
os.system("mkdir -p Laba\ 2.2.3/graphs")

#types: approx1 - линейная аппроксимация, график проходит через нулевую   точку, 
#       approx2 - линейная аппроксимация, график проходит через ненулевую точку
#       curve - кривая, котрую надо промести с апроксимизацией

# data_pltDataXY = {  
#     "plt1": {
#             "type": "approx1",
#             "grName": "Зависимость ΔT(N)",
#             "dataY": [[0, 360.68, 852.52, 1250.69, 1640.62], [0, 196.38, 373.05, 564.26, 826.39]],
#             "dataX": [[0, 1.8, 4.08, 6.26, 8.01], [0, 1.94, 4.05, 6.01, 7.91]],
#             "names": ["Экс. №1", "Экс. №2"],
#             "nameX": "ΔT, K",
#             "nameY": "N, мВт"
#             }
# }

data_pltDataXY = {  
    "plt1": {
            "type": "approx2",
            "grName": "Зависимость R(Qн)",
            "dataX": [[35.88, 72.25, 109.28, 147.24, 183.89, 225.05, 267.23, 306.59]],
            "dataY": [[19.78, 20.01, 20.30, 20.56, 20.68, 20.92, 21.19, 21.38]],
            "names": ["T = 23.4°C"],
            "nameX": "Qн, мДж",
            "nameY": "R, Ом"
            },
    "plt2": {
            "type": "approx2",
            "grName": "Зависимость R(Qн)",
            "dataY": [[20.42, 20.65, 20.95, 21.17, 21.42, 21.55, 21.76, 21.98]],
            "dataX": [[34.56, 69.74, 107.40, 144.69, 184.87, 220.55, 260.30, 300.38]],
            "names": ["T = 33.4°C"],
            "nameX": "Qн, мДж",
            "nameY": "R, Ом"
            },
    "plt3": {
            "type": "approx2",
            "grName": "Зависимость R(Qн)",
            "dataY": [[21.47, 21.80, 22.01, 22.25, 22.34, 22.06, 22.75, 22.95]],
            "dataX": [[34.45, 69.41, 104.99, 145.64, 179.04, 216.09, 253.25, 292.31]],
            "names": ["T = 48.4°C"],
            "nameX": "Qн, мДж",
            "nameY": "R, Ом"
            },
    "plt4": {
            "type": "approx2",
            "grName": "Зависимость R(Qн)",
            "dataY": [[21.47, 21.80, 22.01, 22.25, 22.34, 22.06, 22.75, 22.95]],
            "dataX": [[34.14, 69.20, 104.17, 139.71, 175.71, 213.14, 249.96, 288.15]],
            "names": ["T = 58.4°C"],
            "nameX": "Qн, мДж",
            "nameY": "R, Ом"
            },
    "plt5": {
            "type": "approx2",
            "grName": "Зависимость R(Qн)",
            "dataY": [[23.05, 23.11, 23.44, 23.50, 23.77, 23.98, 24.12, 24.25]],
            "dataX": [[33.59, 67.60, 102.57, 137.86, 173.36, 208.24, 246.85, 289.04]],
            "names": ["T = 68.4°C"],
            "nameX": "Qн, мДж",
            "nameY": "R, Ом"
            },
    "plt6": {
            "type": "approx2",
            "grName": "Зависимость R(T)",
            "dataY": [[18.6, 20.27, 21.4, 21.4, 22.85]],
            "dataX": [[23.4, 33.4, 48.4, 58.4, 68.4]],
            "names": [""],
            "nameX": "T, °C",
            "nameY": "R, Ом"
            },
    "plt7": {
            "type": "approx1",
            "grName": "Зависимость ln(k) от ln(T)",
            "dataY": [[3.39, 3.40, 3.56, 3.54, 3.48]],
            "dataX": [[5.69, 5.72, 5.77, 5.8, 5.83]],
            "names": [""],
            "nameX": "ln(T)",
            "nameY": "ln(k)"
            }
    }
for i in range(1, len(data_pltDataXY)+1):
    for j in range(len(data_pltDataXY.get("plt" + str(i)).get("dataY"))):
        dataY = data_pltDataXY.get("plt" + str(i)).get("dataY")[j]
        dataX = data_pltDataXY.get("plt" + str(i)).get("dataX")[j]
        names = data_pltDataXY.get("plt" + str(i)).get("names")
        type = data_pltDataXY.get("plt" + str(i)).get("type")
        nameX = data_pltDataXY.get("plt" + str(i)).get("nameX")
        nameY = data_pltDataXY.get("plt" + str(i)).get("nameY")
        plot_scatter(dataX, dataY, 0.2, 0.02)
        #print(j)
        create_approximate_line(dataX, dataY, j, type, label=names[j], coeff=True)

        print(root_mean_square_value(dataY), root_mean_arithmetic_value(dataY),
        root_mean_square_value(dataX), root_mean_arithmetic_value(dataX))

    plt.ylabel(nameY)
    plt.xlabel(nameX)
    plt.title(data_pltDataXY.get("plt" + str(i)).get("grName"))
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Laba 2.2.3/graphs/figure{i}")
    plt.show()
