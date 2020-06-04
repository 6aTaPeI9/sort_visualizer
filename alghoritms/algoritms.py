import typing
from functools import lru_cache

class Alghoritm:
    def get_pos_history(self, iteratin_index: int):
        raise NotImplementedError('Метод get_pos_history не реализован.')


class BubleSort(Alghoritm):
    NAME = 'Bubble'
    GROUP = 'Comparisons'

    def __init__(self, data: list):
        self.data = data
        self.end = False
        self.algh_gen = self.algh()

    def algh(self):
        for i in range(len(self.data) - 1):
            for j in range(0, len(self.data)-i-1):
                yield {'Position': (j, j+1), 'Command': 'Colorized'}

                if self.data[j] > self.data[j + 1]:
                    yield {'Position': (j, j+1), 'Command': 'Swap'}
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

    @lru_cache(maxsize=24)
    def get_pos_history(self, iteratin_index: int):
        """
            Метод возвращает позиции столбцов для следующей отрисовки.
            :param iteratin_index: параметр для попадения метода в кэш и
            возможности получения истории итерации.
        """
        try:
            result = self.algh_gen.__next__()
            return result
        except StopIteration:
            return None


class ShakeSort(Alghoritm):
    NAME = 'Shake'
    GROUP = 'Comparisons'

    def __init__(self, data: list):
        self.data = data
        self.end = False
        self.algh_gen = self.algh()

    def algh(self):
        data_range = len(self.data) - 1
        for i in range(data_range):
            swapped = False
            for j in range(i, data_range - i, 1):
                yield {'Position': (j, j+1), 'Command': 'Colorized'}

                if self.data[j] > self.data[j + 1]:
                    yield {'Position': (j, j+1), 'Command': 'Swap'}
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    swapped = True

            for j in range(data_range - i, i, -1):
                yield {'Position': (j - 1, j), 'Command': 'Colorized'}
                if self.data[j - 1] > self.data[j]:
                    yield {'Position': (j - 1, j), 'Command': 'Swap'}
                    self.data[j - 1], self.data[j] = self.data[j], self.data[j - 1]
                    swapped = True

            if not swapped:
                return


    @lru_cache(maxsize=24)
    def get_pos_history(self, iteratin_index: int):
        """
            Метод возвращает позиции столбцов для следующей отрисовки.
            :param iteratin_index: параметр для попадения метода в кэш и
            возможности получения истории итерации.
        """
        try:
            result = self.algh_gen.__next__()
            return result
        except StopIteration:
            return None


class OddEventSort(Alghoritm):
    NAME = 'Odd-Event'
    GROUP = 'Comparisons'

    def __init__(self, data: list):
        self.data = data
        self.end = False
        self.algh_gen = self.algh()

    def algh(self):
        data_range = len(self.data) - 1
        for i in range(data_range):
            swapped = False
            for j in range(0, data_range, 2):
                yield {'Position': (j, j+1), 'Command': 'Colorized'}

                if self.data[j] > self.data[j + 1]:
                    yield {'Position': (j, j+1), 'Command': 'Swap'}
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    swapped = True

            for j in range(1, data_range, 2):
                yield {'Position': (j, j+1), 'Command': 'Colorized'}

                if self.data[j] > self.data[j + 1]:
                    yield {'Position': (j, j+1), 'Command': 'Swap'}
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    swapped = True

            if not swapped:
                return


    @lru_cache(maxsize=24)
    def get_pos_history(self, iteratin_index: int):
        """
            Метод возвращает позиции столбцов для следующей отрисовки.
            :param iteratin_index: параметр для попадения метода в кэш и
            возможности получения истории итерации.
        """
        try:
            result = self.algh_gen.__next__()
            return result
        except StopIteration:
            return None


