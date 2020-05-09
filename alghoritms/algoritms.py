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
