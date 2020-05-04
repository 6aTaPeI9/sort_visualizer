from functools import lru_cache

class Alghoritm:
    def get_pos_history(self, iteratin_index: int):
        raise NotImplementedError('Метод get_pos_history не реализован.')


class LineSort(Alghoritm):
    def __init__(self, data: list):
        print('Инициализая линейной сортировки')
        self.name = 'Line Sort'
        self.data = data
        self.end = False
        self.algh_gen = self.algh()

    def algh(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                yield {
                    'Position': (i, j),
                    'Command': 'Colorized'
                }

                if self.data[i] < self.data[j]:
                    yield {
                        'Position': (i, j),
                        'Command': 'Swap'
                    }
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                else:
                    continue

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