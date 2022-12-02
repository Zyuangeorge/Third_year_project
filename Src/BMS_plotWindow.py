import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import (QComboBox, QDialog, QHBoxLayout, QMessageBox,
                               QPushButton, QVBoxLayout,QTabWidget,QLabel,QWidget)


class plotWindow(pg.GraphicsLayoutWidget):
    """Window for plotting graphs"""
    def __init__(self):
        super().__init__()

        # Set plot windows
        self.p0 = self.addPlot(title="Cell 1 Voltage")
        self.p1 = self.addPlot(title="Cell 2 Voltage")
        self.p2 = self.addPlot(title="Cell 3 Voltage")
        self.p3 = self.addPlot(title="Cell 4 Voltage")

        self.nextRow()
        self.p4 = self.addPlot(title="Cell 5 Voltage")
        self.p5 = self.addPlot(title="Cell 6 Voltage")
        self.p6 = self.addPlot(title="Cell 7 Voltage")
        self.p7 = self.addPlot(title="Cell 8 Voltage")

        self.nextRow()
        self.p8 = self.addPlot(title="Cell 9 Voltage")
        self.p9 = self.addPlot(title="Cell 10 Voltage")
        self.p10 = self.addPlot(title="Cell 11 Voltage")
        self.p11 = self.addPlot(title="Cell 12 Voltage")

        self.nextRow()
        self.p12 = self.addPlot(title="Cell 13 Voltage")
        self.p13 = self.addPlot(title="Cell 14 Voltage")
        self.packCurrentP = self.addPlot(title="Pack Current")

        self.nextRow()
        self.ICTempP = self.addPlot(title="IC Temperature")
        self.packVoltageP = self.addPlot(title="Pack Voltage")

        self.voltageCurves = [
            self.p0,self.p1,self.p2,self.p3,
            self.p4,self.p5,self.p6,self.p7,
            self.p8,self.p9,self.p10,self.p11,
            self.p12,self.p13]

        self.initCurves()

    def initCurves(self):
        """Handler for curve initialisation"""
        for curve in self.voltageCurves:
            curve.setLabel('bottom', "Time (s)")
            curve.setLabel('left', "Voltage (V)")
            curve.enableAutoRange(axis='y')
        
        self.ICTempP.setLabel('bottom', "Time (s)")
        self.ICTempP.setLabel('left', "Temperature (°C)")
        self.ICTempP.enableAutoRange(axis='y')

        self.packVoltageP.setLabel('bottom', "Time (s)")
        self.packVoltageP.setLabel('left', "Voltage (V)")
        self.packVoltageP.enableAutoRange(axis='y')

        self.packCurrentP.setLabel('bottom', "Time (s)")
        self.packCurrentP.setLabel('left', "Current (mA)")
        self.packCurrentP.enableAutoRange(axis='y')


class zoomWindow(QDialog):
    """Window for zooming graphs"""
    def __init__(self):
        super().__init__()

        self.canvas = pg.GraphicsLayoutWidget()

        self.labels = ["Default window name","Default left label"]
        
        self.plot = self.canvas.addPlot()

        self.initGraph()
    
    def initGraph(self):
        """Handler for initialisation graph window"""

        self.setWindowTitle(self.labels[0])

        self.canvas.resize(800, 600)
        
        self.plot.setLabel('left', self.labels[1])
        self.plot.setLabel('bottom', "Time (s)")

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def updateGraph(self):
        """Handler for updating graph labels"""
        self.setWindowTitle(self.labels[0])
        self.plot.setLabel('left', self.labels[1])
        self.plot.autoRange()


