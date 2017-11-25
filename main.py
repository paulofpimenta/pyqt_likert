import sys
from PyQt5.QtWidgets import  QApplication
from pyqt_likert.MainWindow import MainWindow

if __name__ == '__main__':
    qtApp = QApplication(sys.argv)
    #tbl = CreateTable()
    lk = MainWindow()
    lk.run()
    sys.exit(qtApp.exec_())
