import os
import sys

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

sys.path.append('.')

class cellDataPlotting:
    def __init__(self, folder):
        
        self.folder = folder

    def plotBatteryData(self):

        dataList = []

        fileList = [self.folder + '\\' + file for file in list(os.listdir(self.folder))]
        fileList.sort()

        for fileName in fileList:
            data = pd.read_csv(fileName)
            dataList.append(data)
        
        batteryData = pd.concat(dataList, axis=0, join='outer', ignore_index=True)
        batteryData['Time(s)'] = batteryData['Date'].map(lambda x: x - batteryData.loc[0,'Date'])

        for batteryNumber in range(14):
            batteryData['cellVoltage_' + str(batteryNumber + 1)] = batteryData['cellVoltage_' + str(batteryNumber + 1)].map(lambda x:x / 1000)
            batteryData['cellSoC_' + str(batteryNumber + 1)] = batteryData['cellSoC_' + str(batteryNumber + 1)].map(lambda x:x / 10)
            batteryData['cellSoH_' + str(batteryNumber + 1)] = batteryData['cellSoH_' + str(batteryNumber + 1)].map(lambda x:x / 10)

        fig = make_subplots(rows=2, cols=2, subplot_titles=("Pack Current", 'Cell Voltage', 'Cell SoC', 'Cell SoH'))

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)", row=1, col=1)
        fig.update_yaxes(title_text="Voltage (mV)", row=1, col=2)
        fig.update_yaxes(title_text="SoC (%)", row=2, col=1)
        fig.update_yaxes(title_text="SoH (%)", row=2, col=2)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'], 
                                    mode='lines',
                                    name='packCurrent'),
                                    row=1, col=1)

        for batteryNumber in range(14):
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_' + str(batteryNumber + 1)],
                                    mode='lines',
                                    name='cellVoltage_' + str(batteryNumber + 1)),
                                    row=1, col=2)

            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)], 
                                    mode='lines',
                                    name='cellSoC_' + str(batteryNumber + 1)),
                                    row=2, col=1)
            
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoH_' + str(batteryNumber + 1)], 
                                    mode='lines',
                                    name='cellSoH_' + str(batteryNumber + 1)),
                                    row=2, col=2)

        fig.update_layout(
            title='Battery Data' + self.folder[6:],
            xaxis_title='Time(s)',
            hovermode='x'
        )

        fig.show()