class loadGraphWindow(QDialog):
    """Window for zooming graphs"""
    def __init__(self):
        super().__init__()

        self.plotTabWindow = plotWindow()
        self.plotTabWindow.removeItem(self.plotTabWindow.packVoltageP)
        self.plotTabWindow.removeItem(self.plotTabWindow.ICTempP)

        self.plotTabWindow_2 = SOCPlotWindow()
        self.plotTabWindow_3 = SOHPlotWindow()
        
        # Reset x axis
        for curve in self.plotTabWindow.voltageCurves:
            curve.setLabel('bottom', "Time (s)")
        self.plotTabWindow.packCurrentP.setLabel('bottom', "Time (s)")
        
        for curve in self.plotTabWindow_2.SoCCurves:
            curve.setLabel('bottom', "Time (s)")
        
        for curve in self.plotTabWindow_3.SoHCurves:
            curve.setLabel('bottom', "Time (s)")

        self.tabWidget = QTabWidget()

        self.title = "Loaded file graphs"
        self.setMinimumWidth(800)

        self.initGraph()

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
        self.zoomGraphComboBox.addItem('Pack Current')

        self.zoomButton = QPushButton("Zoom Graph")

        graphPageLayout.addWidget(self.plotTabWindow)
        
        zoomLayout = QHBoxLayout()
        zoomLabel = QLabel("Choose to zoom")
        zoomLayout.addWidget(zoomLabel)
        zoomLayout.addWidget(self.zoomGraphComboBox)
        zoomLayout.addWidget(self.zoomButton)

        # Add graph panels
        self.batteryData_1Layout.addLayout(graphPageLayout)
        self.batteryData_1Layout.addLayout(zoomLayout)

    def initGraphPage_2(self):
        # Init graph page layout
        graphPageLayout = QVBoxLayout()
        graphPageLayout.addWidget(self.plotTabWindow_2)

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
        self.batteryData_2Layout.addLayout(graphPageLayout)
        self.batteryData_2Layout.addLayout(zoomLayout)

    def initGraphPage_3(self):
        # Init graph page layout
        graphPageLayout = QVBoxLayout()
        graphPageLayout.addWidget(self.plotTabWindow_3)

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
        self.batteryData_3Layout.addLayout(graphPageLayout)
        self.batteryData_3Layout.addLayout(zoomLayout)

    def initGraph(self):
        """Handler for initialisation graph window"""
        self.batteryData_1 = QWidget()
        self.batteryData_2 = QWidget()
        self.batteryData_3 = QWidget()

        self.batteryData_1Layout = QVBoxLayout(self.batteryData_1)
        self.batteryData_2Layout = QVBoxLayout(self.batteryData_2)
        self.batteryData_3Layout = QVBoxLayout(self.batteryData_3)

        self.tabWidget.addTab(self.batteryData_1,"Battery Cell Information")
        self.tabWidget.addTab(self.batteryData_2,"State of Charge Graphs")
        self.tabWidget.addTab(self.batteryData_3,"State of Health Graphs")

        self.initGraphPage_1()
        self.initGraphPage_2()
        self.initGraphPage_3()
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)

        # Connect zoom button functions
        self.zoomButton.clicked.connect(self.zoomGraph)
        self.zoomButton_2.clicked.connect(self.zoomGraph_2)
        self.zoomButton_3.clicked.connect(self.zoomGraph_3)
    
    def loadGraphData(self, readFile):
        """Handler for loading curve data"""

        readFile = readFile.drop('Date', axis=1) # Remove time column
        readFile = readFile.drop('equivalentFullCycle', axis=1) # Remove EFC column

        self.data = readFile.values # Set data frame as matrix

        self.data = np.array(self.data).astype(np.float32) # Transfer matrix to numpy matrix

        self.data = np.transpose(self.data) # Transpose the matrix

        for j in range(0,14):
            self.plotTabWindow.voltageCurves[j].plot(list(i / 1000000 for i in self.data[j])) # Set voltage data in order
            self.plotTabWindow_2.SoCCurves[j].plot(list(i / 10 for i in self.data[j+15]))
            self.plotTabWindow_3.SoHCurves[j].plot(list(i / 10 for i in self.data[j+29]))
        self.plotTabWindow.packCurrentP.plot(list(i for i in self.data[14]))

    def zoomGraph(self):
        """Handler for zooming graph"""
        zoomedGraph = self.zoomGraphComboBox.currentText()
        zoomedGraphDict = {
            'Cell 1 Voltage': 0,
            'Cell 2 Voltage': 1,
            'Cell 3 Voltage': 2,
            'Cell 4 Voltage': 3,
            'Cell 5 Voltage': 4,
            'Cell 6 Voltage': 5,
            'Cell 7 Voltage': 6,
            'Cell 8 Voltage': 7,
            'Cell 9 Voltage': 8,
            'Cell 10 Voltage': 9,
            'Cell 11 Voltage': 10,
            'Cell 12 Voltage': 11,
            'Cell 13 Voltage': 12,
            'Cell 14 Voltage': 13,
            'Pack Current': 14
        }

        if self.data.shape[0] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox.currentText()

            if graphItemIndex < 13:
                yLabel = "Voltage (V)"
            else:
                yLabel = "Current (mA)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.data[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')

    def zoomGraph_2(self):
        """Handler for zooming graph 2"""
        zoomedGraph = self.zoomGraphComboBox_2.currentText()
        zoomedGraphDict = {
            'Cell 1 SoC': 15,
            'Cell 2 SoC': 16,
            'Cell 3 SoC': 17,
            'Cell 4 SoC': 18,
            'Cell 5 SoC': 19,
            'Cell 6 SoC': 20,
            'Cell 7 SoC': 21,
            'Cell 8 SoC': 22,
            'Cell 9 SoC': 23,
            'Cell 10 SoC': 24,
            'Cell 11 SoC': 25,
            'Cell 12 SoC': 26,
            'Cell 13 SoC': 27,
            'Cell 14 SoC': 28,
        }

        if self.data.shape[0] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox_2.currentText()

            yLabel = "SoC (%)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.data[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')

    def zoomGraph_3(self):
        """Handler for zooming graph 3"""
        zoomedGraph = self.zoomGraphComboBox_3.currentText()
        zoomedGraphDict = {
            'Cell 1 SoH': 29,
            'Cell 2 SoH': 30,
            'Cell 3 SoH': 31,
            'Cell 4 SoH': 32,
            'Cell 5 SoH': 33,
            'Cell 6 SoH': 34,
            'Cell 7 SoH': 35,
            'Cell 8 SoH': 36,
            'Cell 9 SoH': 37,
            'Cell 10 SoH': 38,
            'Cell 11 SoH': 39,
            'Cell 12 SoH': 40,
            'Cell 13 SoH': 41,
            'Cell 14 SoH': 42,
        }

        if self.data.shape[0] > 2:
            graphItemIndex = zoomedGraphDict.get(zoomedGraph)
            
            title = self.zoomGraphComboBox_3.currentText()
            
            yLabel = "SoH (%)"

            graphWindow = zoomWindow() # Init zoom window
            graphWindow.labels = [title, yLabel]
            graphWindow.plot.plot(self.data[graphItemIndex]) # Plot Curve
            graphWindow.updateGraph() # Update labels
            graphWindow.exec()
        else:
            QMessageBox.critical(
                self, 'Data error', 'No curve data, please restart plotting')


