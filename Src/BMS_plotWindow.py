# Import PySide6 widgets
from PySide6.QtWidgets import QHBoxLayout

# Import pyqtgraph
import pyqtgraph as pg

import numpy as np

class plotWindow(pg.GraphicsLayoutWidget):
    """Window for plotting graphs"""

    def __init__(self):
        super().__init__()
        
        # Battery data
        self.batteryDataBuffer = [] # Data buffer

        # Panel list
        self.voltagePanels = []
        
        self.setPlotPanels()
        self.setGraphs()

    def setPlotPanels(self):
        """Handler for setting battery data graphs"""

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
        self.ICTempP = self.addPlot(title="Pack Voltage")
        self.packVoltageP = self.addPlot(title="IC Temperature")

        self.voltageCurves = (
            self.p0,self.p1,self.p2,self.p3,
            self.p4,self.p5,self.p6,self.p7,
            self.p8,self.p9,self.p10,self.p11,
            self.p12,self.p13)

    def setGraphs(self):
        """Handler for setting panels"""
        for curve in self.voltageCurves:
            # Set background colour
            curve.autoRange()

        self.packVoltageP.autoRange()
        self.ICTempP.autoRange()

    def updateThresholdLines(self, voltageThreshold, tempThreshold, packVoltageThreshold):
        """Handler for adding threshold lines"""
        pen = pg.mkPen(color=(255, 0, 0))

        for curve in self.voltageCurves:
            curve.addLine(y=voltageThreshold[0],pen=pen)
            curve.addLine(y=voltageThreshold[1],pen=pen)

        self.ICTempP.addLine(y=tempThreshold[0],pen=pen)
        self.ICTempP.addLine(y=tempThreshold[1],pen=pen)

        self.packVoltageP.addLine(y=packVoltageThreshold[0],pen=pen)
        self.packVoltageP.addLine(y=packVoltageThreshold[1],pen=pen)
