# import sys
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton,\
    QDesktopWidget, QFileDialog, QComboBox, \
    QVBoxLayout, QHBoxLayout, QFormLayout, QMainWindow

from pyqt_likert.Table import Table
from pyqt_likert.Plot import initLikert
from xlrd import open_workbook


# Class definition
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.filePath = ""
        self.table = Table()
        self.statusBar().addWidget(QLabel("Ready"))

        self.initUI()

    def initUI(self):
        #self.setGeometry(300, 400, 600, 400)
        self.setWindowTitle('Antonio\'s likert scale bar plot generator')
        self.center()
        self.land_use = ['Agriculture', 'Forest', 'Settlement', 'Grassland']
        self.services = ['Food', 'Wood', 'Water Supply', 'Regulation', 'Air Quality', 'Scenic Beauty']
        self.social_variables = ['Gender', 'Age', 'Age class', 'Education', 'Activity']

        # Defining combo boxes
        self.cmbServices = QComboBox()
        self.cmbLandScape = QComboBox()
        self.cmbSocial = QComboBox()
        self.cmbServices.addItems(self.services)
        self.cmbLandScape.addItems(self.land_use)
        self.cmbSocial.addItems(self.social_variables)
        self.cmbServices.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.cmbLandScape.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.cmbSocial.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        # Defining labels:
        lblServices = QLabel('Select a service')
        lblLandScape = QLabel('Select a land scape')
        lblSocial = QLabel('Select a social variable')

        # Button definition
        self.btnOpen = QPushButton('Open', self)
        self.btnQuit = QPushButton('Quit', self)
        self.btnRun = QPushButton('Run', self)
        self.btnView = QPushButton('View table', self)
        self.btnView.setDisabled(True)
        self.btnRun.setDisabled(True)

        # Connecting slots
        self.btnOpen.setStatusTip('Open the excel File')
        self.btnQuit.setStatusTip('Quit')
        self.btnOpen.clicked.connect(self.showOpenFileDialog)
        self.btnView.clicked.connect(self.showTable)
        self.btnQuit.clicked.connect(self.quitApp)
        self.btnRun.clicked.connect(self.runPlot)

        # Defining table widget
        # Form layout for combos and labels
        self.combosLayout = QVBoxLayout()
        self.combosLayout.addWidget(lblServices)
        self.combosLayout.addWidget(self.cmbServices)
        self.combosLayout.addWidget(lblLandScape)
        self.combosLayout.addWidget(self.cmbLandScape)
        self.combosLayout.addWidget(lblSocial)
        self.combosLayout.addWidget(self.cmbSocial)
        self.combosLayout.addStretch()

        # Horizontal layout for buttons
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.btnOpen)
        self.buttonsLayout.addWidget(self.btnQuit)
        self.buttonsLayout.addWidget(self.btnView)
        self.buttonsLayout.addWidget(self.btnRun)
        self.buttonsLayout.addStretch()

        # Setting some space and putting layouts together
        self.mainLayout = QFormLayout()
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.addRow(self.combosLayout)
        self.mainLayout.addRow(self.buttonsLayout)

        # Creating a widget (for cental widget) and set the layout for the window
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.central_widget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr  .moveCenter(cp)
        self.move(qr.topLeft())

    def showOpenFileDialog(self):
        # For static function call
        # fileDialog = QFileDialog()
        filename = QFileDialog.getOpenFileName(None, 'Open file',
         'c:\\Users\\Elena Arsevska\\Dropbox\\R\\',"Excel files (*.xls *.xlsx)")
        if filename[0]:
            fullFilePath = filename[0]
            file = open(fullFilePath, 'r')
            self.statusBar().showMessage("Loaded file : " + fullFilePath)
            self.filePath = fullFilePath
            self.btnView.setEnabled(True)
            self.btnRun.setEnabled(True)
        if not filename[0]:
            print("empty")
            self.statusBar().showMessage("Ready")

    def showTable(self):
        workbook = open_workbook(self.filePath)
        print("FileTest name  : " + self.filePath)
        self.table.fillTable(workbook)
        self.table.centerTable()
        self.table.show()

    def runPlot(self):
        selectedService = self.cmbServices.currentIndex()
        selectedLandScape = self.cmbLandScape.currentIndex()
        selectedSocial = self.cmbSocial.currentIndex()
        print("FileTest name  : " + self.filePath +
              "\nService : " + str(selectedService) +
              "\nLandscape: " + str(selectedLandScape) +
              "\nSocial: " + str(selectedSocial))
        initLikert(selectedService,selectedLandScape,selectedSocial,self.filePath)


    # Only the active windows closes, not the whole program
    def quitApp(self):
        self.close()

    def run(self):
        self.show()

