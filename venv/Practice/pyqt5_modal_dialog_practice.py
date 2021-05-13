"""
    QDialog 연습
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 300)

        self.setWindowTitle('Status Window')

        self.button = QPushButton('Dialog Button', self)
        self.button.clicked.connect(self.dialog_open)
        self.button.setGeometry(10, 10, 200, 50)

        self.dialog = QDialog()

    def dialog_open(self):
        btnDialog = QPushButton("OK", self.dialog)
        btnDialog.move(100, 100)
        btnDialog.clicked.connect(self.dialog_close)

        self.dialog.setWindowTitle('Dialog')

        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()

    def dialog_close(self):
        self.dialog.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())