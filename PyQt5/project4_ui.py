from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtCore import QIODevice
import json

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 511)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btnDisconnect = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnDisconnect.setObjectName("btnDisconnect")
        self.gridLayout.addWidget(self.btnDisconnect, 0, 3, 1, 1)
        self.btnRefreshPorts = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnRefreshPorts.setObjectName("btnRefreshPorts")
        self.gridLayout.addWidget(self.btnRefreshPorts, 0, 4, 1, 1)
        self.btnConnect = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnConnect.setObjectName("btnConnect")
        self.gridLayout.addWidget(self.btnConnect, 0, 2, 1, 1)
        self.lblComPort = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblComPort.setObjectName("lblComPort")
        self.gridLayout.addWidget(self.lblComPort, 0, 0, 1, 1)
        self.cbComPorts = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cbComPorts.setObjectName("cbComPorts")
        self.gridLayout.addWidget(self.cbComPorts, 0, 1, 1, 1)
        self.lblX = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblX.setFont(font)
        self.lblX.setObjectName("lblX")
        self.gridLayout.addWidget(self.lblX, 1, 0, 1, 1)
        self.lblY = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblY.setFont(font)
        self.lblY.setObjectName("lblY")
        self.gridLayout.addWidget(self.lblY, 1, 2, 1, 1)
        self.lblZ = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblZ.setFont(font)
        self.lblZ.setObjectName("lblZ")
        self.gridLayout.addWidget(self.lblZ, 1, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btnDisconnect.setEnabled(False)

        self.serialPort = QSerialPort()

        self.listSerialPorts()

        self.btnConnect.clicked.connect(self.connect_clicked)
        self.btnDisconnect.clicked.connect(self.disconnect_clicked)
        self.serialPort.readyRead.connect(self.receiveData)
        self.btnRefreshPorts.clicked.connect(self.refreshports_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Project 4 - Accelerometer"))
        self.btnDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.btnRefreshPorts.setText(_translate("MainWindow", "Refresh Ports"))
        self.btnConnect.setText(_translate("MainWindow", "Connect"))
        self.lblComPort.setText(_translate("MainWindow", "Com Ports:"))
        self.lblX.setText(_translate("MainWindow", "X: -"))
        self.lblY.setText(_translate("MainWindow", "Y: -"))
        self.lblZ.setText(_translate("MainWindow", "Z: -"))

    def listSerialPorts(self):
        serialPortInfo = QSerialPortInfo()
        for serialPort in serialPortInfo.availablePorts():
            self.cbComPorts.addItem(serialPort.portName())

    def refreshports_clicked(self):
        self.cbComPorts.clear()
        serialPortInfo = QSerialPortInfo()
        for serialPort in serialPortInfo.availablePorts():
            self.cbComPorts.addItem(serialPort.portName())


    def connect_clicked(self):
        self.serialPort.setPortName(self.cbComPorts.currentText())
        self.serialPort.setBaudRate(QSerialPort.Baud115200)
        self.serialPort.setDataBits(QSerialPort.Data8)
        self.serialPort.setParity(QSerialPort.NoParity)
        self.serialPort.setBaudRate(QSerialPort.Baud115200)
        self.serialPort.setStopBits(QSerialPort.OneStop)
        
        if not (self.serialPort.isOpen()):
            self.serialPort.open(QIODevice.ReadWrite)
            self.btnConnect.setStyleSheet("background-color : green; color : white;")
            self.btnConnect.setEnabled(False)
            self.btnRefreshPorts.setEnabled(False)
            self.btnDisconnect.setEnabled(True)
        else:
            self.btnConnect.setStyleSheet("background-color : red; color : white;")

    def disconnect_clicked(self):
        if (self.serialPort.isOpen()):
            self.serialPort.close()
            self.btnConnect.setStyleSheet("")
            self.btnConnect.setEnabled(True)
            self.btnRefreshPorts.setEnabled(True)
            self.btnDisconnect.setEnabled(False)

    def receiveData(self):
        jsonData = self.serialPort.readLine().data().decode()
        data = json.loads(jsonData)
        self.lblX.setText("X: " + str(data["X"]))
        self.lblY.setText("Y: " + str(data["Y"]))
        self.lblZ.setText("Z: " + str(data["Z"]))

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
