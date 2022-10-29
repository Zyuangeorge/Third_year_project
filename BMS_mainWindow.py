# Import built-in functions
import sys

# Import serial library
import serial
import serial.tools.list_ports

# Import time
import time

# Import enum
from enum import Enum

# Import PyQt widgets: PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

# Import UI file
from BMS_GUI import Ui_MainWindow

# Import utility functions
import util


class voltageStatus(Enum):
    DEFAULT = "NORMAL"
    UNDERVOLTAGE = "UNDERVOLTAGE"
    OVERVOLTAGE = "OVERVOLTAGE"


class currentStatus(Enum):
    DEFAULT = "NORMAL"
    UNDERCURRENT = "UNDERCURRENT"
    OVERCURRENT = "OVERCURRENT"


class tempStatus(Enum):
    DEFAULT = "NORMAL"
    UNDERTEMPERATURE = "UNDERTEMPERATURE"
    OVERTEMPERATURE = "OVERTEMPERATURE"


class mainWindow(QMainWindow, Ui_MainWindow):
    """Main window widget for BMS GUI"""

    def __init__(self):
        super(mainWindow, self).__init__()

        # Display UI
        self.setupUi(self)

        # Set up window logo and disable window size modification
        self.setWindowIcon(QIcon("sheffield_logo.jpg"))
        self.setFixedSize(self.width(), self.height())

        # Threshold variables
        self.currentThreshold = [0, 1600]
        self.voltageThreshold = [3000, 3700]
        self.tempThreshold = [35, 105]
        self.packVoltageThreshold = [i * 14 for i in self.voltageThreshold]

        # Status button list
        self.statusButtonList = [
            self.Cell1StatusDisplay, self.Cell2StatusDisplay, self.Cell3StatusDisplay,
            self.Cell4StatusDisplay, self.Cell5StatusDisplay, self.Cell6StatusDisplay,
            self.Cell7StatusDisplay, self.Cell8StatusDisplay, self.Cell9StatusDisplay,
            self.Cell10StatusDisplay, self.Cell11StatusDisplay, self.Cell12StatusDisplay,
            self.Cell13StatusDisplay, self.Cell14StatusDisplay,
        ]

        # Pack data
        self.packData = {'voltage': 0, 'current': 0,
                         'voltageStatus': voltageStatus.DEFAULT,
                         'currentStatus': currentStatus.DEFAULT}

        # IC data
        self.ICData = {'temp': 0,
                       'tempStatus': tempStatus.DEFAULT}

        # Cell data
        self.cellData = {'voltage': [],
                         'voltageStatus': [], 'currentStatus': []}

        # Initialisation of cell data
        for num in range(0, 14):
            self.cellData['voltage'].append(0)
            self.cellData['voltageStatus'].append(voltageStatus.DEFAULT)
            self.cellData['currentStatus'].append(currentStatus.DEFAULT)

        # Initialisation of serial
        self.serial = serial.Serial()
        self.checkPort()

        # Initialisation of the GUI
        self.init()

    def init(self):
        """GUI initialisation"""
        # Disable the change of the table item
        self.voltageTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set the stop monitoring button to close
        self.stopButton.setEnabled(False)

        # Set threshold values
        self.currentMiniLineEdit.setText((str)(self.currentThreshold[0]))
        self.currentMaxLineEdit.setText((str)(self.currentThreshold[1]))

        self.voltageMiniLineEdit.setText((str)(self.voltageThreshold[0]))
        self.voltageMaxLineEdit.setText((str)(self.voltageThreshold[1]))

        self.tempMiniLineEdit.setText((str)(self.tempThreshold[0]))
        self.tempMaxLineEdit.setText((str)(self.tempThreshold[1]))

        # Clear cell voltage
        self.voltageTable.clearContents()
        for num in range(0, 14):
            self.cellData['voltage'][num] = 0
            self.voltageTable.setItem(num, 0, QTableWidgetItem(
                (str)(self.cellData['voltage'][num])))
            self.voltageTable.setItem(num, 1, QTableWidgetItem('mV'))

        # Clear cell status
        for cellStatus in self.cellData['voltageStatus']:
            cellStatus = voltageStatus.DEFAULT
        for cellStatus in self.cellData['currentStatus']:
            cellStatus = currentStatus.DEFAULT

        # Clear pack data
        self.packData['voltage'] = 0
        self.packData['current'] = 0
        self.packVoltageLineEdit.setText((str)(self.packData['voltage']))
        self.packCurrentLineEdit.setText((str)(self.packData['current']))

        # Clear pack status
        self.packData['voltageStatus'] = voltageStatus.DEFAULT
        self.packData['currentStatus'] = currentStatus.DEFAULT
        self.packStatusDisplay.setText(
            (str)(self.packData['voltageStatus'].value))

        # Clear IC status
        self.ICData['status'] = tempStatus.DEFAULT
        self.ICStatusDisplay.setText((str)(self.ICData['status'].value))

        # Clear IC temp data
        self.ICData['temp'] = 0
        self.ICTempLineEdit.setText((str)(self.ICData['temp']))

        # Clear port status
        self.portStatusDisplay.setChecked(False)
        self.portStatusDisplay.setEnabled(False)

        # Connect serial button functions
        self.detectPortButton.clicked.connect(self.checkPort)
        self.startButton.clicked.connect(self.startMonitor)
        self.stopButton.clicked.connect(self.stopMonitor)

        # Connect cell state display
        self.Cell1StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell1StatusDisplay)))
        self.Cell2StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell2StatusDisplay)))
        self.Cell3StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell3StatusDisplay)))
        self.Cell4StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell4StatusDisplay)))
        self.Cell5StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell5StatusDisplay)))
        self.Cell6StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell6StatusDisplay)))
        self.Cell7StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell7StatusDisplay)))
        self.Cell8StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell8StatusDisplay)))
        self.Cell9StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell9StatusDisplay)))
        self.Cell10StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell10StatusDisplay)))
        self.Cell11StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell11StatusDisplay)))
        self.Cell12StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell12StatusDisplay)))
        self.Cell13StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell13StatusDisplay)))
        self.Cell14StatusDisplay.clicked.connect(lambda: self.displayCellStatus(
            self.statusButtonList.index(self.Cell14StatusDisplay)))

    def checkPort(self):
        """Check the connected ports"""
        self.portsDict = {}
        ports = serial.tools.list_ports.comports()

        self.portComboBox.clear()
        for port in ports:
            self.portsDict[(str)(port[0])] = (str)(port[1])
            self.portComboBox.addItem(port[0])

        if len(self.portsDict) == 0:
            self.portComboBox.addItem("NULL")

    def startMonitor(self):
        """Start the monitor process"""
        # Set COM port
        self.serial.port = self.portComboBox.currentText()

        # Set Baud rate
        self.serial.baudrate = (int)(self.baudRateComboBox.currentText())

        # Set Parity
        parity = self.parityComboBox.currentText()
        parityDict = {
            'None': serial.PARITY_NONE,
            'Odd': serial.PARITY_ODD,
            'Even': serial.PARITY_EVEN,
        }
        self.serial.parity = parityDict.get(parity)

        # Set Data bits
        dataBits = self.dataBitsComboBox.currentText()
        dataBitsDict = {
            '5': serial.FIVEBITS,
            '6': serial.SIXBITS,
            '7': serial.SEVENBITS,
            '8': serial.EIGHTBITS
        }
        self.serial.bytesize = dataBitsDict.get(dataBits)

        # Set Stop bits
        stopBits = self.stopBitsComboBox.currentText()
        stopBitsDict = {
            '1': serial.STOPBITS_ONE,
            '2': serial.STOPBITS_TWO
        }
        self.serial.stopbits = stopBitsDict.get(stopBits)

        # Test port
        try:
            time.sleep(0.1)
            self.serial.open()
        except:
            QMessageBox.critical(self, "COM error", "Please check COM port!")
            return None

        # Disable stop monitor if monitoring is started
        if self.serial.isOpen():
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.portStatusDisplay.setChecked(True)

        # Open the timer to receive data
        self.timer = QTimer()
        # self.timer.timeout.connect(self.receiveData)

        # Set the timer for receiving
        self.timer.start(1)  # 1ms/T

    def stopMonitor(self):
        try:
            self.timer.stop()
            self.serial.close()
        except:
            QMessageBox.critical(self, "COM error", "COM close failed")
        
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def displayCellStatus(self, batteryNumber):
        currentStatus = self.cellData['currentStatus'][batteryNumber].value
        voltageStatus = self.cellData['voltageStatus'][batteryNumber].value

        message = "Cell Current Status: %s\nCell Voltage Status: %s" %(currentStatus, voltageStatus)

        QMessageBox.about(self, "Cell %s" % str(batteryNumber+1) + " Status", message)


# Main
if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
