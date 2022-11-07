# Import PySide6 widgets
from PySide6.QtWidgets import QDialog, QApplication, QHBoxLayout, QMessageBox
from PySide6.QtCore import QTimer

# Import pyqtgraph
import pyqtgraph as pg

# Import numpy
import numpy as np

from random import randint

# Import serial library
import serial

class plotWindow(QDialog):
    """Window for plotting graphs"""

    def __init__(self):
        super().__init__()
        
        # Graph titles
        self.titles = ["Battery Data Display", "Time(s)", "Default y axis"]

        # x axis setting
        self.xAxis = list(range(100)) # x-axis values

        # Battery data
        self.batteryData = [randint(0,100) for _ in range(100)] # y-axis values
        self.realtimeData = 0

        # Graph widget
        self.graphWidget = pg.PlotWidget()
        
        # Serial port
        self.serialPort = serial.Serial()
        
        # Set layout
        self.setWindowTitle(self.titles[0])
        self.buildLayout()

        # Add timer
        self.timer = QTimer()
        self.initTimer()

    def setGraph(self):
        # Set background colour
        self.graphWidget.setBackground('w')
        
        # Set x and y axis label
        self.graphWidget.setLabel(axis='bottom', text=self.titles[1])
        self.graphWidget.setLabel(axis='left', text=self.titles[2])

        # Set Graph pen
        self.pen = pg.mkPen(color=(0, 255, 0))

        # Set line
        self.dataLine =  self.graphWidget.plot(self.xAxis, self.batteryData, pen=self.pen)

        # Set graph layout
        graphLayout = QHBoxLayout()
        graphLayout.addWidget(self.graphWidget)

        return graphLayout

    def buildLayout(self):
        graphLayout = self.setGraph()

        # Set window layout
        dialogLayout = QHBoxLayout() # Layout type

        dialogLayout.addLayout(graphLayout)
        self.setLayout(dialogLayout)

    def initTimer(self):
        self.timer.setInterval(200) # Set time interval in milliseconds
        self.timer.timeout.connect(self.updateData)  
        self.timer.start()    

    def updateData(self):
        self.xAxis = self.xAxis[1:]  # Remove the first y element.
        self.xAxis.append(self.xAxis[-1] + 0.5)  # Add a new value 1 higher than the last.

        self.batteryData = self.batteryData[1:]  # Remove the first
        self.batteryData.append(self.realtimeData)  # Add the battery data.

        self.dataLine.setData(self.xAxis, self.batteryData)  # Update the data.

    def updateTitles(self):
        self.setWindowTitle(self.titles[0])
        self.graphWidget.setLabel(axis='bottom', text=self.titles[1])
        self.graphWidget.setLabel(axis='left', text=self.titles[2])
        


if __name__ == "__main__":
    application = QApplication([])
    plotDialog = plotWindow()
    plotDialog.show()
    exit(application.exec())