"""
BMS GUI Version 1.1.1
Features:
    Support PC, uC transmission

pipenv Install:
pyinstaller --add-data="sheffield_logo.png;img" -w -i guiLogo.ico --distpath Release/ --clean BMS_TYP.py
"""
# Import functions in other folders
import sys
import gc
import os
# Expend file path
sys.path.append('.')

# Import time for setting timer
import time
# Import enum to define status
from enum import Enum

# Import numpy for realtime plotting
import numpy as np
# Import pandas for data outputting
import pandas as pd
# Import pyserial for serial communication
import serial
import serial.tools.list_ports
# Import PyQt widgets: PySide6
from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox,
                               QFileDialog, QHBoxLayout, QLabel, QMainWindow,
                               QMessageBox, QPushButton, QSizePolicy,
                               QSpacerItem, QTableWidgetItem, QVBoxLayout)

# Import util functions
import util.util as util
# Import graph window
from BMS_plotWindow import loadGraphWindow, plotWindow, zoomWindow, SOCPlotWindow, SOHPlotWindow, CBPlotWindow
# Import UI file
from UI.BMS_GUI import Ui_MainWindow
# Import Plotly file
from Plotly_Src.cellDataPlot import cellDataPlotting

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
        self.setMinimumWidth(1100)

        # ===================Data used for GUI displaying====================

        # Threshold variables
        self.currentThreshold = [0, 1500]
        self.voltageThreshold = [1700, 2500]
        self.tempThreshold = [20, 105]
        self.packVoltageThreshold = [i * 14 for i in self.voltageThreshold]

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

        # Raw battery data in integer form
        self.bccData = [0 for _ in range(17)]

        # SOC and SOH data
        self.SOC_SOHData = [0 for _ in range(28)]

        # Balancing data
        self.CBData = [0 for _ in range(14)]

        # Initialisation of cell data
        for num in range(0, 14):
            self.cellData['voltage'].append(0)
            self.cellData['voltageStatus'].append(voltageStatus.DEFAULT)
            self.cellData['currentStatus'].append(currentStatus.DEFAULT)

        # Battery status flag
        self.statusUpdateFlag = [0 for _ in range(17)]

        # Output time interval
        self.outputTimeInterval = int(self.recordDoubleSpinBox.value() * 3600)

        # ===================Real time data====================

        self.outputData = np.zeros((1,59)).astype(np.int32)

        self.graphData = np.zeros((59,1)).astype(np.float16)

        self.xaxis = np.zeros(1).astype(np.float16)

        self.EFC_Data = 0

        # BMS command
        self.command = b'IDLE'

        # ===================GUI Widgets====================

        # Status button list
        self.statusButtonList = [
            self.Cell1StatusDisplay, self.Cell2StatusDisplay, self.Cell3StatusDisplay,
            self.Cell4StatusDisplay, self.Cell5StatusDisplay, self.Cell6StatusDisplay,
            self.Cell7StatusDisplay, self.Cell8StatusDisplay, self.Cell9StatusDisplay,
            self.Cell10StatusDisplay, self.Cell11StatusDisplay, self.Cell12StatusDisplay,
            self.Cell13StatusDisplay, self.Cell14StatusDisplay,
        ]

        # Initialisation of serial
        self.serial = serial.Serial()

        # Initialisation of graph window
        self.graphWindow = plotWindow()
        self.graphWindow_SOC = SOCPlotWindow()
        self.graphWindow_SOH = SOHPlotWindow()
        self.graphWindow_CB = CBPlotWindow()

        # Three timers
        self.timer = QTimer() # Timer for GUI data displaying
        self.timer2 = QTimer() # Timer for data plotting
        self.timer3 = QTimer() # Timer for data recoding

        # Initialisation of the GUI
        self.init()