class SOCPlotWindow(pg.GraphicsLayoutWidget):
    """Window for plotting graphs"""
    def __init__(self):
        super().__init__()

        # Set plot windows
        self.p0 = self.addPlot(title="Cell 1 SoC")
        self.p1 = self.addPlot(title="Cell 2 SoC")
        self.p2 = self.addPlot(title="Cell 3 SoC")
        self.p3 = self.addPlot(title="Cell 4 SoC")

        self.nextRow()
        self.p4 = self.addPlot(title="Cell 5 SoC")
        self.p5 = self.addPlot(title="Cell 6 SoC")
        self.p6 = self.addPlot(title="Cell 7 SoC")
        self.p7 = self.addPlot(title="Cell 8 SoC")

        self.nextRow()
        self.p8 = self.addPlot(title="Cell 9 SoC")
        self.p9 = self.addPlot(title="Cell 10 SoC")
        self.p10 = self.addPlot(title="Cell 11 SoC")
        self.p11 = self.addPlot(title="Cell 12 SoC")

        self.nextRow()
        self.p12 = self.addPlot(title="Cell 13 SoC")
        self.p13 = self.addPlot(title="Cell 14 SoC")

        self.SoCCurves = [
            self.p0,self.p1,self.p2,self.p3,
            self.p4,self.p5,self.p6,self.p7,
            self.p8,self.p9,self.p10,self.p11,
            self.p12,self.p13]

        self.initCurves()

    def initCurves(self):
        """Handler for curve initialisation"""
        for curve in self.SoCCurves:
            curve.setLabel('bottom', "Time (s)")
            curve.setLabel('left', "SoC (%)")
            curve.enableAutoRange(axis='y')


class SOHPlotWindow(pg.GraphicsLayoutWidget):
    """Window for plotting graphs"""
    def __init__(self):
        super().__init__()
        # Set plot windows
        self.p0 = self.addPlot(title="Cell 1 SoH")
        self.p1 = self.addPlot(title="Cell 2 SoH")
        self.p2 = self.addPlot(title="Cell 3 SoH")
        self.p3 = self.addPlot(title="Cell 4 SoH")

        self.nextRow()
        self.p4 = self.addPlot(title="Cell 5 SoH")
        self.p5 = self.addPlot(title="Cell 6 SoH")
        self.p6 = self.addPlot(title="Cell 7 SoH")
        self.p7 = self.addPlot(title="Cell 8 SoH")

        self.nextRow()
        self.p8 = self.addPlot(title="Cell 9 SoH")
        self.p9 = self.addPlot(title="Cell 10 SoH")
        self.p10 = self.addPlot(title="Cell 11 SoH")
        self.p11 = self.addPlot(title="Cell 12 SoH")

        self.nextRow()
        self.p12 = self.addPlot(title="Cell 13 SoH")
        self.p13 = self.addPlot(title="Cell 14 SoH")

        self.SoHCurves = [
            self.p0,self.p1,self.p2,self.p3,
            self.p4,self.p5,self.p6,self.p7,
            self.p8,self.p9,self.p10,self.p11,
            self.p12,self.p13]

        self.initCurves()

    def initCurves(self):
        """Handler for curve initialisation"""
        for curve in self.SoHCurves:
            curve.setLabel('bottom', "Time (s)")
            curve.setLabel('left', "SoH (%)")
            curve.enableAutoRange(axis='y')
