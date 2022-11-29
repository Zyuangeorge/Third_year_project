import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import (QComboBox, QDialog, QHBoxLayout, QMessageBox,
                               QPushButton, QVBoxLayout)


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
        self.nextRow()
        self.ICTempP = self.addPlot(title="IC Temperature")
        self.packVoltageP = self.addPlot(title="Pack Voltage")
        self.packCurrentP = self.addPlot(title="Pack Current")

        self.voltageCurves = [
            self.p0,self.p1,self.p2,self.p3,
            self.p4,self.p5,self.p6,self.p7,
            self.p8,self.p9,self.p10,self.p11,
            self.p12,self.p13]

        # self.setPlotPanels()
        self.initCurves()
        self.setGraphs()

    def initCurves(self):
        """Handler for curve initialisation"""
        for curve in self.voltageCurves:
            curve.setLabel('bottom', "Time (s) * 5")
            curve.setLabel('left', "Voltage (V)")
        
        self.ICTempP.setLabel('bottom', "Time (s) * 5")
        self.ICTempP.setLabel('left', "Temperature (°C)")

        self.packVoltageP.setLabel('bottom', "Time (s) * 5")
        self.packVoltageP.setLabel('left', "Voltage (V)")

        self.packCurrentP.setLabel('bottom', "Time (s) * 5")
        self.packCurrentP.setLabel('left', "Current (mA)")

    def setGraphs(self):
        """Handler for setting panels"""
        for curve in self.voltageCurves:
            curve.autoRange()

        self.packVoltageP.autoRange()

        self.ICTempP.autoRange()

        self.packCurrentP.autoRange()


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
        self.plot.setLabel('bottom', "Time (s) * 5")

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

        self.canvas = plotWindow()

        self.title = "Loaded file graphs"

        self.initGraph()
    
    def initGraph(self):
        """Handler for initialisation graph window"""

        self.setWindowTitle(self.title)

        layout = QVBoxLayout()

        graphLayout = QHBoxLayout()
        graphLayout.addWidget(self.canvas)

        plotButtonLayout = QHBoxLayout()
        
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
        self.zoomGraphComboBox.addItem('Pack Current')

        self.zoomButton = QPushButton("Zoom Graph")

        plotButtonLayout.addWidget(self.zoomGraphComboBox)
        plotButtonLayout.addWidget(self.zoomButton)

        layout.addLayout(graphLayout)
        layout.addLayout(plotButtonLayout)

        # Connect zoom button functions
        self.zoomButton.clicked.connect(self.zoomGraph)

        self.setLayout(layout)
    
    def loadGraphData(self, readFile):
        """Handler for loading curve data"""

        readFile = readFile.drop('Date', axis=1) # Remove time column to get value

        self.data = readFile.values # Set data frame as matrix

        self.data = np.array(self.data) # Transfer matrix to numpy matrix

        self.data = np.transpose(self.data) # Transpose the matrix

        for j in range(0,14):
            self.canvas.voltageCurves[j].plot(list(i / 1000000 for i in self.data[j + 1])) # Set voltage data in order

        self.canvas.packVoltageP.plot(list(i / 1000000 for i in self.data[0]))
        
        self.canvas.ICTempP.plot(list(i / 10 for i in self.data[15]))

        self.canvas.packCurrentP.plot(list(i for i in self.data[16]))

        self.canvas.setGraphs()
    
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
            'Pack Current': 16
        }
        if self.data.shape[1] > 2:
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
            if graphItemIndex < 15:
                graphWindow.plot.plot(list(i / 1000000 for i in self.data[graphItemIndex])) # Plot Curve
            elif graphItemIndex == 15:
                graphWindow.plot.plot(list(i / 10 for i in self.data[graphItemIndex]))
            else:
                graphWindow.plot.plot(list(i for i in self.data[graphItemIndex]))

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
        self.setGraphs()

    def initCurves(self):
        """Handler for curve initialisation"""
        for curve in self.SoCCurves:
            curve.setLabel('bottom', "Time (s) * 5")
            curve.setLabel('left', "SoC (%)")
        
    def setGraphs(self):
        """Handler for setting panels"""
        for curve in self.SoCCurves:
            curve.autoRange()

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
        self.setGraphs()

    def initCurves(self):
        """Handler for curve initialisation"""
        for curve in self.SoHCurves:
            curve.setLabel('bottom', "Time (s) * 5")
            curve.setLabel('left', "SoH (%)")
        
    def setGraphs(self):
        """Handler for setting panels"""
        for curve in self.SoHCurves:
            curve.autoRange()