"""
BMS GUI Version 6
Features:
*Update open file
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
from PySide6.QtWidgets import QMainWindow, QAbstractItemView, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QPushButton, QFileDialog, QComboBox, QSpacerItem, QLabel
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import QTimer, QDateTime

# Import UI file
from UI.BMS_GUI import Ui_MainWindow

# Import util functions
import util.util as util

# Import graph window
from BMS_plotWindow import plotWindow, zoomWindow, loadGraphWindow

# Import pandas
import pandas as pd
import numpy as np


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
        self.setMinimumWidth(1200)

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

        # ===================Data used for GUI displaying====================
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

        # Raw data in integer form
        self.bccData = [0 for i in range(0,16)]

        # Initialisation of cell data
        for num in range(0, 14):
            self.cellData['voltage'].append(0)
            self.cellData['voltageStatus'].append(voltageStatus.DEFAULT)
            self.cellData['currentStatus'].append(currentStatus.DEFAULT)

        # ===================Data used for graph plotting and recording====================

        self.outputData = pd.DataFrame(
        columns=[
            'packVoltage','cellVoltage_1','cellVoltage_2','cellVoltage_3','cellVoltage_4',
            'cellVoltage_5', 'cellVoltage_6', 'cellVoltage_7', 'cellVoltage_8', 'cellVoltage_9',
            'cellVoltage_10','cellVoltage_11','cellVoltage_12','cellVoltage_13','cellVoltage_14',
            'ICTemperature','Date'])
        
        self.graphData = np.zeros((16,1))

        # ===================================================================

        # Initialisation of serial
        self.serial = serial.Serial()

        # Initialisation of graph window
        self.graphWindow = plotWindow()

        # Two timers
        self.timer = QTimer() # Timer for GUI data displaying
        self.timer2 = QTimer() # Timer for data plotting
        self.timer3 = QTimer() # Timer for data recoding

        # Initialisation of the GUI
        self.init()

        # Update threshold values
        self.voltageMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.voltageMiniLineEdit.textChanged.connect(self.updateThreshold)

        self.currentMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.currentMiniLineEdit.textChanged.connect(self.updateThreshold)

        self.tempMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.tempMiniLineEdit.textChanged.connect(self.updateThreshold)

# ===================Class initialisation====================

    def init(self):
        """GUI initialisation"""
        # Init graph page layout
        graphPageLayout = QVBoxLayout()
        plotButtonLayout = QHBoxLayout()

        # Add stop and start plotting button
        self.startPlotButton = QPushButton("Start Plotting")
        self.stopPlotButton = QPushButton("Stop Plotting")

        graphSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        zoomLabel = QLabel("Choose to zoom")

        # Add zoom item combo box
        self.zoomGraphComboBox = QComboBox()
        self.zoomGraphComboBox.addItem('Cell 1 Voltage')
        self.zoomGraphComboBox.addItem('Cell 2 Voltage')
        self.zoomGraphComboBox.addItem('Cell 3 Voltage')
        self.zoomGraphComboBox.addItem('Cell 4 Voltage')
        self.zoomGraphComboBox.addItem('Cell 5 Voltage')
        self.zoomGraphComboBox.addItem('Cell 6 Voltage')
        self.zoomGraphComboBox.addItem('Cell 7 Voltage')
        self.zoomGraphComboBox.addItem('Cell 8 Voltage')
        self.zoomGraphComboBox.addItem('Cell 9 Voltage')
        self.zoomGraphComboBox.addItem('Cell 10 Voltage')
        self.zoomGraphComboBox.addItem('Cell 11 Voltage')
        self.zoomGraphComboBox.addItem('Cell 12 Voltage')
        self.zoomGraphComboBox.addItem('Cell 13 Voltage')
        self.zoomGraphComboBox.addItem('Cell 14 Voltage')
        self.zoomGraphComboBox.addItem('Pack Voltage')
        self.zoomGraphComboBox.addItem('IC Temperature')

        self.zoomButton = QPushButton("Zoom Graph")

        # Set layouts
        plotButtonLayout.addWidget(self.startPlotButton)
        plotButtonLayout.addWidget(self.stopPlotButton)

        plotButtonLayout.addItem(graphSpacer)

        plotButtonLayout.addWidget(zoomLabel)
        plotButtonLayout.addWidget(self.zoomGraphComboBox)
        plotButtonLayout.addWidget(self.zoomButton)

        graphPageLayout.addWidget(self.graphWindow)

        # Init record button
        self.startRecordButton.setEnabled(False)
        self.stopRecordButton.setChecked(True)

        # Add print button
        self.printButton = QPushButton("Print Data")
        self.recordGroupBoxLayout.addWidget(self.printButton)

        # Add graph panels
        self.batteryData_3Layout.addLayout(graphPageLayout)
        self.batteryData_3Layout.addLayout(plotButtonLayout)
        
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

        # Set the port status to be unchanged
        self.portStatusDisplay.setEnabled(False)

        # Set threshold values
        self.currentMiniLineEdit.setText(str(self.currentThreshold[0]))
        self.currentMaxLineEdit.setText(str(self.currentThreshold[1]))

        self.voltageMiniLineEdit.setText(str(self.voltageThreshold[0]))
        self.voltageMaxLineEdit.setText(str(self.voltageThreshold[1]))

        self.tempMiniLineEdit.setText(str(self.tempThreshold[0]))
        self.tempMaxLineEdit.setText(str(self.tempThreshold[1]))

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

        # Connect plot button functions
        self.startPlotButton.clicked.connect(self.plotGraph)
        self.stopPlotButton.clicked.connect(self.stopPlotting)

        # Connect record button functions
        self.startRecordButton.toggled.connect(self.startRecording)
        self.stopRecordButton.toggled.connect(self.stopRecording)
        self.printButton.clicked.connect(self.printData)

        # Connect zoom button functions
        self.zoomButton.clicked.connect(self.zoomGraph)

        # Connect load button function
        self.loadingButton.clicked.connect(self.openFile)

# ===================Update threshold values====================

    def updateThreshold(self):
        """This function is used to update the threshold values"""
        self.currentThreshold = [int(self.currentMiniLineEdit.text()), int(
            self.currentMaxLineEdit.text())]
        print("Current threshold: ")
        print(self.currentThreshold)

        self.voltageThreshold = [int(self.voltageMiniLineEdit.text()), int(
            self.voltageMaxLineEdit.text())]

        print("Voltage threshold: ")
        print(self.voltageThreshold)
        
        self.tempThreshold = [int(self.tempMiniLineEdit.text()), int(
            self.tempMaxLineEdit.text())]
        
        print("Temperature threshold: ")
        print(self.tempThreshold)

# ===================Clear and reset data====================

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

        # Clear output data and graph data
        self.graphData = np.zeros((16,1))
        self.outputData =self.outputData.drop(index = self.outputData.index)
        self.updateGraphData()

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

# ===================Port configuration and communication====================

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
        print("Baud rate: " + str(self.serial.baudrate))

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
            self.startRecordButton.setEnabled(True)
        except:
            QMessageBox.critical(self, "COM error", "Please check COM port!")
            return None

        # Disable stop monitor if monitoring is started
        if self.serial.isOpen():
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.portStatusDisplay.setChecked(True)

        # Open the timer to receive data
        self.timer.timeout.connect(self.receiveData)

        # Set the timer for receiving
        self.timer.start(1)  # 1ms/T

    def stopMonitor(self):
        """Stop the monitoring process"""
        try:
            self.timer.stop()
            self.timer2.stop()
            self.stopRecordButton.setChecked(True) #Stop timer 3
            self.serial.close()
        except:
            QMessageBox.critical(self, "COM error", "COM close failed")

        self.startRecordButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.portStatusDisplay.setChecked(False)        

# ===================Data printing====================

    def startRecording(self):
        """Handler for start data recording"""
        # Detect port status
        self.timer3.timeout.connect(self.recordData)
        self.timer3.start(200)

    def stopRecording(self):
        """Handler for stop data recording"""
        self.timer3.stop()

    def recordData(self):
        """Handler for updating data"""
        # Update real time data
        if self.waitBits > 0:
            # Set time information
            timeInfo = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss.zzz")

            # Add realtime data
            index = self.outputData.index.size
            realTimeData = self.bccData
            realTimeData.append(timeInfo)
            self.outputData.loc[index] = realTimeData
            self.outputData.index = self.outputData.index + 1
            
    def printData(self):
        """Handler for saving data as zip"""
        self.stopRecordButton.setChecked(True)

        if self.serial.isOpen() and self.outputData.size > 2:
            fileName = QFileDialog.getSaveFileName(self, "Save File", ".", ("*.csv"))
            
            with open(fileName[0],'w') as f:
                self.outputData.to_csv(f, index=False, line_terminator='\n')
                f.close()
            
            self.outputData = self.outputData.drop(index = self.outputData.index)

        else:
            self.stopRecordButton.setChecked(True)
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')

# ===================Data graph plotting====================

    def updateGraphData(self):
        """Handler for updating curve data"""
        insertData = list(i / 1000000 for i in self.bccData)
        insertData[15] = insertData[15] * 100000

        insertData = np.array(insertData).reshape((16,1))

        self.graphData = np.append(self.graphData, insertData, axis = 1)

        for i in range(0,16):
            self.curveList[i].setData(self.graphData[i])
        
        self.graphWindow.setGraphs()

    def plotGraph(self):
        """Show cell status, pack status, IC temperature in a graph"""
        self.cellCurve1 = self.graphWindow.p0.plot() # plotDataItem
        self.cellCurve2 = self.graphWindow.p1.plot()
        self.cellCurve3 = self.graphWindow.p2.plot()
        self.cellCurve4 = self.graphWindow.p3.plot()

        self.cellCurve5 = self.graphWindow.p4.plot()
        self.cellCurve6 = self.graphWindow.p5.plot()
        self.cellCurve7 = self.graphWindow.p6.plot()
        self.cellCurve8 = self.graphWindow.p7.plot()
        
        self.cellCurve9 = self.graphWindow.p8.plot()
        self.cellCurve10 = self.graphWindow.p9.plot()
        self.cellCurve11 = self.graphWindow.p10.plot()
        self.cellCurve12 = self.graphWindow.p11.plot()

        self.cellCurve13 = self.graphWindow.p12.plot()
        self.cellCurve14 = self.graphWindow.p13.plot()
        
        self.packVoltageCurve = self.graphWindow.packVoltageP.plot()
        self.ICTempCurve = self.graphWindow.ICTempP.plot()

        self.curveList = [self.packVoltageCurve,
            self.cellCurve1, self.cellCurve2, self.cellCurve3,
            self.cellCurve4, self.cellCurve5, self.cellCurve6,
            self.cellCurve7, self.cellCurve8, self.cellCurve9,
            self.cellCurve10, self.cellCurve11, self.cellCurve12,
            self.cellCurve13, self.cellCurve14, self.ICTempCurve]

        if self.serial.isOpen():
            self.timer2.timeout.connect(self.updateGraphData)
            self.timer2.start(200)
        else:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')

    def stopPlotting(self):
        """Handler for stop plotting data"""
        if self.serial.isOpen():
            self.timer2.stop()
        else:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')
    
    def zoomGraph(self):
        """Handler for zooming graph"""
        zoomedGraph = self.zoomGraphComboBox.currentText()
        zoomedGraphDict = {
            'Cell 1 Voltage': 1,
            'Cell 2 Voltage': 2,
            'Cell 3 Voltage': 3,
            'Cell 4 Voltage': 4,
            'Cell 5 Voltage': 5,
            'Cell 6 Voltage': 6,
            'Cell 7 Voltage': 7,
            'Cell 8 Voltage': 8,
            'Cell 9 Voltage': 9,
            'Cell 10 Voltage': 10,
            'Cell 11 Voltage': 11,
            'Cell 12 Voltage': 12,
            'Cell 13 Voltage': 13,
            'Cell 14 Voltage': 14,
            'Pack Voltage': 0,
            'IC Temperature': 15
        }

        if self.graphData.shape[1] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox.currentText()

            if graphItemIndex < 15:
                yLabel = "Voltage (V)"
            else:
                yLabel = "Temperature (°C)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.graphData[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')

# ===================Read data====================

    def openFile(self):
        """Handler for opening file"""
        try:
            openFileName = QFileDialog.getOpenFileName(
                self, 'Choose a CSV file to open', '.', 'CSV file(*.csv)')

            readFile = pd.read_csv(openFileName[0])

            if readFile.shape[1] > 2:
                loadWindow = loadGraphWindow()
                loadWindow.loadGraphData(readFile)
                loadWindow.exec()
            else:
                QMessageBox.critical(
                    self, 'Data error', 'No curve data, please check file')
        except:
            pass

# ===================Status display====================

    def displayCellStatus(self, batteryNumber):
        """Show cell status through a pop-up window"""
        currentStatus = self.cellData['currentStatus'][batteryNumber].value
        voltageStatus = self.cellData['voltageStatus'][batteryNumber].value

        message = "Cell Current Status: %s\nCell Voltage Status: %s" % (
            currentStatus, voltageStatus)

        QMessageBox.about(self, "Cell %s" % str(
            batteryNumber+1) + " Status", message)

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

# ===================GUI pop-up dialogues====================

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

# ===================Serial data receiving and updating====================

    def updateData(self):
        """This function is used to update the data as well as the status"""
        # Update data and status
        self.packData['voltage'] = self.bccData[0] / 1000
        if self.packData['voltage'] > self.packVoltageThreshold[1]:
            self.packData['voltageStatus'] = voltageStatus.OVERVOLTAGE
        elif self.packData['voltage'] < self.packVoltageThreshold[0]:
            self.packData['voltageStatus'] = voltageStatus.UNDERVOLTAGE
        else:
            self.packData['voltageStatus'] = voltageStatus.DEFAULT

        for i in range(0, 14):
            self.cellData['voltage'][i] = self.bccData[i+1] / 1000
            if self.cellData['voltage'][i] > self.voltageThreshold[1]:
                self.cellData['voltageStatus'][i] = voltageStatus.OVERVOLTAGE
            elif self.cellData['voltage'][i] < self.voltageThreshold[0]:
                self.cellData['voltageStatus'][i] = voltageStatus.UNDERVOLTAGE
            else:
                self.cellData['voltageStatus'][i] = voltageStatus.DEFAULT

        self.ICData['temp'] = self.bccData[15] / 10
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
        try:
            # Get the data bits in waiting
            self.waitBits = self.serial.in_waiting

            # Wait and receive the data again to avoid error
            if self.waitBits > 0:
                time.sleep(0.1)
                self.waitBits = self.serial.in_waiting
        except:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')
            self.close()
            return None

        if self.waitBits > 0:
            # Read data from COM port
            bccRawData = self.serial.read(self.waitBits)

            # Transfer the byte data to UART data list
            dataList = list(hex(data) for data in list(bccRawData))

            # Filter out incorrect inputs
            if len(dataList) == 64:
                self.bccData = util.listData2strData(dataList)
                self.updateData()
                self.updateGUIData()
            else:
                pass
        else:
            pass

# ===================Main====================

if __name__ == "__main__":
    application = QApplication(sys.argv)
    application.setStyle('Fusion')
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