class CombSort(Alghoritm):
    NAME = 'Comb'
    GROUP = 'Comparisons'

    def __init__(self, data: list):
        self.data = data
        self.end = False
        self.algh_gen = self.algh()

    def algh(self):
        red_fact = len(self.data)
        swapped = True
        while red_fact > 1 or swapped:
            red_fact = max(1, int(red_fact / 1.25))
            swapped = False
            for i in range(len(self.data) - red_fact):
                j = i + red_fact
                yield {'Position': (i, j), 'Command': 'Colorized'}

                if self.data[i] > self.data[j]:
                    yield {'Position': (i, j), 'Command': 'Swap'}
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                    swapped = True


    @lru_cache(maxsize=24)
    def get_pos_history(self, iteratin_index: int):
        """
            Метод возвращает позиции столбцов для следующей отрисовки.
            :param iteratin_index: параметр для попадения метода в кэш и
            возможности получения истории итерации.
        """
        try:
            result = self.algh_gen.__next__()
            return result
        except StopIteration:
            return None


class QuickSort(Alghoritm):
    NAME = 'Quick'
    GROUP = 'Comparisons'

    def __init__(self, data: list):
        self.data = data
        self.end = False
        self.algh_gen = self.algh(0, len(self.data) - 1)

    def algh(self, start, end):
        if start >= end:
            return

        pivot = self.data[end]
        pivotIdx = start

        for i in range(start, end):
            yield {'Position': (i, pivotIdx), 'Command': 'Colorized'}
            if self.data[i] < pivot:
                yield {'Position': (i, pivotIdx), 'Command': 'Swap'}
                self.data[i], self.data[pivotIdx] = self.data[pivotIdx], self.data[i]
                pivotIdx += 1

        yield {'Position': (end, pivotIdx), 'Command': 'Swap'}
        self.data[end], self.data[pivotIdx] = self.data[pivotIdx], self.data[end]

        yield from self.algh(start, pivotIdx - 1)
        yield from self.algh(pivotIdx + 1, end)


    @lru_cache(maxsize=24)
    def get_pos_history(self, iteratin_index: int):
        """
            Метод возвращает позиции столбцов для следующей отрисовки.
            :param iteratin_index: параметр для попадения метода в кэш и
            возможности получения истории итерации.
        """
        try:
            result = self.algh_gen.__next__()
            return result
        except StopIteration:
            return None


class InsertSort(Alghoritm):
    NAME = 'InsertSort'
    GROUP = 'Inserts'

    def __init__(self, data: list):
        self.data = data
        self.end = False
        self.algh_gen = self.algh()

    def algh(self):
        for i in range(len(self.data)):
            j = i - 1
            val = self.data[i]
            yield {'Position': (self.data[i],), 'Command': 'Colorized', 'Color': 'green'}

            while val < self.data[j] and j >=0:
                self.data[j + 1] = self.data[j]
                yield {'Position': (j + 1,), 'Command': 'Insert', 'Value': self.data[j]}
                j -= 1

            yield {'Position': (j + 1,), 'Command': 'Insert', 'Value': val}
            self.data[j + 1] = val


    @lru_cache(maxsize=24)
    def get_pos_history(self, iteratin_index: int):
        """
            Метод возвращает позиции столбцов для следующей отрисовки.
            :param iteratin_index: параметр для попадения метода в кэш и
            возможности получения истории итерации.
        """
        try:
            result = self.algh_gen.__next__()
            return result
        except StopIteration:
            return None



# import random


# def generate_data(len):
#     return [random.randint(0, 10) for i in range(len)]


# def bubble_sort(data):
#     """
#         Пузырьковая сортировка
#         Сложность:
#             худшее: O(n^2)
#             среднее: O(n^2)
#             Лучшее: O(n)
#         Память: O(1)

#         Итерируемся от начала массива, сравнивая по 2 следующих элемента
#         тем самым вытесняя максимальный элемент за одну итерацию в самый конец
#     """
#     iters = 0
#     for i in range(len(data) - 1):
#         for j in range(len(data) - 1 - i):
#             if data[j] > data[j + 1]:
#                 data[j], data[j + 1] = data[j + 1], data[j]

#             iters += 1
#     print('Bubble iters: ', iters)
#     print('Bubble data: ', data)


# def shake_sort(data):
#     """
#         Шейкерная сортировка
#         Сложность:
#             худшее: O(n^2)
#             среднее: O(n^2)
#             Лучшее: O(n)
#         Память: O(1)
#         Работает так же как и пузырьковая, но работает в две стороны
#     """
#     data_rande = len(data) - 1
#     iters = 0
#     for i in range(data_rande):
#         swapped = False
#         for j in range(i, data_rande - i, 1):
#             iters += 1
#             if data[j] > data[j + 1]:
#                 data[j], data[j + 1] = data[j + 1], data[j]
#                 swapped = True