# ===================Class initialisation====================

    def initGraphPage_1(self):
        # Init graph page layout
        graphPageLayout = QVBoxLayout()

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
        self.zoomGraphComboBox.addItem('Pack Current')
        self.zoomGraphComboBox.addItem('IC Temperature')

        self.zoomButton = QPushButton("Zoom Graph")

        graphPageLayout.addWidget(self.graphWindow)
        
        zoomLayout = QHBoxLayout()
        zoomLabel = QLabel("Choose to zoom")
        zoomLayout.addWidget(zoomLabel)
        zoomLayout.addWidget(self.zoomGraphComboBox)
        zoomLayout.addWidget(self.zoomButton)

        # Add graph panels
        self.batteryData_3Layout.addLayout(graphPageLayout)
        self.batteryData_3Layout.addLayout(zoomLayout)

    def initGraphPage_2(self):
        # Init graph page layout
        graphPageLayout = QVBoxLayout()
        graphPageLayout.addWidget(self.graphWindow_SOC)

        # Add zoom item combo box
        self.zoomGraphComboBox_2 = QComboBox()
        self.zoomGraphComboBox_2.addItem('Cell 1 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 2 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 3 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 4 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 5 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 6 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 7 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 8 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 9 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 10 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 11 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 12 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 13 SoC')
        self.zoomGraphComboBox_2.addItem('Cell 14 SoC')

        self.zoomButton_2 = QPushButton("Zoom Graph")
        
        zoomLayout = QHBoxLayout()
        zoomLabel = QLabel("Choose to zoom")
        zoomLayout.addWidget(zoomLabel)
        zoomLayout.addWidget(self.zoomGraphComboBox_2)
        zoomLayout.addWidget(self.zoomButton_2)

        # Add graph panels
        self.batteryData_4Layout.addLayout(graphPageLayout)
        self.batteryData_4Layout.addLayout(zoomLayout)

    def initGraphPage_3(self):
        # Init graph page layout
        graphPageLayout = QVBoxLayout()
        graphPageLayout.addWidget(self.graphWindow_SOH)

        # Add zoom item combo box
        self.zoomGraphComboBox_3 = QComboBox()
        self.zoomGraphComboBox_3.addItem('Cell 1 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 2 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 3 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 4 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 5 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 6 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 7 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 8 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 9 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 10 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 11 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 12 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 13 SoH')
        self.zoomGraphComboBox_3.addItem('Cell 14 SoH')

        self.zoomButton_3 = QPushButton("Zoom Graph")
        
        zoomLayout = QHBoxLayout()
        zoomLabel = QLabel("Choose to zoom")
        zoomLayout.addWidget(zoomLabel)
        zoomLayout.addWidget(self.zoomGraphComboBox_3)
        zoomLayout.addWidget(self.zoomButton_3)

        # Add graph panels
        self.batteryData_5Layout.addLayout(graphPageLayout)
        self.batteryData_5Layout.addLayout(zoomLayout)

    def initGraphPage_4(self):
        # Init graph page layout
        graphPageLayout = QVBoxLayout()
        graphPageLayout.addWidget(self.graphWindow_CB)

        # Add zoom item combo box
        self.zoomGraphComboBox_4 = QComboBox()
        self.zoomGraphComboBox_4.addItem('Cell 1 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 2 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 3 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 4 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 5 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 6 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 7 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 8 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 9 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 10 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 11 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 12 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 13 CB Control')
        self.zoomGraphComboBox_4.addItem('Cell 14 CB Control')

        self.zoomButton_4 = QPushButton("Zoom Graph")
        
        zoomLayout = QHBoxLayout()
        zoomLabel = QLabel("Choose to zoom")
        zoomLayout.addWidget(zoomLabel)
        zoomLayout.addWidget(self.zoomGraphComboBox_4)
        zoomLayout.addWidget(self.zoomButton_4)

        # Add graph panels
        self.cbVerticalLayout.addLayout(graphPageLayout)
        self.cbVerticalLayout.addLayout(zoomLayout)

    def init(self):
        """GUI initialisation"""
        self.initGraphPage_1()
        self.initGraphPage_2()
        self.initGraphPage_3()
        self.initGraphPage_4()

        # Init plot button
        plotButtonLayout = QHBoxLayout()

        # Add stop and start plotting button
        self.startPlotButton = QPushButton("Start Plotting")
        self.stopPlotButton = QPushButton("Stop Plotting")

        graphSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Set layouts
        plotButtonLayout.addItem(graphSpacer)
        plotButtonLayout.addWidget(self.startPlotButton)
        plotButtonLayout.addWidget(self.stopPlotButton)

        self.monitorGroupBoxLayout.addLayout(plotButtonLayout)

        # Init record button
        self.startRecordButton.setEnabled(False)
        self.stopRecordButton.setChecked(True)
        
        # Add Plotly button
        self.plotlyButton = QPushButton("Plot by Plotly")
        self.verticalLayout_2.addWidget(self.plotlyButton)

        # Set QLineEdit restrictions
        self.voltageMaxLineEdit.setValidator(QIntValidator(0,2400))
        self.voltageMiniLineEdit.setValidator(QIntValidator(0,2400))
        self.currentMaxLineEdit.setValidator(QIntValidator(0,1500))
        self.currentMiniLineEdit.setValidator(QIntValidator(0,1500))
        self.tempMaxLineEdit.setValidator(QIntValidator(-40,120))
        self.tempMiniLineEdit.setValidator(QIntValidator(-40,120))

        # Disable the change of the table item
        self.voltageTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set table item
        for num in range(0, 14):
            self.cellData['voltage'][num] = 0
            self.voltageTable.setItem(num, 0, QTableWidgetItem(
                str(self.cellData['voltage'][num])))
            self.voltageTable.setItem(num, 1, QTableWidgetItem('mV'))

        # Disable spinbox line edit
        self.recordDoubleSpinBox.lineEdit().setReadOnly(True)

        # Set the stop monitoring button to close
        self.stopButton.setEnabled(False)

        # Set the stop plotting button to close
        self.stopPlotButton.setEnabled(False)

        # Set the stop balancing button to close
        self.StopBalancingButton.setEnabled(False)

        # Set the port status to be unchanged
        self.portStatusDisplay.setEnabled(False)

        # Set the cell balancing status to be unchanged
        self.CellBalancingStatusDisplay.setEnabled(False)

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

        # Connect cell balancing control button functions
        self.StartBalancingButton.clicked.connect(self.startCellBalancing)
        self.StopBalancingButton.clicked.connect(self.stopCellBalancing)

        # Connect zoom button functions
        self.zoomButton.clicked.connect(self.zoomGraph)
        self.zoomButton_2.clicked.connect(self.zoomGraph_2)
        self.zoomButton_3.clicked.connect(self.zoomGraph_3)
        self.zoomButton_4.clicked.connect(self.zoomGraph_4)

        # Connect load button function
        self.loadingButton.clicked.connect(self.openFile)
        self.plotlyButton.clicked.connect(self.plotByPlotly)

        # Connect stack widgets functions
        self.cbPushButtonSoC.clicked.connect(lambda: self.cbStackedWidget.setCurrentIndex(0))
        self.cbPushButtonControl.clicked.connect(lambda: self.cbStackedWidget.setCurrentIndex(1))

        # Connect output time interval function
        self.recordDoubleSpinBox.valueChanged.connect(self.updateOutputTimeInterval)

        # Update threshold values
        self.voltageMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.voltageMiniLineEdit.textChanged.connect(self.updateThreshold)

        self.currentMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.currentMiniLineEdit.textChanged.connect(self.updateThreshold)

        self.tempMaxLineEdit.textChanged.connect(self.updateThreshold)
        self.tempMiniLineEdit.textChanged.connect(self.updateThreshold)

        # Link the timer to functions
        self.timer.timeout.connect(self.receiveData)
        self.timer2.timeout.connect(self.updateGraphData)
        self.timer3.timeout.connect(self.recordData)

