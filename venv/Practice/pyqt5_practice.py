"""
    progressbar와 dialog를 응용하여
    데이터를 읽어오는 동안
    dialog를 만들어 progress를 보여주고 끝나면 dialog를 끄도록 구현
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ProgressDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Progress Dialog')

        self.setWindowModality(Qt.NonModal)

        self.btnDialog = QPushButton("Close", self)
        self.btnDialog.move(100, 100)
        self.btnDialog.clicked.connect(self.dialog_close)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btnDialog.hide()

    def dialog_close(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 300)

        self.setWindowTitle('Status Window')

        self.button = QPushButton('Dialog Button', self)
        self.button.clicked.connect(self.dialog_open)
        self.button.setGeometry(10, 10, 200, 50)

        self.timer = QBasicTimer()
        self.step = 0

    def dialog_open(self):
        self.dialog = ProgressDialog()

        self.timer.start(100, self)
        self.dialog.show()

        self.dialog.exec_()

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.step >= 100:
            self.timer.stop()
            self.dialog.btnDialog.show()
            return

        self.step += 1
        self.dialog.pbar.setValue(self.step)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
