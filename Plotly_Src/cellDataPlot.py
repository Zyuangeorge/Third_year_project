import os
import sys
# Import enum to define status
from enum import Enum

import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import pandas as pd

sys.path.append('.')


class selectedPowerSupplyDataLines(Enum):
    skiprows = 8328
    nrows = 3880


class selectedBatteryDataLines(Enum):
    LOWER = 7216
    UPPER = 11087


class selectedCBDataLines(Enum):
    LOWER = 0
    UPPER = 5300


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
        # batteryData['Time(s)'] = pd.to_datetime(batteryData['Date'], unit='s')

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
        batteryData = self.prepareDataSet()

        batteryData = batteryData[selectedBatteryDataLines.LOWER.value:selectedBatteryDataLines.UPPER.value]

        batteryData['Time(s)'] = batteryData['Time(s)'] - batteryData['Time(s)'][selectedBatteryDataLines.LOWER.value]

        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'],
                                 mode='lines',
                                 name='packCurrent'),
                      row=1, col=1)
        
        # Add accurate SoC data
        df = self.getAccurateSoC()
        
        fig.add_trace(go.Scatter(x=df.index, y=df['Accurate SoC'],
                                 mode='lines',
                                 name='Accurate SoC'),
                                 row=2, col=2)

        for batteryNumber in range(14):
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellVoltage_' + str(batteryNumber + 1)),
                          row=1, col=2)

            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellSoC_' + str(batteryNumber + 1)),
                          row=2, col=1)

            """ fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoH_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellSoH_' + str(batteryNumber + 1)),
                          row=3, col=1) """

        fig = self.changeStyle(fig, 'Time(s)', "Current (mA)", False)

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)")

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)", row=1, col=1)
        fig.update_yaxes(title_text="Voltage (mV)", row=1, col=2)
        fig.update_yaxes(title_text="SoC (%)", row=2, col=1)
        fig.update_yaxes(title_text="Accurate SoC (%)", row=2, col=2) 
        #fig.update_yaxes(title_text="SoH (%)", row=3, col=1)

        newnames = {
                    'packCurrent': 'Current',
                    'cellVoltage_1': 'Cell 1', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
                    'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
                    'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14',

                    'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
                    'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
                    'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',

                    'Accurate SoC':'Accurate SoC'
                    #'cellSoH_1': 'Cell 1 SoH', 'cellSoH_2': 'Cell 2 SoH', 'cellSoH_3': 'Cell 3 SoH', 'cellSoH_4': 'Cell 4 SoH', 'cellSoH_5': 'Cell 5 SoH',
                    #'cellSoH_6': 'Cell 6 SoH', 'cellSoH_7': 'Cell 7 SoH', 'cellSoH_8': 'Cell 8 SoH', 'cellSoH_9': 'Cell 9 SoH', 'cellSoH_10': 'Cell 10 SoH',
                    #'cellSoH_11': 'Cell 11 SoH', 'cellSoH_12': 'Cell 12 SoH', 'cellSoH_13': 'Cell 13 SoH', 'cellSoH_14': 'Cell 14 SoH',
                    }
        
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

        fig.update_traces(selector=dict(name='Cell 1'), marker=dict(color='blue'))
        fig.update_traces(selector=dict(name='Cell 2'), marker=dict(color='green'))
        fig.update_traces(selector=dict(name='Cell 3'), marker=dict(color='red'))
        fig.update_traces(selector=dict(name='Cell 4'), marker=dict(color='purple'))
        fig.update_traces(selector=dict(name='Cell 5'), marker=dict(color='orange'))
        fig.update_traces(selector=dict(name='Cell 6'), marker=dict(color='yellow'))
        fig.update_traces(selector=dict(name='Cell 7'), marker=dict(color='brown'))
        fig.update_traces(selector=dict(name='Cell 8'), marker=dict(color='pink'))
        fig.update_traces(selector=dict(name='Cell 9'), marker=dict(color='gray'))
        fig.update_traces(selector=dict(name='Cell 10'), marker=dict(color='black'))
        fig.update_traces(selector=dict(name='Cell 11'), marker=dict(color='cyan'))
        fig.update_traces(selector=dict(name='Cell 12'), marker=dict(color='magenta'))
        fig.update_traces(selector=dict(name='Cell 13'), marker=dict(color='olive'))
        fig.update_traces(selector=dict(name='Cell 14'), marker=dict(color='teal'))

        fig.update_traces(showlegend=False, row=2, col=1)

        fig.show()

    def getAccurateSoC(self):

        df = pd.read_csv("E:\\Workspace for VSCode\\Third_year_project\\Data\\PowerSupply\\23-3-2023-Charge-9-40.csv", delimiter=";",skiprows=selectedPowerSupplyDataLines.skiprows.value, nrows=selectedPowerSupplyDataLines.nrows.value)

        # Convert the 'Time' column to datetime format
        df['Time'] = pd.to_datetime(df['Time'])

        df['I actual'] = df['I actual'].str.replace(',', '.').str.replace('A', '').astype(float)

        df['I actual cumsum'] = df['I actual'].cumsum()

        df['Accurate SoC'] = df.iloc[:, 13].apply(lambda x:x/(2.5*36))

        df['Time(s)'] = df['Time'].map(
            lambda x: x - df.loc[0, 'Time'])

        return df
    
    def plotCBControlData(self):
        """Plot CB control signal data"""
        batteryData = self.prepareDataSet()

        batteryData = batteryData[selectedCBDataLines.LOWER.value:selectedCBDataLines.UPPER.value] # [0:5300] is for cell balancing data

        # Create a separate trace for each signal in a different subplot
        traces = []

        for batteryNumber in range(14):
            y = batteryData['cellCB_' + str(batteryNumber + 1)]

            trace = go.Scatter(x=batteryData['Time(s)'], y=y,
                               mode='lines', name='cellCB_' + str(batteryNumber + 1))

            traces.append(trace)

        fig = make_subplots(
            rows=14, cols=1, shared_xaxes=True, vertical_spacing=0.02)

        for i, trace in enumerate(traces):
            fig.add_trace(trace, row=i+1, col=1)

        fig = self.changeStyle(
            fig, "Time (s)", "Cell Balancing Control (On/Off)", True)

        newnames = {'cellCB_1': 'Cell 1', 'cellCB_2': 'Cell 2', 'cellCB_3': 'Cell 3', 'cellCB_4': 'Cell 4', 'cellCB_5': 'Cell 5',
                    'cellCB_6': 'Cell 6', 'cellCB_7': 'Cell 7', 'cellCB_8': 'Cell 8', 'cellCB_9': 'Cell 9', 'cellCB_10': 'Cell 10',
                    'cellCB_11': 'Cell 11', 'cellCB_12': 'Cell 12', 'cellCB_13': 'Cell 13', 'cellCB_14': 'Cell 14'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))
        fig.show()

        fig2 = go.Figure()

        for batteryNumber in range(14):
            fig2.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_' + str(batteryNumber + 1)],
                                      mode='lines',
                                      name='cellVoltage_' + str(batteryNumber + 1)))

        fig2 = self.changeStyle(fig2, "Time (s)", "Cell Voltage (mV)", False)

        newnames = {'cellVoltage_1': 'Cell 1', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
                    'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
                    'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14'}
        fig2.for_each_trace(lambda t: t.update(name=newnames[t.name]))
        fig2.show()

        fig3 = go.Figure()

        for batteryNumber in range(14):
            fig3.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)],
                                      mode='lines',
                                      name='cellSoC_' + str(batteryNumber + 1)))

        fig3 = self.changeStyle(fig3, "Time (s)", "Cell SoC (%)", False)

        newnames = {'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
                    'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
                    'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14'}
        fig3.for_each_trace(lambda t: t.update(name=newnames[t.name]))
        fig3.show()

        # Filter data distorted by the balancing process
        fig4 = go.Figure()
        trendData = batteryData
        trendData.loc[batteryData['cellCB_9'] != 0, :] = np.nan

        for batteryNumber in range(14):
            dataColumn = trendData['cellVoltage_' + str(batteryNumber + 1)]
            
            # Filter outlier 
            mean = dataColumn.mean()
            sigma = dataColumn.std()

            trendData = trendData.loc[(dataColumn >= mean - 3 * sigma) & (
                dataColumn <= mean + 3 * sigma)]

            trendData = trendData.fillna(method='bfill')

            # Median filter
            trendData.loc[:, 'filteredCellVoltage_' + str(batteryNumber + 1)] = trendData.loc[:, 'cellVoltage_' + str(batteryNumber + 1)].rolling(65, center=True).median().values

            fig4.add_trace(go.Scatter(x=trendData['Time(s)'], y=trendData['filteredCellVoltage_' + str(batteryNumber + 1)],
                                      mode='lines',
                                      name='filteredCellVoltage_' + str(batteryNumber + 1)))

        fig4 = self.changeStyle(fig4, "Time (s)", "Cell Voltage (mV)", False)

        newnames = {'filteredCellVoltage_1': 'Cell 1', 'filteredCellVoltage_2': 'Cell 2', 'filteredCellVoltage_3': 'Cell 3', 'filteredCellVoltage_4': 'Cell 4', 'filteredCellVoltage_5': 'Cell 5',
                    'filteredCellVoltage_6': 'Cell 6', 'filteredCellVoltage_7': 'Cell 7', 'filteredCellVoltage_8': 'Cell 8', 'filteredCellVoltage_9': 'Cell 9', 'filteredCellVoltage_10': 'Cell 10',
                    'filteredCellVoltage_11': 'Cell 11', 'filteredCellVoltage_12': 'Cell 12', 'filteredCellVoltage_13': 'Cell 13', 'filteredCellVoltage_14': 'Cell 14'}
        fig4.for_each_trace(lambda t: t.update(name=newnames[t.name]))
        fig4.show()

    def changeStyle(self, fig, xLabel, yLabel, stackPlot):
        # choose the figure font
        font_dict = dict(family='Times New Roman',
                         size=20,
                         color='black'
                         )

        # general figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                          plot_bgcolor='white',  # background color
                          # width=850,  # figure width
                          # height=700,  # figure height
                          # margin=dict(r=20, t=20, b=10)  # remove white space
                          legend=dict(
                              title_font_family="Times New Roman",
                              font=font_dict,
                              bgcolor="White",
                              bordercolor="Black",
                              borderwidth=1
                          )
                          )

        if stackPlot == False:
            fig.update_yaxes(title_text=yLabel,  # axis label
                             showline=True,  # add line at x=0
                             linecolor='black',  # line color
                             linewidth=2.4,  # line size
                             ticks='outside',  # ticks outside axis
                             tickfont=font_dict,  # tick label font
                             mirror='allticks',  # add ticks to top/right axes
                             tickwidth=2.4,  # tick width
                             tickcolor='black',  # tick color
                             gridcolor='lightgray'
                             )

            fig.update_xaxes(title_text=xLabel,
                             showline=True,
                             showticklabels=True,
                             linecolor='black',
                             linewidth=2.4,
                             ticks='outside',
                             tickfont=font_dict,
                             mirror='allticks',
                             tickwidth=2.4,
                             tickcolor='black',
                             gridcolor='lightgray'
                             )
        else:
            # x and y-axis formatting
            fig.update_layout(showlegend=True)

            fig.update_yaxes(
                showline=True,  # add line at x=0
                linecolor='black',  # line color
                linewidth=2.4,  # line size
                mirror='all',  # add ticks to top/right axes
                type="category",
            )

            fig.update_yaxes(title_text='Balancing control signal',
                             row=7, col=1)  # axis label

            fig.update_xaxes(
                showline=True,
                showticklabels=False,
                linecolor='black',
                linewidth=2.4,
                mirror='all',
            )

            fig.update_xaxes(title_text=xLabel,
                             showticklabels=True, row=14, col=1)

        return fig


if __name__ == "__main__":
    cbAndSoCData = 'Data\\Cyclon_2.5Ah_LeadAcid\\24-03-2023'
    charingData = 'Data\\Cyclon_2.5Ah_LeadAcid\\23-03-2023'
    cellDataPlotting(charingData).plotBatteryData()
    cellDataPlotting(cbAndSoCData).plotCBControlData()
