import math
import random
import typing
import constants
import matplotlib.pyplot as plt

from algoritms import Alghoritm
from collections import deque
from matplotlib import rc
from matplotlib import container
from matplotlib import animation

FIGURE = plt.figure()

class Frames:
    FRAMES = []
    DATA_LEN = 50

    @staticmethod
    def fill_axes():
        count_alg = Frames.get_count_algh()

        if not count_alg:
            return

        frame_size = math.log2(count_alg) or 1
        frame_size = (round(frame_size + 0.5), int(frame_size))
        data_set = Frames.generate_data_set()
        for indx, sub_class in enumerate(Frames.get_sub_classes()):
            axes = FIGURE.add_subplot(
                frame_size[0],
                frame_size[1],
                indx + 1
            ) # создаем форму графика

            axes.set_xmargin(constants.BAR_XMARGIN)
            axes.set(facecolor=constants.FACECOLOR)
            sub_class = sub_class(data_set.copy())
            bar_containter = axes.bar(
                list(range(0, Frames.DATA_LEN)),
                data_set.copy(),
                color=constants.BAR_COLOR,
                width=1
            )
            axes.set_title(sub_class.name, {'color': constants.BAR_COLOR})

            Frames.FRAMES.append({
                'BarCont': bar_containter,
                'Axes': axes,
                'Algh': sub_class
            })

            return [frame.get('Axes') for frame in Frames.FRAMES]

    @staticmethod
    def generate_data_set():
        return [random.randint(0, constants.MAX_HEIGHT) for i in range(0, Frames.DATA_LEN)]

    @staticmethod
    def get_count_algh():
        return len(Frames.get_sub_classes())

    @staticmethod
    def get_sub_classes():
        return Alghoritm.__subclasses__()

class BarCommand:

    @staticmethod
    def execute_command(
        command: str,
        bar_cont: container.BarContainer,
        *args,
        **kwargs
    ):
        COMMANDS = {
            'Swap': BarCommand.swap_bars,
            'Colorized': BarCommand.mark_bar_color
        }

        method = COMMANDS.get(command)

        if not method:
            Warning(f'Указанный метод {method} не реализован.')
            return

        return method(bar_cont, *args, **kwargs)

    @staticmethod
    def swap_bars(
        bar_cont: container.BarContainer,
        left_bar_index: int,
        right_bar_index: int,
        **kwargs
    ) -> None:
        temp_heigt = bar_cont[left_bar_index]._height
        bar_cont[left_bar_index].set_height(bar_cont[right_bar_index]._height)
        bar_cont[right_bar_index].set_height(temp_heigt)

    @staticmethod
    def mark_bar_color(bar_cont: container.BarContainer, *args, **kwargs):
        for i in [*args]:
            print({**kwargs}.get('color'))
            bar_cont[i].set_color({**kwargs}.get('color'))


def animations(main_figure: plt.Figure):
    def calc_next_frame(iter: int, iter_index = [0]):
        changed_axes = []
        for algh in Frames.FRAMES:
            algh_obj = algh.get('Algh')
            selected = algh_obj.get_pos_history(iter_index[0])
            bar_cont = algh.get('BarCont')

            if not selected:
                continue

            if iter_index[0] != 0:
                prev_pos = algh_obj.get_pos_history(iter_index[0] - 1)
                if prev_pos:
                    BarCommand.execute_command(
                        'Colorized',
                        bar_cont,
                        *prev_pos.get('Position'),
                        color=constants.BAR_COLOR
                    )

            BarCommand.execute_command(
                selected.get('Command'),
                bar_cont,
                *selected.get('Position'),
                color=constants.SELECTED_COLOR
            )
            changed_axes.append(algh.get('Axes'))

        iter_index[0] = iter_index[0] + 1
        # return changed_axes

    anim = animation.FuncAnimation(
        main_figure,
        calc_next_frame,
        init_func=Frames.fill_axes,
        repeat=True,
        blit=False,
        # blit=True
        interval=1
    )
    plt.show()


if __name__ == '__main__':
    FIGURE.canvas.toolbar.pack_forget()
    FIGURE.set(facecolor=constants.FACECOLOR)
    rc('axes', edgecolor=constants.BAR_BORDER_COLOR)
    animations(FIGURE)