# ===================Update threshold values====================

    def updateThreshold(self):
        """This function is used to update the threshold values"""
        self.currentThreshold = [int(self.currentMiniLineEdit.text()), int(
            self.currentMaxLineEdit.text())]

        self.voltageThreshold = [int(self.voltageMiniLineEdit.text()), int(
            self.voltageMaxLineEdit.text())]
        
        self.tempThreshold = [int(self.tempMiniLineEdit.text()), int(
            self.tempMaxLineEdit.text())]

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
        self.EFC_Data = 0
        self.packVoltageLineEdit.setText(str(self.packData['voltage']))
        self.packCurrentLineEdit.setText(str(self.packData['current']))

        # Clear IC temp data
        self.ICData['temp'] = 0
        self.ICTempLineEdit.setText(str(self.ICData['temp']))

        # Clear port status
        self.portStatusDisplay.setEnabled(False)

        # Clear output data and graph data
        self.stopRecordButton.setChecked(True)
        self.graphData = np.zeros((59,1)).astype(np.float16)
        self.xaxis = np.zeros(1).astype(np.float16)

        self.outputData = np.zeros((1,59)).astype(np.int32)

        # Clear battery data
        self.bccData = [0 for _ in range(17)]
        self.SOC_SOHData = [0 for _ in range(28)]

        try:
            self.stopPlotting()
            self.cellCurve0.setData(self.xaxis,self.graphData[0], _callSync='off')
            self.cellCurve1.setData(self.xaxis,self.graphData[1], _callSync='off')
            self.cellCurve2.setData(self.xaxis,self.graphData[2], _callSync='off')
            self.cellCurve3.setData(self.xaxis,self.graphData[3], _callSync='off')
            self.cellCurve4.setData(self.xaxis,self.graphData[4], _callSync='off')
            self.cellCurve5.setData(self.xaxis,self.graphData[5], _callSync='off')
            self.cellCurve6.setData(self.xaxis,self.graphData[6], _callSync='off')
            self.cellCurve7.setData(self.xaxis,self.graphData[7], _callSync='off')
            self.cellCurve8.setData(self.xaxis,self.graphData[8], _callSync='off')
            self.cellCurve9.setData(self.xaxis,self.graphData[9], _callSync='off')
            self.cellCurve10.setData(self.xaxis,self.graphData[10], _callSync='off')
            self.cellCurve11.setData(self.xaxis,self.graphData[11], _callSync='off')
            self.cellCurve12.setData(self.xaxis,self.graphData[12], _callSync='off')
            self.cellCurve13.setData(self.xaxis,self.graphData[13], _callSync='off')
            self.cellCurve14.setData(self.xaxis,self.graphData[14], _callSync='off')
            self.cellCurve15.setData(self.xaxis,self.graphData[15], _callSync='off')
            self.cellCurve16.setData(self.xaxis,self.graphData[16], _callSync='off')
            self.cellCurve17.setData(self.xaxis,self.graphData[17], _callSync='off')
            self.cellCurve18.setData(self.xaxis,self.graphData[18], _callSync='off')
            self.cellCurve19.setData(self.xaxis,self.graphData[19], _callSync='off')
            self.cellCurve20.setData(self.xaxis,self.graphData[20], _callSync='off')
            self.cellCurve21.setData(self.xaxis,self.graphData[21], _callSync='off')
            self.cellCurve22.setData(self.xaxis,self.graphData[22], _callSync='off')
            self.cellCurve23.setData(self.xaxis,self.graphData[23], _callSync='off')
            self.cellCurve24.setData(self.xaxis,self.graphData[24], _callSync='off')
            self.cellCurve25.setData(self.xaxis,self.graphData[25], _callSync='off')
            self.cellCurve26.setData(self.xaxis,self.graphData[26], _callSync='off')
            self.cellCurve27.setData(self.xaxis,self.graphData[27], _callSync='off')
            self.cellCurve28.setData(self.xaxis,self.graphData[28], _callSync='off')
            self.cellCurve29.setData(self.xaxis,self.graphData[29], _callSync='off')
            self.cellCurve30.setData(self.xaxis,self.graphData[30], _callSync='off')
            self.cellCurve31.setData(self.xaxis,self.graphData[31], _callSync='off')
            self.cellCurve32.setData(self.xaxis,self.graphData[32], _callSync='off')
            self.cellCurve33.setData(self.xaxis,self.graphData[33], _callSync='off')
            self.cellCurve34.setData(self.xaxis,self.graphData[34], _callSync='off')
            self.cellCurve35.setData(self.xaxis,self.graphData[35], _callSync='off')
            self.cellCurve36.setData(self.xaxis,self.graphData[36], _callSync='off')
            self.cellCurve37.setData(self.xaxis,self.graphData[37], _callSync='off')
            self.cellCurve38.setData(self.xaxis,self.graphData[38], _callSync='off')
            self.cellCurve39.setData(self.xaxis,self.graphData[39], _callSync='off')
            self.cellCurve40.setData(self.xaxis,self.graphData[40], _callSync='off')
            self.cellCurve41.setData(self.xaxis,self.graphData[41], _callSync='off')
            self.cellCurve42.setData(self.xaxis,self.graphData[42], _callSync='off')
            self.cellCurve43.setData(self.xaxis,self.graphData[43], _callSync='off')
            self.cellCurve44.setData(self.xaxis,self.graphData[44], _callSync='off')
            self.cellCurve45.setData(self.xaxis,self.graphData[45], _callSync='off')
            self.cellCurve46.setData(self.xaxis,self.graphData[46], _callSync='off')
            self.cellCurve47.setData(self.xaxis,self.graphData[47], _callSync='off')
            self.cellCurve48.setData(self.xaxis,self.graphData[48], _callSync='off')
            self.cellCurve49.setData(self.xaxis,self.graphData[49], _callSync='off')
            self.cellCurve50.setData(self.xaxis,self.graphData[50], _callSync='off')
            self.cellCurve51.setData(self.xaxis,self.graphData[51], _callSync='off')
            self.cellCurve52.setData(self.xaxis,self.graphData[52], _callSync='off')
            self.cellCurve53.setData(self.xaxis,self.graphData[53], _callSync='off')
            self.cellCurve54.setData(self.xaxis,self.graphData[54], _callSync='off')
            self.cellCurve55.setData(self.xaxis,self.graphData[55], _callSync='off')
            self.cellCurve56.setData(self.xaxis,self.graphData[56], _callSync='off')
            self.cellCurve57.setData(self.xaxis,self.graphData[57], _callSync='off')
            self.cellCurve58.setData(self.xaxis,self.graphData[58], _callSync='off')
        except:
            pass

        gc.collect()

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

        # Clear status
        self.statusUpdateFlag = [0 for _ in range(17)]

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

        # Set the timer for receiving
        self.timer.start(1)  # 1ms/T

    def stopMonitor(self):
        """Stop the monitoring process"""
        try:
            self.timer.stop()
            self.timer2.stop()
            self.stopPlotting()
            self.stopRecordButton.setChecked(True) #Stop timer 3
            self.stopCellBalancing()
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
        self.timer3.start(1000) # 1s

        # Disable change output time interval function
        self.recordDoubleSpinBox.setEnabled(False)

    def stopRecording(self):
        """Handler for stop data recording"""
        self.timer3.stop()

        # Enable change output time interval function
        self.recordDoubleSpinBox.setEnabled(True)

    def updateOutputTimeInterval(self):
        """Handler for changing output time interval"""
        self.outputTimeInterval = int(self.recordDoubleSpinBox.value() * 3600)
        
    def recordData(self):
        """Handler for updating data"""
        # Update real time data
        realTimeData = [0 for _ in range(59)]

        if self.serial.isOpen():
            # Set time information
            timeInfo = QDateTime.currentDateTime().toSecsSinceEpoch()

            # Add realtime data
            realTimeData[0:14] = self.bccData[1:15] # Cell Voltage Data
            realTimeData[14] = self.bccData[16] # Pack Current Data
            realTimeData[15:43] = self.SOC_SOHData # SoC and SoH Data
            realTimeData[43] = self.EFC_Data
            realTimeData[44:58] = self.CBData
            realTimeData[58] = timeInfo # Time information

            self.outputData = np.append(self.outputData, [realTimeData], axis = 0) # Convert to two dimension and add to output data
            
            if self.outputData.shape[0] > self.outputTimeInterval: # Automatic Recording
                columnName = [
                            'cellVoltage_1','cellVoltage_2','cellVoltage_3','cellVoltage_4',
                            'cellVoltage_5', 'cellVoltage_6', 'cellVoltage_7', 'cellVoltage_8', 
                            'cellVoltage_9','cellVoltage_10','cellVoltage_11','cellVoltage_12',
                            'cellVoltage_13','cellVoltage_14',
                            'packCurrent',

                            'cellSoC_1','cellSoC_2','cellSoC_3','cellSoC_4',
                            'cellSoC_5','cellSoC_6','cellSoC_7','cellSoC_8',
                            'cellSoC_9','cellSoC_10','cellSoC_11','cellSoC_12',
                            'cellSoC_13','cellSoC_14',

                            'cellSoH_1','cellSoH_2','cellSoH_3','cellSoH_4',
                            'cellSoH_5','cellSoH_6','cellSoH_7','cellSoH_8',
                            'cellSoH_9','cellSoH_10','cellSoH_11','cellSoH_12',
                            'cellSoH_13','cellSoH_14',
                            'equivalentFullCycle',

                            'cellCB_1','cellCB_2','cellCB_3','cellCB_4',
                            'cellCB_5','cellCB_6','cellCB_7','cellCB_8',
                            'cellCB_9','cellCB_10','cellCB_11','cellCB_12',
                            'cellCB_13','cellCB_14',

                            'Date']

                outputDir_1 = './Data/Charging'
                outputDir_2 = './Data/Discharging'
                outputDir_3 = './Data/OpenCircuit'

                if not os.path.exists(outputDir_1):
                    os.mkdir(outputDir_1)
                
                if not os.path.exists(outputDir_2):
                    os.mkdir(outputDir_2)

                if not os.path.exists(outputDir_3):
                    os.mkdir(outputDir_3)

                if self.outputData[1][14] < 0: # Current smaller then 0
                    fileName = outputDir_1 + "/" + str(timeInfo) + ".csv" # Address name
                elif self.outputData[1][14] > 20:
                    fileName = outputDir_2 + "/" + str(timeInfo) + ".csv" # Address name
                else:
                    fileName = outputDir_3 + "/" + str(timeInfo) + ".csv" # Address name

                self.outputData = np.delete(self.outputData, 0, axis = 0) # Remove first line

                df = pd.DataFrame(self.outputData, columns = columnName) 
                df.to_csv(fileName, index=False, line_terminator='\n')

                self.outputData = np.zeros((1,59)).astype(np.int32)
                del df

        del realTimeData
        gc.collect() # Collect garbage

    def printData(self):
        """Handler for saving data"""
        self.stopRecordButton.setChecked(True)
        
        if self.serial.isOpen() and self.outputData.shape[0] > 1:
            fileName = QFileDialog.getSaveFileName(self, "Save File", ".", ("*.csv"))

            self.outputData = np.delete(self.outputData, 0, axis = 0) # Delete 0 line

            columnName = [
            'cellVoltage_1','cellVoltage_2','cellVoltage_3','cellVoltage_4',
            'cellVoltage_5', 'cellVoltage_6', 'cellVoltage_7', 'cellVoltage_8', 
            'cellVoltage_9','cellVoltage_10','cellVoltage_11','cellVoltage_12',
            'cellVoltage_13','cellVoltage_14',
            'packCurrent',

            'cellSoC_1','cellSoC_2','cellSoC_3','cellSoC_4',
            'cellSoC_5','cellSoC_6','cellSoC_7','cellSoC_8',
            'cellSoC_9','cellSoC_10','cellSoC_11','cellSoC_12',
            'cellSoC_13','cellSoC_14',

            'cellSoH_1','cellSoH_2','cellSoH_3','cellSoH_4',
            'cellSoH_5','cellSoH_6','cellSoH_7','cellSoH_8',
            'cellSoH_9','cellSoH_10','cellSoH_11','cellSoH_12',
            'cellSoH_13','cellSoH_14',
            'equivalentFullCycle',

            'cellCB_1','cellCB_2','cellCB_3','cellCB_4',
            'cellCB_5','cellCB_6','cellCB_7','cellCB_8',
            'cellCB_9','cellCB_10','cellCB_11','cellCB_12',
            'cellCB_13','cellCB_14',

            'Date']

            df = pd.DataFrame(self.outputData, columns = columnName)
            try:
                with open(fileName[0],'w') as f:
                    df.to_csv(f, index=False, line_terminator='\n')
                    f.close()
                    del df
            except:
                pass

            self.outputData = np.zeros((1,59)).astype(np.int32)
            gc.collect() # Collect garbage

        else:
            self.stopRecordButton.setChecked(True)
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')

