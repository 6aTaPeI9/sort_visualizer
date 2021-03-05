# -*- coding: utf-8 -*-
"""
    Модуль содрежит реализацию веджета для графика
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont, QColor


class Bar:
    def __init__(self, height: int, color = Qt.white):
        self._height = height
        self.color = color

    def set_height(self, new_height: int):
        self._height = new_height

    def set_color(self, new_color: int):
        self.color = new_color


class QBar(QWidget):
    def __init__(self, bars: list, titile = 'test'):
        super().__init__()
        self.bars = []
        self.titile = titile
        self.padding = 0.1
        self.total_count = 0

        for bar in bars:
            self.bars.append(Bar(bar))


    def __getitem__(self, index):
        return self.bars[index]


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawWdiget(qp)
        qp.end()


    def drawWdiget(self, qp):
        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.gray)
        qp.setBrush(Qt.white)

        size = self.size()
        width = size.width()
        height = size.height()
        spacing = width / 100
        bar_width = (width - spacing * 2) / len(self.bars)
        text_space = width / 10

        qp.drawLine(0, 0, 0, height)
        qp.drawLine(0, 0, (width / 2) - text_space, 0)
        qp.drawLine((width / 2) + text_space, 0, width, 0)
        qp.drawLine(width, height, 0, height)
        qp.drawLine(width, height, width, 0)

        for x, bar in enumerate(self.bars):
            qp.setBrush(bar.color)
            qp.drawRect(
                spacing + bar_width * x,
                height - bar._height,
                bar_width - self.padding,
                height - self.padding
            )

        qp.drawText((width / 2) + (text_space / 6), 7 , self.titile)
        qp.drawText(width / 25, height / 10 , f'Total operations: {self.total_count}')

        return
