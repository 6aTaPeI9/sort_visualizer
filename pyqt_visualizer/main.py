import math
import time
import random

from command_helper import BarCommand
from pyqt_visualizer import QBarWidget, constants
from alghoritms.algoritms import Alghoritm
from PyQt5.QtWidgets import (QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QStackedLayout, QGridLayout, QPushButton, QSlider, QLabel, QCheckBox)
from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot, QThread, QTimer
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPalette


class WorkerThread(QObject):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        while True:
            self.signal.emit()
            time.sleep(0.005)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(constants.DEF_WIDTH, constants.DEF_HEIGTH)
        self.bars = []
        self.selected_algh = {}
        self.Ended = False
        self.stoped = True
        self.count_bar_items = constants.DEF_BARS_COUNT
        self.setWindowTitle('Sort alghoritms')
        self.InitWindowGrid()
        self.show()


    def InitWindowGrid(self):
        # self.worker = WorkerThread()
        # self.workerThread = QThread()
        # self.workerThread.started.connect(self.worker.run)
        # self.worker.signal.connect(self.signal)
        # self.worker.moveToThread(self.workerThread)
        # self.workerThread.start()

        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(constants.DEF_TIMEOUT / 100)
        self.timer.timeout.connect(self.signal)

        h_layout_main = QHBoxLayout()
        h_right_layout = QHBoxLayout()
        v_right_layout = QVBoxLayout() # правый макет с элементами управления

        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.start_timer)

        stop_button = QPushButton('Stop', self)
        stop_button.clicked.connect(self.stop_timer)

        h_right_layout.addWidget(start_button)
        h_right_layout.addWidget(stop_button)

        gr_layout = QGridLayout()
        gr_layout.setSpacing(20)
        gr_layout.addWidget(QWidget())

        self.lcd = QLabel(f'Кол-во эл.: {self.count_bar_items}', self)
        self.lcd.setStyleSheet('color: white')

        self.lb_speed = QLabel(f'Шаг каждые: {constants.DEF_TIMEOUT / 1000}(мс)')
        self.lb_speed.setStyleSheet('color: white')

        sld = QSlider(Qt.Horizontal, self)
        sld.valueChanged.connect(self.slider_value_changed)
        sld.setMinimum(1)
        sld.setMaximum(1000)
        sld.setSingleStep(1)
        sld.setValue(100)

        sld_speed = QSlider(Qt.Horizontal, self)
        sld_speed.valueChanged.connect(self.set_timer_interval)
        sld_speed.setMinimum(1)
        sld_speed.setMaximum(100000)
        sld_speed.setSingleStep(1)
        sld_speed.setValue(constants.DEF_TIMEOUT)

        v_right_layout.addLayout(h_right_layout)
        v_right_layout.addWidget(self.lcd)
        v_right_layout.addWidget(sld)

        q_grid_boxes = QGridLayout()
        row, col = 0, 0
        for i, sub_class in enumerate(self.get_alghoritms()):
            ch_box = QCheckBox(sub_class.NAME, self)
            ch_box.setStyleSheet('color: white')
            self.selected_algh[sub_class.NAME] = False
            ch_box.stateChanged.connect(self.add_q_box_signal(i, sub_class.NAME))

            if col >= 2:
                row += 1
                col = 0
            q_grid_boxes.addWidget(ch_box, row, col)
            col += 1

        v_right_layout.addLayout(q_grid_boxes)
        v_right_layout.addWidget(self.lb_speed)
        v_right_layout.addWidget(sld_speed)
        v_right_layout.addWidget(QWidget(), 5)


        h_layout_main.addLayout(gr_layout, 5)
        h_layout_main.addLayout(v_right_layout, 1)

        widget = QWidget()
        palette = widget.palette()
        widget.setAutoFillBackground(True)
        palette.setColor(widget.backgroundRole(), Qt.black)
        widget.setPalette(palette)
        widget.setLayout(h_layout_main)
        self.main_layout = gr_layout
        self.setCentralWidget(widget)


    def add_q_box_signal(self, i: int, name):
        """
            Метод генерирует методы для колбека от чекбоксов
        """
        def q_box_changed(checked, name: str = name):
            self.selected_algh[name] = bool(checked)

        q_box_changed.__name__ = f'q_box_changed{i}'
        setattr(self, q_box_changed.__name__, q_box_changed)
        return getattr(self, q_box_changed.__name__)


    def get_alghoritms(self, names: list = None) -> list:
        """
            Метод возвращает все унаследованные классы от класса Alghoritm.
            :param name: список значений атрибута NAME для которых нужно вернуть их классы
        """
        sub_classes = Alghoritm.__subclasses__()

        if not names:
            return sub_classes

        res = []
        for sub_class in Alghoritm.__subclasses__():
            if not hasattr(sub_class, 'NAME'):
                continue

            if sub_class.NAME in names:
                res.append(sub_class)

        return res


    def set_timer_interval(self, value):
        """
            Метод получает текущее положение ползунка и устанавливает
            интервал для таймера
        """
        value = round(value / 100, 2)
        self.timer.start(value)
        self.lb_speed.setText(f'Шаг каждые: {value}(мс.)')
        self.lb_speed.adjustSize()


    def slider_value_changed(self, value):
        """
            Метод получает текущее значение ползунка, устанавливает
            требуемое кол-во колонов в гистограмме и обновляет лейбл.
        """
        self.count_bar_items = value
        self.lcd.setText(f'Кол-во эл.: {value}')
        self.lcd.adjustSize()


    def start_timer(self):
        """
            Метод возобнавляет визуалицаю сортировки.
            Если визуализация уже была завершена, метод запустит ее заново.
        """
        if not self.stoped or self.Ended:
            self.signal(drop_iter=True)
            self.clear_bars()
            self.create_bars()

        self.stoped = False
        self.Ended = False
        self.timer.start()


    def stop_timer(self):
        """
            Метод приостанавливает визуализацию сортировки.
        """
        self.stoped = True
        self.timer.stop()


    def signal(self, iter_index = [0], drop_iter: bool = False):
        """
            Метод получает сигнал из таймера и перерисовывает все гистограммы.
        """
        if drop_iter:
            iter_index[0] = 0
            return

        all_ended = True
        for bar in self.bars:

            if bar.get('End'):
                continue

            all_ended = False

            algh_obj = bar.get('Algh')
            selected = algh_obj.get_pos_history(iter_index[0])
            bar_cont = bar.get('QBar')

            if not selected:
                bar['End'] = True
                continue

            if iter_index[0] != 0:
                prev_pos = algh_obj.get_pos_history(iter_index[0] - 1)
                if prev_pos:
                    BarCommand.execute_command(
                        'Colorized',
                        bar_cont,
                        *prev_pos.get('Position'),
                        color=Qt.white
                    )

            BarCommand.execute_command(
                selected.get('Command'),
                bar_cont,
                *selected.get('Position'),
                color=Qt.red
            )
            bar_cont.total_count = iter_index[0]
            bar_cont.update()

        if all_ended:
            self.Ended = True
            iter_index[0] = 0
        else:
            iter_index[0] = iter_index[0] + 1

        return


    def generate_data_set(self, max: int, len: int) -> list:
        """
            Метод генерирует список случайных чисел.
            :param max: максимальное значение для снегерированных числе
            :param len: кол-во чисел
        """
        return [random.randint(0, max) for i in range(0, len)]


    def clear_bars(self):
        """
            Метод очищает основной макет от всех виджетов, для последующей перерисовки
        """
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)


    def create_bars(self) -> None:
        """
            Метод заполняет поле self.bars связями QBarWidger и экзепляра
            алгоритма сортировки.
        """
        self.bars.clear()
        no_one_bar = True

        subclasses = Alghoritm.__subclasses__()

        frame_pos = math.log2(len(subclasses)) or 1
        data_set = self.generate_data_set(99, self.count_bar_items)
        row, col = 0, 0
        for alghoritm in subclasses:
            if not self.selected_algh.get(alghoritm.NAME):
                continue

            bar = QBarWidget.QBar(data_set.copy())
            self.main_layout.addWidget(bar, row, col)

            alghoritm = alghoritm(data_set.copy())

            col += 1
            if col >= frame_pos:
                col = 0
                row += 1

            self.bars.append({
                'QBar': bar,
                'Algh': alghoritm
            })

            no_one_bar = False

        if no_one_bar:
            self.main_layout.addWidget(QWidget())
