import os
import sys

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

sys.path.append('.')


class cellDataPlotting:
    def __init__(self, folder):

        self.folder = folder

    def prepareDataSet(self):
        """Prepare data set for data visualisation"""
        dataList = []

        fileList = [self.folder + '/' +
                    file for file in list(os.listdir(self.folder))]
        fileList.sort()

        for fileName in fileList:
            data = pd.read_csv(fileName)
            dataList.append(data)

        batteryData = pd.concat(
            dataList, axis=0, join='outer', ignore_index=True)
        batteryData['Time(s)'] = batteryData['Date'].map(
            lambda x: x - batteryData.loc[0, 'Date'])

        for batteryNumber in range(14):
            batteryData['cellVoltage_' + str(batteryNumber + 1)] = batteryData['cellVoltage_' + str(
                batteryNumber + 1)].map(lambda x: x / 1000)
            batteryData['cellSoC_' + str(batteryNumber + 1)] = batteryData['cellSoC_' + str(
                batteryNumber + 1)].map(lambda x: x / 10)
            batteryData['cellSoH_' + str(batteryNumber + 1)] = batteryData['cellSoH_' + str(
                batteryNumber + 1)].map(lambda x: x / 10)

        return batteryData

    def plotBatteryData(self):
        """Plot multiple battery data"""
        df = self.prepareDataSet()
        batteryData = df[0:5300]

        fig = make_subplots(rows=2, cols=2, subplot_titles=(
            "Pack Current", 'Cell Voltage', 'Cell SoC', 'Cell SoH', 'Cell CB Control'))

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

    def plotCBControlData(self):
        """Plot CB control signal data"""
        batteryData = self.prepareDataSet()

        # Create a separate trace for each signal in a different subplot
        traces = []

        for batteryNumber in range(14):
            y = batteryData['cellCB_' + str(batteryNumber + 1)]

            trace = go.Scatter(x=batteryData['Time(s)'], y=y,
                               mode='lines', name='cellCB_' + str(batteryNumber + 1))
            
            traces.append(trace)

        fig = make_subplots(rows=14, cols=1, shared_xaxes=True, vertical_spacing=0.02)

        fig.update_yaxes(type="category")

        for i, trace in enumerate(traces):
            fig.add_trace(trace, row=i+1, col=1)

        fig.update_layout(
            title="Cell Balancing Control Signal")

        fig.show()

if __name__ == "__main__":
    cbAndSoCData = 'Data\\Cyclon_2.5Ah_LeadAcid\\24-03-2023'
    cellDataPlotting(cbAndSoCData).plotBatteryData()
    cellDataPlotting(cbAndSoCData).plotCBControlData()
