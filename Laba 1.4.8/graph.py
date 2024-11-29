import matplotlib.pyplot as plt
from numpy.ma.extras import average

indexOfColor = 0
indexOfCoefficient = 0
colors = ["orange", "blue", "green"]
coefficients = []


def approximatingStraightLineCoefficient1(dataX, dataY):
    global coefficients, indexOfCoefficient
    coefficient = (sum(map(lambda x, y: x * y, dataX, dataY)) / len(dataX)) / (
                sum(map(lambda x: pow(x, 2), dataX)) / len(dataX))
    coefficients.append(coefficient)
    return coefficient

def approximatingStraightLineCoefficient2(dataX, dataY):
    global coefficients, indexOfCoefficient
    coefficient = (sum(map(lambda x, y: x * y, dataX, dataY)) / len(dataX) - sum(dataX) / len(dataX) * sum(dataY) / len(dataY)) \
                  / (sum(map(lambda x: pow(x, 2), dataX)) / len(dataX) - (sum(dataX) / len(dataX))**2)
    coefficients.append(coefficient)
    return coefficient

def printLine(dataX, dataY):
    global indexOfColor
    plt.plot(dataX, dataY, c="black")  # colors[indexOfColor]
    indexOfColor += 1


def createApproximateLine1(dataX, dataY):
    approximatCoefficient = approximatingStraightLineCoefficient1(dataX, dataY)
    print(f"approximatingStraightLineCoefficient:", approximatingStraightLineCoefficient1(dataX, dataY))
    new_dataX = [0, max(dataX)]
    new_dataY = [0, max(dataX) * approximatCoefficient]
    printLine(new_dataX, new_dataY)


def createApproximateLine2(dataX, dataY):
    approximatCoefficient = approximatingStraightLineCoefficient2(dataX, dataY)
    print(f"approximatingStraightLineCoefficient:", approximatingStraightLineCoefficient2(dataX, dataY))
    print(max(dataX) * approximatCoefficient)
    new_dataX = [dataX[0], max(dataX)]
    new_dataY = [dataY[0], dataY[0] + max(dataX) * approximatCoefficient]
    printLine(new_dataX, new_dataY)


def printScaters(dataX, dataY):
    yerr = 0.000005
    xerr = 0.000005  # list(map(lambda x: float(0.002 * x + 0.002), dataX))

    plt.scatter(dataX, dataY, s=5, c="black")
    #plt.errorbar(dataX, dataY, xerr=xerr, yerr=yerr, c="white", ecolor="black", barsabove=True)


# srednee kvadratichnoe znachenie
def rootMeanSquareValue(array):
    return sum(list(map(lambda x: x ** 2, array))) / len(array)

# srednee arifmeticheskoe znachenie
def rootMeanArifmValue(array):
    return sum(array) / len(array)

dataX = [[0, 0.0001, 0.0004, 0.0009, 0.001225, 0.0016, 0.002025, 0.0025, 0.003025, 0.0036]]
dataY = [[0.0086, 0.0092, 0.0089, 0.01, 0.0106, 0.0111, 0.01118, 0.0123, 0.0136, 0.0141]]

for i in range(len(dataX)):
    printScaters(dataX[i], dataY[i])
    createApproximateLine2(dataX[i], dataY[i])

plt.ylabel('I, m*(м)^2')
plt.xlabel('h^2, кг^2')
# plt.title('Зависимость Vв(Ia)')
plt.grid(True)
plt.show()

print(rootMeanSquareValue(dataY[0]), rootMeanArifmValue(dataY[0]), rootMeanSquareValue(dataX[0]), rootMeanArifmValue(dataX[0]))