# ===================Data graph plotting====================

    def plotGraph(self):
        """Show cell status, pack status, IC temperature in a graph"""
        self.cellCurve0  = self.graphWindow.packVoltageP.plot()
        self.cellCurve1  = self.graphWindow.p0.plot() # plotDataItem
        self.cellCurve2  = self.graphWindow.p1.plot()
        self.cellCurve3  = self.graphWindow.p2.plot()
        self.cellCurve4  = self.graphWindow.p3.plot()
        self.cellCurve5  = self.graphWindow.p4.plot()
        self.cellCurve6  = self.graphWindow.p5.plot()
        self.cellCurve7  = self.graphWindow.p6.plot()
        self.cellCurve8  = self.graphWindow.p7.plot()
        self.cellCurve9  = self.graphWindow.p8.plot()
        self.cellCurve10 = self.graphWindow.p9.plot()
        self.cellCurve11 = self.graphWindow.p10.plot()
        self.cellCurve12 = self.graphWindow.p11.plot()
        self.cellCurve13 = self.graphWindow.p12.plot()
        self.cellCurve14 = self.graphWindow.p13.plot()

        self.cellCurve15 = self.graphWindow.ICTempP.plot()
        self.cellCurve16 = self.graphWindow.packCurrentP.plot()

        self.cellCurve17 = self.graphWindow_SOC.p0.plot()
        self.cellCurve18 = self.graphWindow_SOC.p1.plot()
        self.cellCurve19 = self.graphWindow_SOC.p2.plot()
        self.cellCurve20 = self.graphWindow_SOC.p3.plot()
        self.cellCurve21 = self.graphWindow_SOC.p4.plot()
        self.cellCurve22 = self.graphWindow_SOC.p5.plot()
        self.cellCurve23 = self.graphWindow_SOC.p6.plot()
        self.cellCurve24 = self.graphWindow_SOC.p7.plot()
        self.cellCurve25 = self.graphWindow_SOC.p8.plot()
        self.cellCurve26 = self.graphWindow_SOC.p9.plot()
        self.cellCurve27 = self.graphWindow_SOC.p10.plot()
        self.cellCurve28 = self.graphWindow_SOC.p11.plot()
        self.cellCurve29 = self.graphWindow_SOC.p12.plot()
        self.cellCurve30 = self.graphWindow_SOC.p13.plot()

        self.cellCurve31 = self.graphWindow_SOH.p0.plot()
        self.cellCurve32 = self.graphWindow_SOH.p1.plot()
        self.cellCurve33 = self.graphWindow_SOH.p2.plot()
        self.cellCurve34 = self.graphWindow_SOH.p3.plot()
        self.cellCurve35 = self.graphWindow_SOH.p4.plot()
        self.cellCurve36 = self.graphWindow_SOH.p5.plot()
        self.cellCurve37 = self.graphWindow_SOH.p6.plot()
        self.cellCurve38 = self.graphWindow_SOH.p7.plot()
        self.cellCurve39 = self.graphWindow_SOH.p8.plot()
        self.cellCurve40 = self.graphWindow_SOH.p9.plot()
        self.cellCurve41 = self.graphWindow_SOH.p10.plot()
        self.cellCurve42 = self.graphWindow_SOH.p11.plot()
        self.cellCurve43 = self.graphWindow_SOH.p12.plot()
        self.cellCurve44 = self.graphWindow_SOH.p13.plot()

        self.cellCurve45 = self.graphWindow_CB.p0.plot()
        self.cellCurve46 = self.graphWindow_CB.p1.plot()
        self.cellCurve47 = self.graphWindow_CB.p2.plot()
        self.cellCurve48 = self.graphWindow_CB.p3.plot()
        self.cellCurve49 = self.graphWindow_CB.p4.plot()
        self.cellCurve50 = self.graphWindow_CB.p5.plot()
        self.cellCurve51 = self.graphWindow_CB.p6.plot()
        self.cellCurve52 = self.graphWindow_CB.p7.plot()
        self.cellCurve53 = self.graphWindow_CB.p8.plot()
        self.cellCurve54 = self.graphWindow_CB.p9.plot()
        self.cellCurve55 = self.graphWindow_CB.p10.plot()
        self.cellCurve56 = self.graphWindow_CB.p11.plot()
        self.cellCurve57 = self.graphWindow_CB.p12.plot()
        self.cellCurve58 = self.graphWindow_CB.p13.plot()

        if self.serial.isOpen():
            self.timer2.start(200)
            self.startPlotButton.setEnabled(False)
            self.stopPlotButton.setEnabled(True)
        else:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')

    def updateGraphData(self):
        """Handler for updating curve data"""
        insertData = list(i / 1000000 for i in self.bccData) # All bcc element divided by 1000000
        insertData[15] = insertData[15] * 100000 # xxx/1000000*10000=xxx/10
        insertData[16] = insertData[16] * 1000000 # xx/1000000*1000000=xx

        insertData.extend(list(i / 10 for i in self.SOC_SOHData))

        insertData.extend(self.CBData)

        insertData = np.array(insertData).reshape((59,1))

        self.graphData = np.append(self.graphData, insertData, axis = 1)
        self.xaxis = np.append(self.xaxis,(self.xaxis[-1] + 0.2))

        if self.graphData.shape[1] >= 9000: # Remove the first value after 9000*0.2/60=30mins
            self.xaxis = self.xaxis[1:]  # Remove the first x element.
            self.graphData = np.delete(self.graphData, 0, axis = 1) # Remove first column

        self.cellCurve0.setData(self.xaxis,self.graphData[0], _callSync='off')
        self.cellCurve1.setData(self.xaxis,self.graphData[1], _callSync='off')
        self.cellCurve2.setData(self.xaxis,self.graphData[2], _callSync='off')
        self.cellCurve3.setData(self.xaxis,self.graphData[3], _callSync='off')
        self.cellCurve4.setData(self.xaxis,self.graphData[4], _callSync='off')
        self.cellCurve5.setData(self.xaxis,self.graphData[5], _callSync='off')
        self.cellCurve6.setData(self.xaxis,self.graphData[6], _callSync='off')
        self.cellCurve7.setData(self.xaxis,self.graphData[7], _callSync='off')
        self.cellCurve8.setData(self.xaxis,self.graphData[8], _callSync='off')
        self.cellCurve9.setData(self.xaxis,self.graphData[9], _callSync='off')
        self.cellCurve10.setData(self.xaxis,self.graphData[10], _callSync='off')
        self.cellCurve11.setData(self.xaxis,self.graphData[11], _callSync='off')
        self.cellCurve12.setData(self.xaxis,self.graphData[12], _callSync='off')
        self.cellCurve13.setData(self.xaxis,self.graphData[13], _callSync='off')
        self.cellCurve14.setData(self.xaxis,self.graphData[14], _callSync='off')
        self.cellCurve15.setData(self.xaxis,self.graphData[15], _callSync='off')
        self.cellCurve16.setData(self.xaxis,self.graphData[16], _callSync='off')
        self.cellCurve17.setData(self.xaxis,self.graphData[17], _callSync='off')
        self.cellCurve18.setData(self.xaxis,self.graphData[18], _callSync='off')
        self.cellCurve19.setData(self.xaxis,self.graphData[19], _callSync='off')
        self.cellCurve20.setData(self.xaxis,self.graphData[20], _callSync='off')
        self.cellCurve21.setData(self.xaxis,self.graphData[21], _callSync='off')
        self.cellCurve22.setData(self.xaxis,self.graphData[22], _callSync='off')
        self.cellCurve23.setData(self.xaxis,self.graphData[23], _callSync='off')
        self.cellCurve24.setData(self.xaxis,self.graphData[24], _callSync='off')
        self.cellCurve25.setData(self.xaxis,self.graphData[25], _callSync='off')
        self.cellCurve26.setData(self.xaxis,self.graphData[26], _callSync='off')
        self.cellCurve27.setData(self.xaxis,self.graphData[27], _callSync='off')
        self.cellCurve28.setData(self.xaxis,self.graphData[28], _callSync='off')
        self.cellCurve29.setData(self.xaxis,self.graphData[29], _callSync='off')
        self.cellCurve30.setData(self.xaxis,self.graphData[30], _callSync='off')
        self.cellCurve31.setData(self.xaxis,self.graphData[31], _callSync='off')
        self.cellCurve32.setData(self.xaxis,self.graphData[32], _callSync='off')
        self.cellCurve33.setData(self.xaxis,self.graphData[33], _callSync='off')
        self.cellCurve34.setData(self.xaxis,self.graphData[34], _callSync='off')
        self.cellCurve35.setData(self.xaxis,self.graphData[35], _callSync='off')
        self.cellCurve36.setData(self.xaxis,self.graphData[36], _callSync='off')
        self.cellCurve37.setData(self.xaxis,self.graphData[37], _callSync='off')
        self.cellCurve38.setData(self.xaxis,self.graphData[38], _callSync='off')
        self.cellCurve39.setData(self.xaxis,self.graphData[39], _callSync='off')
        self.cellCurve40.setData(self.xaxis,self.graphData[40], _callSync='off')
        self.cellCurve41.setData(self.xaxis,self.graphData[41], _callSync='off')
        self.cellCurve42.setData(self.xaxis,self.graphData[42], _callSync='off')
        self.cellCurve43.setData(self.xaxis,self.graphData[43], _callSync='off')
        self.cellCurve44.setData(self.xaxis,self.graphData[44], _callSync='off')
        self.cellCurve45.setData(self.xaxis,self.graphData[45], _callSync='off')
        self.cellCurve46.setData(self.xaxis,self.graphData[46], _callSync='off')
        self.cellCurve47.setData(self.xaxis,self.graphData[47], _callSync='off')
        self.cellCurve48.setData(self.xaxis,self.graphData[48], _callSync='off')
        self.cellCurve49.setData(self.xaxis,self.graphData[49], _callSync='off')
        self.cellCurve50.setData(self.xaxis,self.graphData[50], _callSync='off')
        self.cellCurve51.setData(self.xaxis,self.graphData[51], _callSync='off')
        self.cellCurve52.setData(self.xaxis,self.graphData[52], _callSync='off')
        self.cellCurve53.setData(self.xaxis,self.graphData[53], _callSync='off')
        self.cellCurve54.setData(self.xaxis,self.graphData[54], _callSync='off')
        self.cellCurve55.setData(self.xaxis,self.graphData[55], _callSync='off')
        self.cellCurve56.setData(self.xaxis,self.graphData[56], _callSync='off')
        self.cellCurve57.setData(self.xaxis,self.graphData[57], _callSync='off')
        self.cellCurve58.setData(self.xaxis,self.graphData[58], _callSync='off')

        self.cbProgressBar.setValue(round(self.SOC_SOHData[0]*0.1))
        self.cbProgressBar_2.setValue(round(self.SOC_SOHData[1]*0.1))
        self.cbProgressBar_3.setValue(round(self.SOC_SOHData[2]*0.1))
        self.cbProgressBar_4.setValue(round(self.SOC_SOHData[3]*0.1))
        self.cbProgressBar_5.setValue(round(self.SOC_SOHData[4]*0.1))
        self.cbProgressBar_6.setValue(round(self.SOC_SOHData[5]*0.1))
        self.cbProgressBar_7.setValue(round(self.SOC_SOHData[6]*0.1))
        self.cbProgressBar_8.setValue(round(self.SOC_SOHData[7]*0.1))
        self.cbProgressBar_9.setValue(round(self.SOC_SOHData[8]*0.1))
        self.cbProgressBar_10.setValue(round(self.SOC_SOHData[9]*0.1))
        self.cbProgressBar_11.setValue(round(self.SOC_SOHData[10]*0.1))
        self.cbProgressBar_12.setValue(round(self.SOC_SOHData[11]*0.1))
        self.cbProgressBar_13.setValue(round(self.SOC_SOHData[12]*0.1))
        self.cbProgressBar_14.setValue(round(self.SOC_SOHData[13]*0.1))

        del insertData
        gc.collect()

    def stopPlotting(self):
        """Handler for stop plotting data"""
        self.timer2.stop()
        self.startPlotButton.setEnabled(True)
        self.stopPlotButton.setEnabled(False)
    
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
            'IC Temperature': 15,
            'Pack Current': 16,
        }

        if self.graphData.shape[1] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox.currentText()

            if graphItemIndex < 15:
                yLabel = "Voltage (V)"
            elif graphItemIndex == 15:
                yLabel = "Temperature (°C)"
            else:
                yLabel = "Current (mA)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.xaxis,self.graphData[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')

    def zoomGraph_2(self):
        """Handler for zooming graph 2"""
        zoomedGraph = self.zoomGraphComboBox_2.currentText()
        zoomedGraphDict = {
            'Cell 1 SoC': 17,
            'Cell 2 SoC': 18,
            'Cell 3 SoC': 19,
            'Cell 4 SoC': 20,
            'Cell 5 SoC': 21,
            'Cell 6 SoC': 22,
            'Cell 7 SoC': 23,
            'Cell 8 SoC': 24,
            'Cell 9 SoC': 25,
            'Cell 10 SoC': 26,
            'Cell 11 SoC': 27,
            'Cell 12 SoC': 28,
            'Cell 13 SoC': 29,
            'Cell 14 SoC': 30,
        }

        if self.graphData.shape[1] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox_2.currentText()

            yLabel = "SoC (%)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.xaxis,self.graphData[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')

    def zoomGraph_3(self):
        """Handler for zooming graph 3"""
        zoomedGraph = self.zoomGraphComboBox_3.currentText()
        zoomedGraphDict = {
            'Cell 1 SoH': 31,
            'Cell 2 SoH': 32,
            'Cell 3 SoH': 33,
            'Cell 4 SoH': 34,
            'Cell 5 SoH': 35,
            'Cell 6 SoH': 36,
            'Cell 7 SoH': 37,
            'Cell 8 SoH': 38,
            'Cell 9 SoH': 39,
            'Cell 10 SoH': 40,
            'Cell 11 SoH': 41,
            'Cell 12 SoH': 42,
            'Cell 13 SoH': 43,
            'Cell 14 SoH': 44,
        }

        if self.graphData.shape[1] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox_3.currentText()
            
            yLabel = "SoH (%)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.xaxis,self.graphData[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')

    def zoomGraph_4(self):
        """Handler for zooming graph 4"""
        zoomedGraph = self.zoomGraphComboBox_4.currentText()
        zoomedGraphDict = {
            'Cell 1 CB Control': 45,
            'Cell 2 CB Control': 46,
            'Cell 3 CB Control': 47,
            'Cell 4 CB Control': 48,
            'Cell 5 CB Control': 49,
            'Cell 6 CB Control': 50,
            'Cell 7 CB Control': 51,
            'Cell 8 CB Control': 52,
            'Cell 9 CB Control': 53,
            'Cell 10 CB Control': 54,
            'Cell 11 CB Control': 55,
            'Cell 12 CB Control': 56,
            'Cell 13 CB Control': 57,
            'Cell 14 CB Control': 58,
        }

        if self.graphData.shape[1] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox_4.currentText()
            
            yLabel = "On/Off"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.xaxis,self.graphData[graphItemIndex]) # Plot Curve
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

            if readFile.shape[0] > 2: # Larger than 2 lines
                loadWindow = loadGraphWindow()
                loadWindow.loadGraphData(readFile)
                loadWindow.exec()
            else:
                QMessageBox.critical(
                    self, 'Data error', 'Invalid data, please check file')
            
            del readFile
            gc.collect()
        except:
            pass
    
    def plotByPlotly(self):
        """Handler for Plotly plotting"""
        try:
            
            dischargingPlot = cellDataPlotting('.\Data\Discharging')
            dischargingPlot.plotBatteryData()

            del dischargingPlot 
        except:
            QMessageBox.critical(
                self, 'Data error', 'No discharging data, please check folder')
        
        try:
            chargingPlot = cellDataPlotting('.\Data\Charging')
            chargingPlot.plotBatteryData()
        
            del chargingPlot
        except:
            QMessageBox.critical(
                self, 'Data error', 'No charging data, please check folder')
        try:
            openCircuitPlot = cellDataPlotting('.\Data\OpenCircuit')
            openCircuitPlot.plotBatteryData()

            del openCircuitPlot
        except:
            QMessageBox.critical(
                self, 'Data error', 'No open circuit data, please check folder')
        
        gc.collect()

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

        # Update pack data
        self.packVoltageLineEdit.setText(str(self.packData['voltage']))

        self.packCurrentLineEdit.setText(str(self.packData['current']))

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

        # Update IC data
        self.ICTempLineEdit.setText(str(self.ICData['temp']))

        if self.ICData['tempStatus'] == tempStatus.OVERTEMPERATURE:
            self.ICStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        elif self.ICData['tempStatus'] == tempStatus.UNDERTEMPERATURE:
            self.ICStatusDisplay.setStyleSheet(
                "background-color: rgb(255, 0, 0)")
        else:
            pass
        
        # Set EFC value
        self.efcLineEdit.setText(str(self.EFC_Data))

        # Set status
        self.packVoltageStatusDisplay.setText(
            self.packData['voltageStatus'].value)

        self.packCurrentStatusDisplay.setText(
            self.packData['currentStatus'].value)

        self.ICStatusDisplay.setText(self.ICData['tempStatus'].value)

