from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QDesktopWidget

from PyQt5.QtCore import Qt
from xlrd import open_workbook


class Table(QTableWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Table view")
        # self.setGeometry(30, 30, 500, 500)
        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.setSortingEnabled(False)
        self.setAlternatingRowColors(True)

    def fillTable(self, workbook):
        # for sheet in workbook.sheets():
        sheet = workbook.sheet_by_index(0)
        print('Sheet:' + sheet.name)
        self.setRowCount(sheet.nrows - 1)
        self.setColumnCount(sheet.ncols)

        for col in range(sheet.ncols):
            colLabel = sheet.cell(0, col).value
            print(colLabel)
            self.setHorizontalHeaderItem(col, QTableWidgetItem(colLabel))
            # Start from line 1
            for row in range(1, sheet.nrows):
                value = sheet.cell(row, col).value
                self.setItem(row - 1, col, QTableWidgetItem(value))
                try:
                    value = str(int(value))
                    self.setItem(row - 1, col, QTableWidgetItem(value))
                except:
                    pass

    def centerTable(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
