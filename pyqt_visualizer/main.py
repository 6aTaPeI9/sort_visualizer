import math
import time
import random

from command_helper import BarCommand
from pyqt_visualizer import QBarWidget
from alghoritms.algoritms import Alghoritm
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QStackedLayout, QGridLayout, QPushButton
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
        self.setMinimumSize(900, 450)
        self.bars = []
        self.setWindowTitle('Test layouts')
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
        self.timer.setInterval(0.05)
        self.timer.timeout.connect(self.signal)
        self.timer.start()

        h_layout_main = QHBoxLayout()
        h_layout_chield = QHBoxLayout() # правый макет с элементами управления

        start_button = QPushButton()
        start_button.text = 'Start'
        start_button.clicked.connect(self.start_timer)

        stop_button = QPushButton()
        stop_button.text = 'Stop'
        stop_button.clicked.connect(self.stop_timer)

        h_layout_chield.addWidget(start_button)
        h_layout_chield.addWidget(stop_button)
        
        gr_layout = QGridLayout()
        gr_layout.setSpacing(20)

        h_layout_main.addLayout(gr_layout, 5)
        h_layout_main.addLayout(h_layout_chield, 1)
        self.create_bars(gr_layout)

        widget = QWidget()
        palette = widget.palette()
        widget.setAutoFillBackground(True)
        palette.setColor(widget.backgroundRole(), Qt.black)
        widget.setPalette(palette)
        widget.setLayout(h_layout_main)
        self.setCentralWidget(widget)


    def start_timer(self):
        self.timer.start()


    def stop_timer(self):
        self.timer.stop()


    def signal(self, iter_index = [0]):
        for bar in self.bars:
            algh_obj = bar.get('Algh')
            selected = algh_obj.get_pos_history(iter_index[0])
            bar_cont = bar.get('QBar')

            if not selected:
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

        iter_index[0] = iter_index[0] + 1
        return


    def generate_data_set(self, max, len):
        return [random.randint(0, max) for i in range(0, len)]


    def create_bars(self, layout):
        subclasses = Alghoritm.__subclasses__()

        frame_pos = math.log2(len(subclasses)) or 1
        data_set = self.generate_data_set(99, 50)
        row, col = 0, 0
        for alghoritm in subclasses:
            bar = QBarWidget.QBar(data_set.copy())
            layout.addWidget(bar, row, col)

            alghoritm = alghoritm(data_set.copy())

            col += 1
            if col >= frame_pos:
                col = 0
                row += 1

            self.bars.append({
                'QBar': bar,
                'Algh': alghoritm
            })
