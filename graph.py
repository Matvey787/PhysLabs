import os
import math
import matplotlib.pyplot as plt
from numpy.ma.extras import average
import numpy as np
from scipy.interpolate import interp1d
import sys

colors = ['orange', 'blue', 'green', 'red', 'yellow', 'purple']


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
            "type": "curve",
            "dataX": [[11.88, 13.59, 15.59, 17.59, 19.62, 21.69, 23.67, 25.65, 27.65, 29.69, 31.62, 33.65, 35.65]],
            "dataY": [[36.13, 35.26, 33.54, 30.55, 25.52, 17.59, 10.73, 7.68, 5.98, 4.86, 4.12, 3.75, 3.38]],
            "names": ["$\\tau^2 - \\tau_0^2(T)$"],
            "nameX": "T, °C",
            "nameY": "$\\tau^2 - \\tau_0^2$, мкс$^2$"
            }, 
    "plt2": {
            "type": "curve",
            "dataX": [[11.88, 13.59, 15.59, 17.59, 19.62, 21.69, 23.67, 25.65, 27.65, 29.69, 31.62, 33.65, 35.65]],
            "dataY": [[0.028, 0.028, 0.030, 0.033, 0.039, 0.057, 0.093, 0.13, 0.167, 0.206, 0.243, 0.267, 0.296]],
            "names": ["$\\frac{1}{\\tau^2 - \\tau_0^2}(T)$"],
            "nameX": "T, °C",
            "nameY": "$\\frac{1}{\\tau^2 - \\tau_0^2}$, мкс$^{-2}$"
            }, 
    }
for i in range(1, len(data_pltDataXY)+1):
    for j in range(len(data_pltDataXY.get("plt" + str(i)).get("dataY"))):
        dataY = data_pltDataXY.get("plt" + str(i)).get("dataY")[j]
        dataX = data_pltDataXY.get("plt" + str(i)).get("dataX")[j]
        names = data_pltDataXY.get("plt" + str(i)).get("names")
        type = data_pltDataXY.get("plt" + str(i)).get("type")
        nameX = data_pltDataXY.get("plt" + str(i)).get("nameX")
        nameY = data_pltDataXY.get("plt" + str(i)).get("nameY")
        plot_scatter(dataX, dataY, 0.01, 0.02)
        #print(j)
        create_approximate_line(dataX, dataY, j, type, label=names[j], coeff=True)

        print(root_mean_square_value(dataY), root_mean_arithmetic_value(dataY),
        root_mean_square_value(dataX), root_mean_arithmetic_value(dataX))

    plt.ylabel(nameY)
    plt.xlabel(nameX)
    plt.title(data_pltDataXY.get("plt" + str(i)).get("grName"))
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Laba 3.4.2/graphs/figure{i}")
    plt.show()