#         for j in range(data_rande - i, i, -1):
#             iters += 1
#             if data[j] < data[j - 1]:
#                 data[j], data[j - 1] = data[j - 1], data[j]
#                 swapped = True

#         if not swapped:
#             return

#     print('Shake iters: ', iters)
#     print('Shake data: ', data)


# def odd_even_sort(data):
#     """
#         Четно-нечетная сортировка.
#         Сложность:
#             худшее: O(n^2)
#             среднее: O(n^2)
#             Лучшее: O(n)
#         Память: O(1).
#         Сначала элементы с нечётными индексами сравниваются/обмениваются с элементами с чётными индексами (1-й со 2-м, 3-й с 4-м, 5-й с 6-м и т.д.).
#         Затем элементы с чётными индексами сравниваются/обмениваются с соседними элементами с нечётными индексами (2-й с 3-м, 4-й с 5-м, 6-й с 7-м и т.д.).
#         Затем снова нечётные сравниваются с чётными, потом снова чётные с нечётными и т.д.
#         Процесс завершается если в результате двух прогонов не происходило обменов - значит массив упорядочен.
#     """
#     data_rande = len(data) - 1
#     iters = 0
#     for i in range(data_rande):
#         swapped = False
#         for j in range(0, data_rande, 2):
#             iters += 1
#             if data[j] > data[j + 1]:
#                 data[j], data[j + 1] = data[j + 1], data[j]
#                 swapped = True

#         for j in range(1, data_rande, 2):
#             iters += 1
#             if data[j] > data[j + 1]:
#                 data[j], data[j + 1] = data[j + 1], data[j]
#                 swapped = True

#         if not swapped:
#             break

#     print('Odd-Even iters: ', iters)
#     print('Odd-Even data: ', data)


# def comb_sort(comb_sort):
#     """
#         Сортировка расческой
#         Сложность:
#             худшее: O(n^2)
#             среднее: O(n^2)
#             Лучшее: O(n)
#         Память: O(1)

#         Итерируемся от начала массива, сравнивая по 2 следующих элемента
#         тем самым вытесняя максимальный элемент за одну итерацию в самый конец
#     """
#     iters = 0
#     red_fact = len(data)
#     print(red_fact)
#     swapped = True
#     while red_fact > 1 or swapped:
#         red_fact = max(1, int(red_fact / 1.25))
        
#         swapped = False
#         iters_0 = 0
#         for i in range(len(data) - red_fact):
#             print(red_fact, iters_0)
#             iters_0+=1
#             j = i + red_fact
#             if data[i] > data[j]:
#                 data[i], data[j] = data[j], data[i]
#                 swapped = True
#         iters += 1

#     print('Comb iters: ', iters)
#     print('Comb data: ', data)


# def quick_sort(data, start, end):
#     if start >= end:
#         return

#     pivot = data[end]
#     j = start

#     for i in range(start, end):
#         if data[i] < pivot:
#             data[i], data[j] = data[j], data[i]
#             j += 1

#     data[j], data[end] = data[end], data[j]
#     quick_sort(data, start, j - 1)
#     quick_sort(data, j + 1, end)


# def insert_sort(data):
#     for i in range(len(data)):
#         j = i - 1
#         key = data[i]
#         while data[j] > key and j >= 0:
#             data[j + 1] = data[j]
#             j -= 1
#         data[j + 1] = key

#     print('Insert sort: ', data)


# def insert_sort_2(self):
#     for i in range(len(data)):
#         j = i - 1
#         val = data[i]
#         while val < data[j] and j >=0:
#             data[j + 1] = data[j]
#             j -= 1
#         data[j + 1] = val

#     print('Data: ', data)

# if __name__ == '__main__':
#     # data = generate_data(50)
#     data = [5,4,3,2,1]
#     print('Start: ' , data)
#     # bubble_sort(data.copy())
#     # shake_sort(data.copy())
#     # odd_even_sort(data.copy())
#     # comb_sort(data)
#     # quick_sort(data, 0, len(data) - 1)
#     # quick_sort_2(data, 0 ,len(data) - 1)
#     # insert_sort(data)
#     insert_sort_2(data)