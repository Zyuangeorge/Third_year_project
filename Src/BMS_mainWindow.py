"""
BMS GUI Version 4
Features:
*Update UART transmission
"""
# Import functions in other folders
import sys
sys.path.append('.')

# Import serial library
import serial
import serial.tools.list_ports

# Import time
import time

# Import enum
from enum import Enum

# Import PyQt widgets: PySide6
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QApplication, QMessageBox
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import QTimer

# Import UI file
from UI.BMS_GUI import Ui_MainWindow

# Import util functions
import util.util as util


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
        self.setWindowIcon(QIcon("./UI/sheffield_logo.jpg"))
        self.setFixedSize(self.width(), self.height())

        # Threshold variables
        self.currentThreshold = [0, 1600]
        self.voltageThreshold = [2800, 4300]
        self.tempThreshold = [20, 105]
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

        # Initialisation of the GUI
        self.init()

        # Update threshold values
        self.voltageMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.voltageMiniLineEdit.textChanged.connect(self.updateThreshold)

        self.currentMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.currentMiniLineEdit.textChanged.connect(self.updateThreshold)

        self.tempMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.tempMiniLineEdit.textChanged.connect(self.updateThreshold)

    def updateThreshold(self):
        """This function is used to update the threshold values"""
        self.currentThreshold = [int(self.currentMiniLineEdit.text()), int(
            self.currentMaxLineEdit.text())]

        self.voltageThreshold = [int(self.voltageMiniLineEdit.text()), int(
            self.voltageMaxLineEdit.text())]

        self.tempThreshold = [int(self.tempMiniLineEdit.text()), int(
            self.tempMiniLineEdit.text())]

    def clearData(self):
        """Clear cell voltage, pack voltage & current and IC temperature"""
        # Clear cell voltage
        for num in range(0, 14):
            self.cellData['voltage'][num] = 0
            self.voltageTable.item(num, 0).setText(str(0))

        # Clear pack data
        self.packData['voltage'] = 0
        self.packData['current'] = 0
        self.packVoltageLineEdit.setText(str(self.packData['voltage']))
        self.packCurrentLineEdit.setText(str(self.packData['current']))

        # Clear IC temp data
        self.ICData['temp'] = 0
        self.ICTempLineEdit.setText(str(self.ICData['temp']))

        # Clear port status
        self.portStatusDisplay.setChecked(False)
        self.portStatusDisplay.setEnabled(False)

    def resetStatus(self):
        """Reset cell, pack and IC status as well as the button colours"""
        # Clear cell status
        for i in range(0, 14):
            self.cellData['voltageStatus'][i] = voltageStatus.DEFAULT
            self.cellData['currentStatus'][i] = currentStatus.DEFAULT

        for button in self.statusButtonList:
            button.setStyleSheet(
                "background-color: rgb(0, 255, 0)")

        # Clear pack status
        self.packData['voltageStatus'] = voltageStatus.DEFAULT
        self.packData['currentStatus'] = currentStatus.DEFAULT
        self.packVoltageStatusDisplay.setText(
            self.packData['voltageStatus'].value)
        self.packCurrentStatusDisplay.setText(
            self.packData['currentStatus'].value)
        self.packVoltageStatusDisplay.setStyleSheet(
            "background-color: rgb(0, 255, 0)")
        self.packCurrentStatusDisplay.setStyleSheet(
            "background-color: rgb(0, 255, 0)")

        # Clear IC status
        self.ICData['tempStatus'] = tempStatus.DEFAULT
        self.ICStatusDisplay.setText(self.ICData['tempStatus'].value)
        self.ICStatusDisplay.setStyleSheet(
            "background-color: rgb(0, 255, 0)")

    def init(self):
        """GUI initialisation"""
        # Set QLineEdit restrictions
        self.voltageMaxLineEdit.setValidator(QIntValidator())
        self.voltageMiniLineEdit.setValidator(QIntValidator())
        self.currentMaxLineEdit.setValidator(QIntValidator())
        self.currentMiniLineEdit.setValidator(QIntValidator())
        self.tempMaxLineEdit.setValidator(QIntValidator())
        self.tempMiniLineEdit.setValidator(QIntValidator())

        # Disable the change of the table item
        self.voltageTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set table item
        for num in range(0, 14):
            self.cellData['voltage'][num] = 0
            self.voltageTable.setItem(num, 0, QTableWidgetItem(
                str(self.cellData['voltage'][num])))
            self.voltageTable.setItem(num, 1, QTableWidgetItem('mV'))

        # Set the stop monitoring button to close
        self.stopButton.setEnabled(False)

        # Set threshold values
        self.currentMiniLineEdit.setText(str(self.currentThreshold[0]))
        self.currentMaxLineEdit.setText(str(self.currentThreshold[1]))

        self.voltageMiniLineEdit.setText(str(self.voltageThreshold[0]))
        self.voltageMaxLineEdit.setText(str(self.voltageThreshold[1]))

        self.tempMiniLineEdit.setText(str(self.tempThreshold[0]))
        self.tempMaxLineEdit.setText(str(self.tempThreshold[1]))

        self.clearData()
        self.resetStatus()

        # Connect serial button functions
        self.detectPortButton.clicked.connect(self.detectPort)
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

        # Connect help menu actions
        self.actionHelp.triggered.connect(self.helpAction)
        self.actionAbout.triggered.connect(self.aboutAction)

        # Connect setting menu actions
        self.actionConnect.triggered.connect(self.startMonitor)
        self.actionDetectPort.triggered.connect(self.detectPort)

        # Connect clear data button
        self.clearDataButton.clicked.connect(self.clearWarning)

        # Connect reset status button
        self.resetStatusButton.clicked.connect(self.resetStatus)

    def detectPort(self):
        """Check the connected ports"""
        self.portsDict = {}
        ports = serial.tools.list_ports.comports()

        self.portComboBox.clear()
        for port in ports:
            self.portsDict[str(port[0])] = str(port[1])
            self.portComboBox.addItem(port[0])

        if len(self.portsDict) == 0:
            self.portComboBox.addItem("NULL")
            QMessageBox.critical(self, "COM error", "COM detect failed")

    def startMonitor(self):
        """Start the monitor process"""
        # Set COM port
        self.serial.port = self.portComboBox.currentText()

        # Set Baud rate
        self.serial.baudrate = int(self.baudRateComboBox.currentText())
        print(self.serial.baudrate)

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
            '1':    serial.STOPBITS_ONE,
            '1.5':  serial.STOPBITS_ONE_POINT_FIVE,
            '2':    serial.STOPBITS_TWO
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
        self.timer.timeout.connect(self.receiveData)

        # Set the timer for receiving
        self.timer.start(1)  # 1ms/T

    def stopMonitor(self):
        """Stop the monitoring process"""
        try:
            self.timer.stop()
            self.serial.close()
        except:
            QMessageBox.critical(self, "COM error", "COM close failed")

        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.portStatusDisplay.setChecked(False)

    def displayCellStatus(self, batteryNumber):
        """Show cell status through a pop-up window"""
        currentStatus = self.cellData['currentStatus'][batteryNumber].value
        voltageStatus = self.cellData['voltageStatus'][batteryNumber].value

        message = "Cell Current Status: %s\nCell Voltage Status: %s" % (
            currentStatus, voltageStatus)

        QMessageBox.about(self, "Cell %s" % str(
            batteryNumber+1) + " Status", message)

    def helpAction(self):
        """User manual"""
        QMessageBox.about(self,
                          "Help",
                          "This GUI supports: \n\
            1. Change UART settings\n\
            2. Set threshold values\n\
            3. Display battery data and status\n\
            4. Display pack data and status\n\
            5. Display MC33771C temperature\n\n\
        Follow these steps to use this GUI: \n\
            1. Set UART configuration\n\
            2. Set threshold values\n\
            3. Start monitoring\n\
            4. Check data and status\n\
        *To check individual cell data, please click the cell button\n\
        **The button will turn red if there is a problem with the status")

    def aboutAction(self):
        """About this GUI"""
        QMessageBox.about(
            self, "About", "This GUI is built by Zhe Yuan, and it is used to monitor the battery cell data through MC33771C")

    def clearWarning(self):
        """Warn user for clearing data"""
        yesButton = QMessageBox.StandardButton.Yes
        noButton = QMessageBox.StandardButton.No

        msg = QMessageBox.warning(
            self, "Warning", "You are going to clear all the data!", yesButton, noButton)
        if msg == QMessageBox.Yes:
            self.clearData()

    def updateData(self, bccData):
        """This function is used to update the data as well as the status"""
        # Update data and status
        self.packData['voltage'] = bccData[0] / 1000
        if self.packData['voltage'] > self.packVoltageThreshold[1]:
            self.packData['voltageStatus'] = voltageStatus.OVERVOLTAGE
        elif self.packData['voltage'] < self.packVoltageThreshold[0]:
            self.packData['voltageStatus'] = voltageStatus.UNDERVOLTAGE
        else:
            self.packData['voltageStatus'] = voltageStatus.DEFAULT

        for i in range(0, 14):
            self.cellData['voltage'][i] = bccData[i+1] / 1000
            if self.cellData['voltage'][i] > self.voltageThreshold[1]:
                self.cellData['voltageStatus'][i] = voltageStatus.OVERVOLTAGE
            elif self.cellData['voltage'][i] < self.voltageThreshold[0]:
                self.cellData['voltageStatus'][i] = voltageStatus.UNDERVOLTAGE
            else:
                self.cellData['voltageStatus'][i] = voltageStatus.DEFAULT

        self.ICData['temp'] = bccData[15] / 10
        if self.ICData['temp'] > self.tempThreshold[1]:
            self.ICData['tempStatus'] = tempStatus.OVERTEMPERATURE
        elif self.ICData['temp'] < self.tempThreshold[0]:
            self.ICData['tempStatus'] = tempStatus.UNDERTEMPERATURE
        else:
            self.ICData['tempStatus'] = tempStatus.DEFAULT

    def receiveData(self):
        """Handler for receiving data"""
        bccRawData = []
        dataList = []
        bccData = []
        try:
            # Get the data bits in waiting
            waitBits = self.serial.in_waiting

            # Wait and receive the data again to avoid error
            if waitBits > 0:
                time.sleep(0.1)
                waitBits = self.serial.in_waiting
        except:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')
            self.close()
            return None

        if waitBits > 0:
            # Read data from COM port
            bccRawData = self.serial.read(waitBits)

            # Transfer the byte data to UART data list
            dataList = list(hex(data) for data in list(bccRawData))

            # Filter out incorrect inputs
            if len(dataList) == 64:
                bccData = util.listData2strData(dataList)
                self.updateData(bccData)
                self.updateGUIData()
            else:
                pass
        else:
            pass

    def updateGUIData(self):
        """This function is used to update GUI display"""
        # Update cell voltage data and status
        for i in range(0, 14):
            self.voltageTable.item(i, 0).setText(
                str(self.cellData['voltage'][i]))
            if self.cellData['voltageStatus'][i] == voltageStatus.OVERVOLTAGE or self.cellData['voltageStatus'][i] == voltageStatus.UNDERVOLTAGE:
                self.statusButtonList[i].setStyleSheet(
                    "background-color: rgb(255, 0, 0)")
            elif self.cellData['currentStatus'][i] == currentStatus.OVERCURRENT or self.cellData['currentStatus'][i] == currentStatus.UNDERCURRENT:
                self.statusButtonList[i].setStyleSheet(
                    "background-color: rgb(255, 0, 0)")
            else:
                pass

        # Update pack data and status
        self.packVoltageLineEdit.setText(str(self.packData['voltage']))
        self.packVoltageStatusDisplay.setText(
            self.packData['voltageStatus'].value)
        self.packCurrentLineEdit.setText(str(self.packData['current']))
        self.packCurrentStatusDisplay.setText(
            self.packData['currentStatus'].value)

        if self.packData['voltageStatus'] == voltageStatus.OVERVOLTAGE:
            self.packVoltageStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        elif self.packData['voltageStatus'] == voltageStatus.UNDERVOLTAGE:
            self.packVoltageStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        else:
            pass

        if self.packData['currentStatus'] == currentStatus.OVERCURRENT:
            self.packCurrentStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        elif self.packData['currentStatus'] == currentStatus.UNDERCURRENT:
            self.packCurrentStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        else:
            pass

        # Update IC data and status
        self.ICTempLineEdit.setText(str(self.ICData['temp']))
        self.ICStatusDisplay.setText(self.ICData['tempStatus'].value)
        if self.ICData['tempStatus'] == tempStatus.OVERTEMPERATURE:
            self.ICStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        elif self.ICData['tempStatus'] == tempStatus.UNDERTEMPERATURE:
            self.ICStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        else:
            pass


# Main
if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
