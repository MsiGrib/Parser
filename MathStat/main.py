from collections import Counter
from tqdm import tqdm
from scipy.stats import t
import matplotlib.pyplot as plt
import os
import platform
import numpy as np
import statistics
import scipy.stats as stats
from scipy import stats


def readFile(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        numbers = []
        for line in tqdm(lines, desc="Read file", unit="line"):
            numbers.append(int(line.strip()))
    return numbers


def quickSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quickSort(left) + middle + quickSort(right)


def calckBaseStat(arr):
    print("-----------------------------------------------------------")
    countNegative = 0
    for item in arr:
        if item < 0:
            countNegative += 1
    print("Negative value count: ", countNegative)

    print("Min value: ", arr[0])
    print("Max value: ", arr[len(arr) - 1])

    sumValue = 0
    for item in arr:
        sumValue += item
    print("Arithmetic mean: ", sumValue / len(arr))

    if len(arr) % 2 == 0:
        medianMean = (arr[len(arr) // 2] + arr[(len(arr) // 2) + 1]) / 2
    else:
        medianMean = arr[len(arr) // 2]
    print("Median mean: ", medianMean)
    print("-----------------------------------------------------------")


def plotUniqueValue(arrSorted):
    counter = Counter(arrSorted)
    uniqueNumbers = list(counter.keys())
    counts = list(counter.values())

    binEdges = np.linspace(min(uniqueNumbers), max(uniqueNumbers), 1000)
    binnedCounts, _ = np.histogram(uniqueNumbers, bins=binEdges, weights=counts)

    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    plt.bar(binEdges[:-1], binnedCounts, width=np.diff(binEdges), align='edge')
    plt.xlabel('Уникальные числа')
    plt.ylabel('Количество')
    plt.title('Математическая статистика чисел (агрегировано)')

    plt.subplot(1, 2, 2)
    plt.boxplot(arrSorted[::100], vert=False)
    plt.xlabel('Значения')
    plt.title('Коробчатая диаграмма для выявления выбросов')

    plt.tight_layout()
    plt.show()


def analizIQR(arrSorted):
    q1 = np.percentile(arrSorted, 25)
    q3 = np.percentile(arrSorted, 75)
    IQR = q3 - q1

    lowerBound = q1 - 1.5 * IQR
    upperBound = q3 + 1.5 * IQR
    outliers = [x for x in arrSorted if x < lowerBound or x > upperBound]

    print("-----------------------------------------------------------")
    print(f"IQR: {IQR}")
    print(f"Нижняя граница выбросов: {lowerBound}")
    print(f"Верхняя граница выбросов: {upperBound}")
    print(f"Количество выбросов: {len(outliers)}")
    print("-----------------------------------------------------------")

    binEdges = np.linspace(min(arrSorted), max(arrSorted), 1000)
    binnedCounts, _ = np.histogram(arrSorted, bins=binEdges)

    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    plt.bar(binEdges[:-1], binnedCounts, width=np.diff(binEdges), align='edge', alpha=0.75, label='Данные')
    plt.axvline(x=lowerBound, color='r', linestyle='--', label='Нижняя граница выбросов')
    plt.axvline(x=upperBound, color='r', linestyle='--', label='Верхняя граница выбросов')
    plt.xlabel('Значения')
    plt.ylabel('Частота')
    plt.yscale('log')
    plt.title('Распределение данных с выбросами (агрегировано)')
    plt.legend()

    plt.tight_layout()
    plt.show()


def analizZScore(arr):
    meanValue = statistics.mean(arr)
    stdDev = statistics.stdev(arr)
    zScores = [(x - meanValue) / stdDev for x in arr]
    print("-----------------------------------------------------------")
    print(f"Стандартное отклонение: {stdDev}")

    zThreshold = 3  # порог для определения выбросов
    outliers = [(i, z) for i, z in enumerate(zScores) if abs(z) > zThreshold]
    print(f"Количество выбросов: {len(outliers)}")
    print("-----------------------------------------------------------")

    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    plt.plot(range(len(zScores)), zScores, label='Z-Score', alpha=0.75)
    plt.axhline(y=zThreshold, color='r', linestyle='--', label='Порог выбросов (+)')
    plt.axhline(y=-zThreshold, color='r', linestyle='--', label='Порог выбросов (-)')
    plt.xlabel('Индекс')
    plt.ylabel('Z-Score')
    plt.yscale('linear')
    plt.title('Z-Score распределения данных')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(arr, bins=50, alpha=0.75, label='Данные')
    plt.axvline(x=meanValue + zThreshold * stdDev, color='r', linestyle='--', label='Порог выбросов (+)')
    plt.axvline(x=meanValue - zThreshold * stdDev, color='r', linestyle='--', label='Порог выбросов (-)')
    plt.xlabel('Значения')
    plt.ylabel('Частота')
    plt.yscale('log')
    plt.title('Распределение данных с выбросами')
    plt.legend()

    plt.tight_layout()
    plt.show()


def analizTestGrubbs(arr, alpha=0.05):
    n = len(arr)
    mean = np.mean(arr)
    stdDev = np.std(arr)
    zScores = np.abs((arr - mean) / stdDev)
    G = np.max(zScores)
    tCrit = t.ppf(1 - alpha / (2 * n), n - 2)
    GCrit = ((n - 1) / np.sqrt(n)) * np.sqrt(tCrit ** 2 / (n - 2 + tCrit ** 2))

    isOutlier = G > GCrit
    outlierIndex = np.argmax(np.abs(zScores))

    print("-----------------------------------------------------------")
    print(f"Значение G: {G}")
    print(f"Критическое значение G: {GCrit}")
    print(f"Наличие выброса: {'Да' if isOutlier else 'Нет'}")
    print(f"Индекс выброса: {outlierIndex if isOutlier else 'Нет выбросов'}")
    print("-----------------------------------------------------------")

    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    plt.plot(range(len(zScores)), zScores, label='Z-Score', alpha=0.75)
    plt.axhline(y=GCrit, color='r', linestyle='--', label='Порог выбросов (+)')
    plt.axhline(y=-GCrit, color='r', linestyle='--', label='Порог выбросов (-)')
    plt.scatter(outlierIndex, zScores[outlierIndex], color='r', label='Выброс', zorder=5)
    plt.xlabel('Индекс')
    plt.ylabel('Z-Score')
    plt.yscale('linear')
    plt.title('Z-Score распределения данных')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(arr, bins=50, alpha=0.75, label='Данные')
    if isOutlier:
        plt.axvline(x=arr[outlierIndex], color='r', linestyle='--', label='Выброс')
    plt.xlabel('Значения')
    plt.ylabel('Частота')
    plt.yscale('log')
    plt.title('Распределение данных с выбросами')
    plt.legend()

    plt.tight_layout()
    plt.show()


def removeOutliersIQR(arrSorted):
    if not isinstance(arrSorted, np.ndarray):
        arrSorted = np.array(arrSorted)
    Q1 = np.percentile(arrSorted, 25)
    Q3 = np.percentile(arrSorted, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return arrSorted[(arrSorted >= lower_bound) & (arrSorted <= upper_bound)]


def viewRemoveOutliers(arrClear):
    plt.figure(figsize=(12, 6))
    plt.hist(arrClear, bins=100, density=True, alpha=0.6, color='g')

    mu, std = stats.norm.fit(arrClear)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Результаты подгонки: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()

    k2, p = stats.normaltest(arrClear)
    alpha = 0.05
    print("-----------------------------------------------------------")
    print("p = {:g}".format(p))
    if p < alpha:
        print("Нулевая гипотеза может быть отвергнута")
    else:
        print("Нулевая гипотеза не может быть отвергнута")

    stat, p = stats.shapiro(arrClear[:5000])
    print('Тест Шапиро-Уилка: Statistics=%.3f, p=%.3f' % (stat, p))
    if p > alpha:
        print('Пример выглядит по Гауссу (fail to reject H0)')
    else:
        print('Образец не выглядит гауссовским (reject H0)')
    print("-----------------------------------------------------------")


def viewPlotStat(arr, arrSorted):
    calckBaseStat(arrSorted)
    plotUniqueValue(arrSorted)
    analizIQR(arrSorted)
    analizZScore(arr)
    analizTestGrubbs(arr)


def removeOutliersZscore(arrSorted, threshold=3):
    if not isinstance(arrSorted, np.ndarray):
        arrSorted = np.array(arrSorted)
    zScores = np.abs(stats.zscore(arrSorted))
    return arrSorted[zScores < threshold]


def removeOutliersNormalRaspr(arrSorted):
    sumValue = 0
    for item in arrSorted:
        sumValue += item
    arithmeticMean = sumValue / len(arrSorted)

    filteredArray = [x for x in arrSorted if x <= arithmeticMean]

    print("-----------------------------------------------------------")
    print("Размер исходного массива: ", len(arrSorted))
    print("Размер итогового массива: ", len(filteredArray))
    lostPercentage = ((len(arrSorted) - len(filteredArray)) / len(arrSorted)) * 100
    print("Сколько значений отбросили: ", len(arrSorted) - len(filteredArray))
    print("Мы выбросили {:.2f}%".format(lostPercentage))
    print("-----------------------------------------------------------")

    viewRemoveOutliers(filteredArray)
    return filteredArray


def saveFile(array, fileName):
    desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filePath = os.path.join(desktopPath, fileName)
    with open(filePath, 'w') as file:
        for number in tqdm(array, desc=f"Запись чисел в файл {fileName}", unit="число"):
            file.write(f"{number}\n")


if __name__ == '__main__':
    fileName = 'Result.txt'
    filePath = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'), fileName)
    array = readFile(filePath)
    arraySorted = quickSort(array)

    # Base stat
    viewPlotStat(array, arraySorted)

    # IQR
    cleanedArrayIQR = removeOutliersIQR(arraySorted)
    viewRemoveOutliers(cleanedArrayIQR)
    saveFile(cleanedArrayIQR, "CleanedArrayIQR.txt")

    # Z-scores
    cleanedArrayZscores = removeOutliersZscore(arraySorted)
    viewRemoveOutliers(cleanedArrayZscores)
    saveFile(cleanedArrayZscores, "CleanedArrayZscores.txt")

    # Remove bed value > threshold (Arithmetic Mean)
    cleanedArrayNormalRaspr = removeOutliersNormalRaspr(arraySorted)
    saveFile(cleanedArrayNormalRaspr, "CleanedArrayNormalRaspr.txt")