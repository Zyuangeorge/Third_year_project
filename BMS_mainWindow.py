# Import built-in functions
import sys

# Import enum
from enum import Enum

# Import PyQt widgets: PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

# Import UI file
from BMS_GUI import Ui_MainWindow


class batteryStatus(Enum):
    DEFAULT = "DEFAULT"
    UNDERVOLTAGE = "UNDERVOLTAGE"
    OVERVOLTAGE = "OVERVOLTAGE"
    UNDERCURRENT = "UNDERCURRENT"
    OVERCURRENT = "OVERCURRENT"
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

        # Status button list
        self.cellStatusButtonList = [
            self.Cell1StatusDisplay, self.Cell2StatusDisplay, self.Cell3StatusDisplay,
            self.Cell4StatusDisplay, self.Cell5StatusDisplay, self.Cell6StatusDisplay,
            self.Cell7StatusDisplay, self.Cell8StatusDisplay, self.Cell9StatusDisplay,
            self.Cell10StatusDisplay, self.Cell11StatusDisplay, self.Cell12StatusDisplay,
            self.Cell13StatusDisplay, self.Cell14StatusDisplay,
        ]

        # Pack data
        self.packData = {'voltage': 0, 'current': 0,
                         'status': batteryStatus.DEFAULT}

        # IC data
        self.ICData = {'temp':0, 'status':batteryStatus.DEFAULT}

        # Cell data
        self.cellData = {'voltage': [], 'status': []}

        # Init cellData
        for num in range(0, 14):
            self.cellData['voltage'].append(0)
            self.cellData['status'].append(batteryStatus.DEFAULT)

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
        for cellStatus in self.cellData['status']:
            cellStatus = batteryStatus.DEFAULT

        # Clear pack data
        self.packData['voltage'] = 0
        self.packData['current'] = 0
        self.packData['status'] = batteryStatus.DEFAULT
        self.packVoltageLineEdit.setText((str)(self.packData['voltage']))
        self.packCurrentLineEdit.setText((str)(self.packData['current']))

        # Clear pack status
        self.packStatusDisplay.setText((str)(self.packData['status'].value))
        self.ICStatusDisplay.setText((str)(self.ICData['status'].value))

        # Clear IC temp data
        self.ICTempLineEdit.setText((str)(self.ICData['temp']))


# Main
if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