# ===================Cell balancing====================
    def startCellBalancing(self):
        # Disable start cell balancing button if monitoring is started
        if self.serial.isOpen():
            self.command = b'OPEN\t'
            self.serial.write(self.command)
            
            self.StartBalancingButton.setEnabled(False)
            self.StopBalancingButton.setEnabled(True)
            self.CellBalancingStatusDisplay.setChecked(True)
        else:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')

    def stopCellBalancing(self):
        # Disable stop cell balancing button if monitoring is started
        if self.serial.isOpen():
            self.command = b'OVER\t'
            self.serial.write(self.command)

            self.StartBalancingButton.setEnabled(True)
            self.StopBalancingButton.setEnabled(False)
            self.CellBalancingStatusDisplay.setChecked(False)
        else:
            QMessageBox.critical(
                self, 'COM error', 'COM data error, please reconnect the port')

# ===================GUI pop-up dialogues====================

    def helpAction(self):
        """User manual"""
        QMessageBox.about(self,
                          "Help",
                          "\nThis GUI supports: \n\
            1. Change UART settings\n\
            2. Set threshold values\n\
            3. Display battery data and status\n\
            4. Display pack data and status\n\
            5. Display MC33771C temperature\n\
            6. Record battery data\n\
            7. Load battery data\n\
            8. Plot full-cycle battery data\n\
            9. Cell balancing control\n\n\
        Follow these steps to use this GUI: \n\
            1. Set UART configuration\n\
            2. Set threshold values\n\
            3. Start monitoring\n\
            4. Check data and status\n\
        *To check cell status, please click the cell button\n\
        *The button will turn red if there is a problem with the status\n")

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
        # Update pack voltage
        self.packData['voltage'] = self.bccData[0] / 1000

        if self.statusUpdateFlag[0] == 0:
            if self.packData['voltage'] > self.packVoltageThreshold[1]:
                self.packData['voltageStatus'] = voltageStatus.OVERVOLTAGE
                self.statusUpdateFlag[0] = 1
            elif self.packData['voltage'] < self.packVoltageThreshold[0]:
                self.packData['voltageStatus'] = voltageStatus.UNDERVOLTAGE
                self.statusUpdateFlag[0] = 1
            else:
                self.packData['voltageStatus'] = voltageStatus.DEFAULT

        # Update pack current
        self.packData['current'] = self.bccData[16]

        if self.statusUpdateFlag[16] == 0:
            if abs(self.packData['current']) > self.currentThreshold[1]:
                self.packData['currentStatus'] = currentStatus.OVERCURRENT
                self.statusUpdateFlag[16] = 1
            elif abs(self.packData['current']) < self.currentThreshold[0]:
                self.packData['currentStatus'] = currentStatus.UNDERCURRENT
                self.statusUpdateFlag[16] = 1
            else:
                self.packData['currentStatus'] = currentStatus.DEFAULT

        # Update cell voltage
        for i in range(0, 14):
            self.cellData['voltage'][i] = self.bccData[i+1] / 1000
            self.cellData['currentStatus'][i] = self.packData['currentStatus']

            if self.statusUpdateFlag[i + 1] == 0:
                if self.cellData['voltage'][i] > self.voltageThreshold[1]:
                    self.cellData['voltageStatus'][i] = voltageStatus.OVERVOLTAGE
                    self.statusUpdateFlag[i + 1] = 1
                elif self.cellData['voltage'][i] < self.voltageThreshold[0]:
                    self.cellData['voltageStatus'][i] = voltageStatus.UNDERVOLTAGE
                    self.statusUpdateFlag[i + 1] = 1
                else:
                    self.cellData['voltageStatus'][i] = voltageStatus.DEFAULT

        # Update IC Temperature
        self.ICData['temp'] = self.bccData[15] / 10

        if self.statusUpdateFlag[15] == 0:
            if self.ICData['temp'] > self.tempThreshold[1]:
                self.ICData['tempStatus'] = tempStatus.OVERTEMPERATURE
                self.statusUpdateFlag[15] = 1
            elif self.ICData['temp'] < self.tempThreshold[0]:
                self.ICData['tempStatus'] = tempStatus.UNDERTEMPERATURE
                self.statusUpdateFlag[15] = 1
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
            self.stopMonitor()
            return None

        if self.waitBits > 0:
            # Read data from COM port
            bccRawData = self.serial.read(self.waitBits)
            
            # Transfer the byte data to UART data list
            dataList = list(hex(data) for data in list(bccRawData))

            # Filter out incorrect inputs
            if len(dataList) == 240:
                data = util.listData2strData(dataList)
                self.bccData = data[0:17]
                self.SOC_SOHData = data[17:45]
                self.EFC_Data = data[45]
                self.CBData = data[46:60]

                self.updateData()
                self.updateGUIData()
            else:
                pass
        else:
            pass

# ===================Main====================

if __name__ == "__main__":
    application = QApplication(sys.argv)
    application.setStyle('QtCurve')
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
