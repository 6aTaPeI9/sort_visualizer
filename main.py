import sys
from PyQt5.QtWidgets import QApplication
from visualizer.main import MainWindow

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec())