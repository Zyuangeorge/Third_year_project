import os
import sys
# Import enum to define status
from enum import Enum

import skimage.io as sio
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import pandas as pd

sys.path.append('.')


class selectedPowerSupplyDataLines(Enum):
    skiprows = 0
    nrows = 50000


class selectedBatteryDataLines(Enum):
    LOWER = 0
    #UPPER = 50000
    #UPPER = 7752 # 26-04-2023 Discharge SoH capacity
    UPPER = 5530 # 28-04-2023 Discharge SoH capacity


class selectedCBDataLines(Enum):
    LOWER = 0
    UPPER = 50000


class cellDataPlotting:
    def __init__(self, folder, powerFilePath, batteryCapacity, mostBalancedCell):

        self.folder = str(folder)
        self.powerFilePath = str(powerFilePath)
        self.batteryCapacity = batteryCapacity
        self.mostBalancedCell = str(mostBalancedCell)

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

        batteryData['cellVoltage_5'] = np.nan
        batteryData['cellVoltage_6'] = np.nan
        batteryData['cellVoltage_7'] = np.nan
        batteryData['cellVoltage_8'] = np.nan
        batteryData['cellVoltage_9'] = np.nan
        batteryData['cellVoltage_10'] = np.nan
        batteryData['cellVoltage_11'] = np.nan

        batteryData['cellSoC_5'] = np.nan
        batteryData['cellSoC_6'] = np.nan
        batteryData['cellSoC_7'] = np.nan
        batteryData['cellSoC_8'] = np.nan
        batteryData['cellSoC_9'] = np.nan
        batteryData['cellSoC_10'] = np.nan
        batteryData['cellSoC_11'] = np.nan

        batteryData['cellSoH_5'] = np.nan
        batteryData['cellSoH_6'] = np.nan
        batteryData['cellSoH_7'] = np.nan
        batteryData['cellSoH_8'] = np.nan
        batteryData['cellSoH_9'] = np.nan
        batteryData['cellSoH_10'] = np.nan
        batteryData['cellSoH_11'] = np.nan

        for batteryNumber in range(14):
            batteryData['cellVoltage_' + str(batteryNumber + 1)] = batteryData['cellVoltage_' + str(
                batteryNumber + 1)].map(lambda x: x / 1000)
            batteryData['cellSoC_' + str(batteryNumber + 1)] = batteryData['cellSoC_' + str(
                batteryNumber + 1)].map(lambda x: x / 10)
            batteryData['cellSoH_' + str(batteryNumber + 1)] = batteryData['cellSoH_' + str(
                batteryNumber + 1)].map(lambda x: x / 10)

        return batteryData

    def plotBatteryDataCharge(self):
        """Plot multiple battery data"""
        batteryData = self.prepareDataSet()
        accurateSoCData = self.getAccurateSoC()

        batteryData = batteryData[selectedBatteryDataLines.LOWER.value:
                                  selectedBatteryDataLines.UPPER.value]

        batteryData['Time(s)'] = batteryData['Time(s)'] - \
            batteryData['Time(s)'][selectedBatteryDataLines.LOWER.value]

        # Get SoC error
        for batteryNumber in range(14):
            batteryData['cellSoCError_' + str(batteryNumber + 1)] = batteryData['cellSoC_' + str(
                batteryNumber + 1)] - batteryData['cellSoC_' + str(batteryNumber + 1)][0]
            batteryData['cellSoCError_' + str(batteryNumber + 1)] = batteryData['cellSoCError_' + str(
                batteryNumber + 1)] - accurateSoCData['Accurate SoC']

        # Plot graph
        fig = make_subplots(rows=2, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": False}], [
                            {"secondary_y": False}, {"secondary_y": False}]], vertical_spacing=0.27, horizontal_spacing=0.25)

        for batteryNumber in range(14):
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellVoltage_' + str(batteryNumber + 1)),
                          row=1, col=1, secondary_y=False)

            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellSoC_' + str(batteryNumber + 1)),
                          row=1, col=2)

            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoCError_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellSoCError_' + str(batteryNumber + 1)),
                          row=2, col=1)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'],
                                 mode='lines',
                                 name='packCurrent'),
                      row=1, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=accurateSoCData.index, y=accurateSoCData['Accurate SoC'],
                                 mode='lines',
                                 name='Accurate SoC'),
                      row=2, col=2)

        fig = self.changeStyle(fig, 'Time(s)', "Default", False)

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)</br></br>(a)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)</br></br>(b)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)",
                         row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Voltage (mV)",
                         row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="SoC (%)", row=1, col=2)
        fig.update_yaxes(title_text="SoC Error(%)", row=2, col=1)
        fig.update_yaxes(title_text="Accurate SoC (%)", row=2, col=2)

        newNames = {
            'packCurrent': 'Current',
            'cellVoltage_1': 'Cell 1', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
            'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
            'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14',

            'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
            'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
            'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',

            'cellSoCError_1': 'Cell 1', 'cellSoCError_2': 'Cell 2', 'cellSoCError_3': 'Cell 3', 'cellSoCError_4': 'Cell 4', 'cellSoCError_5': 'Cell 5',
            'cellSoCError_6': 'Cell 6', 'cellSoCError_7': 'Cell 7', 'cellSoCError_8': 'Cell 8', 'cellSoCError_9': 'Cell 9', 'cellSoCError_10': 'Cell 10',
            'cellSoCError_11': 'Cell 11', 'cellSoCError_12': 'Cell 12', 'cellSoCError_13': 'Cell 13', 'cellSoCError_14': 'Cell 14',

            'Accurate SoC': 'Accurate SoC'

        }

        fig.for_each_trace(lambda t: t.update(name=newNames[t.name]))

        fig.update_traces(selector=dict(name='Cell 1'),
                          marker=dict(color='blue'))
        fig.update_traces(selector=dict(name='Cell 2'),
                          marker=dict(color='green'))
        fig.update_traces(selector=dict(name='Cell 3'),
                          marker=dict(color='red'))
        fig.update_traces(selector=dict(name='Cell 4'),
                          marker=dict(color='purple'))
        fig.update_traces(selector=dict(name='Cell 5'),
                          marker=dict(color='orange'))
        fig.update_traces(selector=dict(name='Cell 6'),
                          marker=dict(color='yellow'))
        fig.update_traces(selector=dict(name='Cell 7'),
                          marker=dict(color='brown'))
        fig.update_traces(selector=dict(name='Cell 8'),
                          marker=dict(color='pink'))
        fig.update_traces(selector=dict(name='Cell 9'),
                          marker=dict(color='gray'))
        fig.update_traces(selector=dict(name='Cell 10'),
                          marker=dict(color='black'))
        fig.update_traces(selector=dict(name='Cell 11'),
                          marker=dict(color='cyan'))
        fig.update_traces(selector=dict(name='Cell 12'),
                          marker=dict(color='magenta'))
        fig.update_traces(selector=dict(name='Cell 13'),
                          marker=dict(color='olive'))
        fig.update_traces(selector=dict(name='Cell 14'),
                          marker=dict(color='teal'))

        fig.update_traces(showlegend=False, row=1, col=2)
        fig.update_traces(showlegend=False, row=2, col=1)

        fig.update_layout(hovermode='x',
                          legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.9))

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 710,
                'width': 1050,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        fig.show(config=config)

    def plotBatteryDataDischarge(self, imagePath):
        """Plot multiple battery data"""
        batteryData = self.prepareDataSet()

        batteryData = batteryData[selectedBatteryDataLines.LOWER.value:
                                  selectedBatteryDataLines.UPPER.value]

        batteryData['Time(s)'] = batteryData['Time(s)'] - \
            batteryData['Time(s)'][selectedBatteryDataLines.LOWER.value]

        # Plot graph
        fig = make_subplots(rows=2, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": False}], [
                            {"secondary_y": False, "type": "image", "colspan": 2}, None]], vertical_spacing=0.2, horizontal_spacing=0.25)

        for batteryNumber in range(14):
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellVoltage_' + str(batteryNumber + 1)),
                          row=1, col=1, secondary_y=False)

            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellSoC_' + str(batteryNumber + 1)),
                          row=1, col=2)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'],
                                 mode='lines',
                                 name='packCurrent'),
                      row=1, col=1, secondary_y=True)

        fig = self.changeStyle(fig, 'Time(s)', "Default", False)
        fig.update_traces(showlegend=False, row=1, col=2)

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)</br></br>(a)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)</br></br>(b)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)<br>(d)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)",
                         row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Voltage (mV)",
                         row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="SoC (%)", row=1, col=2)

        newNames = {
            'packCurrent': 'Current',
            'cellVoltage_1': 'Cell 1', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
            'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
            'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14',

            'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
            'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
            'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',
        }

        fig.for_each_trace(lambda t: t.update(name=newNames[t.name]))

        fig.update_traces(selector=dict(name='Cell 1'),
                          marker=dict(color='blue'))
        fig.update_traces(selector=dict(name='Cell 2'),
                          marker=dict(color='green'))
        fig.update_traces(selector=dict(name='Cell 3'),
                          marker=dict(color='red'))
        fig.update_traces(selector=dict(name='Cell 4'),
                          marker=dict(color='purple'))
        fig.update_traces(selector=dict(name='Cell 5'),
                          marker=dict(color='orange'))
        fig.update_traces(selector=dict(name='Cell 6'),
                          marker=dict(color='yellow'))
        fig.update_traces(selector=dict(name='Cell 7'),
                          marker=dict(color='brown'))
        fig.update_traces(selector=dict(name='Cell 8'),
                          marker=dict(color='pink'))
        fig.update_traces(selector=dict(name='Cell 9'),
                          marker=dict(color='gray'))
        fig.update_traces(selector=dict(name='Cell 10'),
                          marker=dict(color='black'))
        fig.update_traces(selector=dict(name='Cell 11'),
                          marker=dict(color='cyan'))
        fig.update_traces(selector=dict(name='Cell 12'),
                          marker=dict(color='magenta'))
        fig.update_traces(selector=dict(name='Cell 13'),
                          marker=dict(color='olive'))
        fig.update_traces(selector=dict(name='Cell 14'),
                          marker=dict(color='teal'))

        # Add image
        img = sio.imread(str(imagePath))
        figm = px.imshow(img)
        fig.add_trace(figm.data[0], 2, 1)
        fig.update_xaxes(title_text=" ", showticklabels=False, row=2, col=1)
        fig.update_yaxes(title_text=" ", showticklabels=False, row=2, col=1)

        fig.update_layout(hovermode='x',
                          legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.9))

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 710,
                'width': 1050,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        fig.show(config=config)

    def plotBatteryDataStateofHealth(self, imagePath):
        """Plot multiple battery data"""
        batteryData = self.prepareDataSet()
        accurateSoCData = self.getAccurateSoC()

        batteryData = batteryData[selectedBatteryDataLines.LOWER.value:
                                  selectedBatteryDataLines.UPPER.value]

        batteryData['Time(s)'] = batteryData['Time(s)'] - \
            batteryData['Time(s)'][selectedBatteryDataLines.LOWER.value]

        # Plot graph
        fig = make_subplots(rows=2, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": False}], [
                            {"secondary_y": False, "type": "image"}, {"secondary_y": False}]], vertical_spacing=0.25, horizontal_spacing=0.25)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_1'],
                                 mode='lines',
                                 name='cellVoltage_1'),
                      row=1, col=1, secondary_y=False)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoH_1'],
                                 mode='lines',
                                 name='cellSoH_1'),
                      row=1, col=2)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'],
                                 mode='lines',
                                 name='packCurrent'),
                      row=1, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=accurateSoCData.index, y=accurateSoCData['I actual cumsum ah'],
                                 mode='lines',
                                 name='integratedCurrent'),
                      row=2, col=2)

        fig = self.changeStyle(fig, 'Time(s)', "Default", False)

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)</br></br>(a)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)</br></br>(b)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)<br>(d)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)",
                         row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Voltage (mV)",
                         row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="SoH (%)", row=1, col=2)
        fig.update_yaxes(title_text="Integrated current (Ah)", row=2, col=2)

        newNames = {
            'packCurrent': 'Current',
            'cellVoltage_1': 'Cell 1 Voltage', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
            'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
            'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14',

            'integratedCurrent': 'Integrated Current',

            'cellSoH_1': 'Cell 1 SoH', 'cellSoH_2': 'Cell 2 SoH', 'cellSoH_3': 'Cell 3 SoH', 'cellSoH_4': 'Cell 4 SoH', 'cellSoH_5': 'Cell 5 SoH',
            'cellSoH_6': 'Cell 6 SoH', 'cellSoH_7': 'Cell 7 SoH', 'cellSoH_8': 'Cell 8 SoH', 'cellSoH_9': 'Cell 9 SoH', 'cellSoH_10': 'Cell 10 SoH',
            'cellSoH_11': 'Cell 11 SoH', 'cellSoH_12': 'Cell 12 SoH', 'cellSoH_13': 'Cell 13 SoH', 'cellSoH_14': 'Cell 14 SoH'
        }

        fig.for_each_trace(lambda t: t.update(name=newNames[t.name]))

        fig.update_traces(selector=dict(name='Cell 1'),
                          marker=dict(color='blue'))
        fig.update_traces(selector=dict(name='Cell 2'),
                          marker=dict(color='green'))
        fig.update_traces(selector=dict(name='Cell 3'),
                          marker=dict(color='red'))
        fig.update_traces(selector=dict(name='Cell 4'),
                          marker=dict(color='purple'))
        fig.update_traces(selector=dict(name='Cell 5'),
                          marker=dict(color='orange'))
        fig.update_traces(selector=dict(name='Cell 6'),
                          marker=dict(color='yellow'))
        fig.update_traces(selector=dict(name='Cell 7'),
                          marker=dict(color='brown'))
        fig.update_traces(selector=dict(name='Cell 8'),
                          marker=dict(color='pink'))
        fig.update_traces(selector=dict(name='Cell 9'),
                          marker=dict(color='gray'))
        fig.update_traces(selector=dict(name='Cell 10'),
                          marker=dict(color='black'))
        fig.update_traces(selector=dict(name='Cell 11'),
                          marker=dict(color='cyan'))
        fig.update_traces(selector=dict(name='Cell 12'),
                          marker=dict(color='magenta'))
        fig.update_traces(selector=dict(name='Cell 13'),
                          marker=dict(color='olive'))
        fig.update_traces(selector=dict(name='Cell 14'),
                          marker=dict(color='teal'))

        # Add image
        img = sio.imread(str(imagePath))
        figm = px.imshow(img)

        fig.add_trace(figm.data[0], 2, 1)
        fig.update_xaxes(title_text=" ", showticklabels=False, row=2, col=1)
        fig.update_yaxes(title_text=" ", showticklabels=False, row=2, col=1)

        fig.update_layout(hovermode='x',
                          legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.9))

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 710,
                'width': 1050,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }
        fig.show(config=config)

    def plotBatteryDataStateofHealthCapacityDischarge(self, imagePath):
        """Plot multiple battery data"""
        batteryData = self.prepareDataSet()

        batteryData = batteryData[selectedBatteryDataLines.LOWER.value:
                                  selectedBatteryDataLines.UPPER.value]

        batteryData['Time(s)'] = batteryData['Time(s)'] - \
            batteryData['Time(s)'][selectedBatteryDataLines.LOWER.value]

        # Plot graph
        fig = make_subplots(rows=2, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": False}], [
                            {"secondary_y": False, "type": "image"}, {"secondary_y": False}]], vertical_spacing=0.25, horizontal_spacing=0.25)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_1'],
                                 mode='lines',
                                 name='cellVoltage_1'),
                      row=1, col=1, secondary_y=False)

        """ for batteryNumber in range(14):
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_' + str(batteryNumber + 1)],
                                     mode='lines',
                                     name='cellVoltage_' + str(batteryNumber + 1)),
                          row=1, col=1, secondary_y=False)

            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoH_' + str(batteryNumber + 1)],
                                 mode='lines',
                                 name='cellSoH_' + str(batteryNumber + 1)),
                      row=1, col=2)
            
            fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)],
                                 mode='lines',
                                 name='cellSoC_' + str(batteryNumber + 1)),
                      row=2, col=2) """
            
              
        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoH_1'],
                                 mode='lines',
                                 name='cellSoH_1'),
                      row=1, col=2)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'],
                                 mode='lines',
                                 name='packCurrent'),
                      row=1, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_1'],
                                 mode='lines',
                                 name='cellSoC_1'),
                      row=2, col=2)

        fig = self.changeStyle(fig, 'Time(s)', "Default", False)

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)</br></br>(a)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)</br></br>(b)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)<br>(d)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)",
                         row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Voltage (mV)",
                         row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="SoH (%)", row=1, col=2)
        fig.update_yaxes(title_text="SoC (%)", row=2, col=2)

        newNames = {
            'packCurrent': 'Current',
            'cellVoltage_1': 'Cell 1 Voltage', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
            'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
            'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14',

            'cellSoC_1': 'Cell 1 SoC', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
            'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
            'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',

            'cellSoH_1': 'Cell 1 SoH', 'cellSoH_2': 'Cell 2', 'cellSoH_3': 'Cell 3', 'cellSoH_4': 'Cell 4', 'cellSoH_5': 'Cell 5',
            'cellSoH_6': 'Cell 6', 'cellSoH_7': 'Cell 7', 'cellSoH_8': 'Cell 8', 'cellSoH_9': 'Cell 9', 'cellSoH_10': 'Cell 10',
            'cellSoH_11': 'Cell 11', 'cellSoH_12': 'Cell 12', 'cellSoH_13': 'Cell 13', 'cellSoH_14': 'Cell 14'
        }

        fig.for_each_trace(lambda t: t.update(name=newNames[t.name]))

        fig.update_traces(selector=dict(name='Cell 1'),
                          marker=dict(color='blue'))
        fig.update_traces(selector=dict(name='Cell 2'),
                          marker=dict(color='green'))
        fig.update_traces(selector=dict(name='Cell 3'),
                          marker=dict(color='red'))
        fig.update_traces(selector=dict(name='Cell 4'),
                          marker=dict(color='purple'))
        fig.update_traces(selector=dict(name='Cell 5'),
                          marker=dict(color='orange'))
        fig.update_traces(selector=dict(name='Cell 6'),
                          marker=dict(color='yellow'))
        fig.update_traces(selector=dict(name='Cell 7'),
                          marker=dict(color='brown'))
        fig.update_traces(selector=dict(name='Cell 8'),
                          marker=dict(color='pink'))
        fig.update_traces(selector=dict(name='Cell 9'),
                          marker=dict(color='gray'))
        fig.update_traces(selector=dict(name='Cell 10'),
                          marker=dict(color='black'))
        fig.update_traces(selector=dict(name='Cell 11'),
                          marker=dict(color='cyan'))
        fig.update_traces(selector=dict(name='Cell 12'),
                          marker=dict(color='magenta'))
        fig.update_traces(selector=dict(name='Cell 13'),
                          marker=dict(color='olive'))
        fig.update_traces(selector=dict(name='Cell 14'),
                          marker=dict(color='teal'))

        """ fig.update_traces(showlegend=False, row=1, col=2)
        fig.update_traces(showlegend=False, row=2, col=2) """

        # Add image
        img = sio.imread(str(imagePath))
        figm = px.imshow(img)

        fig.add_trace(figm.data[0], 2, 1)
        fig.update_xaxes(title_text=" ", showticklabels=False, row=2, col=1)
        fig.update_yaxes(title_text=" ", showticklabels=False, row=2, col=1)

        fig.update_layout(hovermode='x',
                          legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.9))

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 710,
                'width': 1050,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }
        fig.show(config=config)

    def plotBatteryDataStateofHealthCapacity(self):
        """Plot multiple battery data"""
        batteryData = self.prepareDataSet()
        accurateSoCData = self.getAccurateSoC()

        batteryData = batteryData[selectedBatteryDataLines.LOWER.value:
                                  selectedBatteryDataLines.UPPER.value]

        batteryData['Time(s)'] = batteryData['Time(s)'] - \
            batteryData['Time(s)'][selectedBatteryDataLines.LOWER.value]

        # Plot graph
        fig = make_subplots(rows=2, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": False}], [
                            {"secondary_y": False}, {"secondary_y": False}]], vertical_spacing=0.25, horizontal_spacing=0.25)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellVoltage_1'],
                                 mode='lines',
                                 name='cellVoltage_1'),
                      row=1, col=1, secondary_y=False)
        
        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['packCurrent'],
                            mode='lines',
                            name='packCurrent'),
                      row=1, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoH_1'],
                                 mode='lines',
                                 name='cellSoH_1'),
                      row=1, col=2)

        fig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_1'],
                                    mode='lines',
                                    name='cellSoC_1'),
                        row=2, col=1)
        
        fig.add_trace(go.Scatter(x=accurateSoCData.index, y=accurateSoCData['Accurate SoC'],
                                 mode='lines',
                                 name='Accurate SoC'),
                      row=2, col=2)

        fig = self.changeStyle(fig, 'Time(s)', "Default", False)

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)</br></br>(a)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)</br></br>(b)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)<br>(d)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)",
                         row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Voltage (mV)",
                         row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="SoH (%)", row=1, col=2)
        fig.update_yaxes(title_text="SoC (%)", row=2, col=1)
        fig.update_yaxes(title_text="Accurate SoC (%)", row=2, col=2)

        newNames = {
            'packCurrent': 'Current',
            'cellVoltage_1': 'Cell 1 Voltage', 'cellVoltage_2': 'Cell 2', 'cellVoltage_3': 'Cell 3', 'cellVoltage_4': 'Cell 4', 'cellVoltage_5': 'Cell 5',
            'cellVoltage_6': 'Cell 6', 'cellVoltage_7': 'Cell 7', 'cellVoltage_8': 'Cell 8', 'cellVoltage_9': 'Cell 9', 'cellVoltage_10': 'Cell 10',
            'cellVoltage_11': 'Cell 11', 'cellVoltage_12': 'Cell 12', 'cellVoltage_13': 'Cell 13', 'cellVoltage_14': 'Cell 14',

            'cellSoH_1': 'Cell 1 SoH', 'cellSoH_2': 'Cell 2 SoH', 'cellSoH_3': 'Cell 3 SoH', 'cellSoH_4': 'Cell 4 SoH', 'cellSoH_5': 'Cell 5 SoH',
            'cellSoH_6': 'Cell 6 SoH', 'cellSoH_7': 'Cell 7 SoH', 'cellSoH_8': 'Cell 8 SoH', 'cellSoH_9': 'Cell 9 SoH', 'cellSoH_10': 'Cell 10 SoH',
            'cellSoH_11': 'Cell 11 SoH', 'cellSoH_12': 'Cell 12 SoH', 'cellSoH_13': 'Cell 13 SoH', 'cellSoH_14': 'Cell 14 SoH',

            'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
            'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
            'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',
            
            'Accurate SoC': 'Accurate SoC'
        }

        fig.for_each_trace(lambda t: t.update(name=newNames[t.name]))

        fig.update_traces(selector=dict(name='Cell 1'),
                          marker=dict(color='blue'))
        fig.update_traces(selector=dict(name='Cell 2'),
                          marker=dict(color='green'))
        fig.update_traces(selector=dict(name='Cell 3'),
                          marker=dict(color='red'))
        fig.update_traces(selector=dict(name='Cell 4'),
                          marker=dict(color='purple'))
        fig.update_traces(selector=dict(name='Cell 5'),
                          marker=dict(color='orange'))
        fig.update_traces(selector=dict(name='Cell 6'),
                          marker=dict(color='yellow'))
        fig.update_traces(selector=dict(name='Cell 7'),
                          marker=dict(color='brown'))
        fig.update_traces(selector=dict(name='Cell 8'),
                          marker=dict(color='pink'))
        fig.update_traces(selector=dict(name='Cell 9'),
                          marker=dict(color='gray'))
        fig.update_traces(selector=dict(name='Cell 10'),
                          marker=dict(color='black'))
        fig.update_traces(selector=dict(name='Cell 11'),
                          marker=dict(color='cyan'))
        fig.update_traces(selector=dict(name='Cell 12'),
                          marker=dict(color='magenta'))
        fig.update_traces(selector=dict(name='Cell 13'),
                          marker=dict(color='olive'))
        fig.update_traces(selector=dict(name='Cell 14'),
                          marker=dict(color='teal'))

        fig.update_layout(hovermode='x',
                          legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.9))

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 710,
                'width': 1050,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }
        fig.show(config=config)

    def getAccurateSoC(self):

        df = pd.read_csv(self.powerFilePath,
                         delimiter=";", skiprows=selectedPowerSupplyDataLines.skiprows.value, nrows=selectedPowerSupplyDataLines.nrows.value)

        # Convert the 'Time' column to datetime format
        df['Time'] = pd.to_datetime(df['Time'])

        df['I actual'] = df['I actual'].str.replace(
            ',', '.').str.replace('A', '').astype(float)

        df['I actual cumsum'] = df['I actual'].cumsum()

        df['I actual cumsum ah'] = df.iloc[:, 13].apply(
            lambda x: x/(3600))

        df['Accurate SoC'] = df.iloc[:, 13].apply(
            lambda x: x/(self.batteryCapacity*36))

        df['Time(s)'] = df['Time'].map(
            lambda x: x - df.loc[0, 'Time'])

        return df

    def plotCBControlData(self):
        """Plot CB control signal data"""
        batteryData = self.prepareDataSet()

        batteryData = batteryData[selectedCBDataLines.LOWER.value:selectedCBDataLines.UPPER.value]

        # Create a separate trace for each signal in a different subplot
        traces = []

        for batteryNumber in range(14):
            y = batteryData['cellCB_' + str(batteryNumber + 1)]

            trace = go.Scatter(x=batteryData['Time(s)'], y=y,
                               mode='lines', name='cellCB_' + str(batteryNumber + 1))

            traces.append(trace)

        fig = make_subplots(
            rows=14, cols=1, shared_xaxes=True)

        for i, trace in enumerate(traces):
            fig.add_trace(trace, row=i+1, col=1)

        fig = self.changeStyle(
            fig, "Time (s)", "Cell Balancing Control (On/Off)", True)

        newnames = {'cellCB_1': 'Cell 1', 'cellCB_2': 'Cell 2', 'cellCB_3': 'Cell 3', 'cellCB_4': 'Cell 4', 'cellCB_5': 'Cell 5',
                    'cellCB_6': 'Cell 6', 'cellCB_7': 'Cell 7', 'cellCB_8': 'Cell 8', 'cellCB_9': 'Cell 9', 'cellCB_10': 'Cell 10',
                    'cellCB_11': 'Cell 11', 'cellCB_12': 'Cell 12', 'cellCB_13': 'Cell 13', 'cellCB_14': 'Cell 14'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 910,
                'width': 1100,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        fig.show(config=config)

        # ----------------------------------------------------
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
        fig2.show(config=config)

        # -------------------------------------------------
        voltageSoCFig = make_subplots(rows=1, cols=2, horizontal_spacing=0.2)

        trendData = batteryData.copy()
        trendData.loc[batteryData[self.mostBalancedCell] != 0, :] = np.nan

        for batteryNumber in range(14):
            voltageSoCFig.add_trace(go.Scatter(x=batteryData['Time(s)'], y=batteryData['cellSoC_' + str(batteryNumber + 1)],
                                               mode='lines',
                                               name='cellSoC_' + str(batteryNumber + 1)),
                                    row=1, col=1, secondary_y=False)

            dataColumn = trendData['cellVoltage_' + str(batteryNumber + 1)]

            # Filter outlier
            mean = dataColumn.mean()
            sigma = dataColumn.std()

            trendData = trendData.loc[(dataColumn >= mean - 3 * sigma) & (
                dataColumn <= mean + 3 * sigma)]

            trendData = trendData.fillna(method='bfill')

            # Median filter
            trendData.loc[:, 'filteredCellVoltage_' + str(batteryNumber + 1)] = trendData.loc[:, 'cellVoltage_' + str(
                batteryNumber + 1)].rolling(65, center=True).median().values

            voltageSoCFig.add_trace(go.Scatter(x=trendData['Time(s)'], y=trendData['filteredCellVoltage_' + str(batteryNumber + 1)],
                                               mode='lines',
                                               name='filteredCellVoltage_' + str(batteryNumber + 1)),
                                    row=1, col=2, secondary_y=False)

        voltageSoCFig = self.changeStyle(
            voltageSoCFig, "Time (s)", "Default", False)

        voltageSoCFig.update_yaxes(title_text="Cell SoC (%)",
                                   row=1, col=1)
        voltageSoCFig.update_yaxes(title_text="Cell Voltage (mV)",
                                   row=1, col=2)

        newnames = {'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
                    'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
                    'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',
                    'filteredCellVoltage_1': 'Cell 1', 'filteredCellVoltage_2': 'Cell 2', 'filteredCellVoltage_3': 'Cell 3', 'filteredCellVoltage_4': 'Cell 4', 'filteredCellVoltage_5': 'Cell 5',
                    'filteredCellVoltage_6': 'Cell 6', 'filteredCellVoltage_7': 'Cell 7', 'filteredCellVoltage_8': 'Cell 8', 'filteredCellVoltage_9': 'Cell 9', 'filteredCellVoltage_10': 'Cell 10',
                    'filteredCellVoltage_11': 'Cell 11', 'filteredCellVoltage_12': 'Cell 12', 'filteredCellVoltage_13': 'Cell 13', 'filteredCellVoltage_14': 'Cell 14'}

        voltageSoCFig.update_traces(showlegend=False, row=1, col=2)
        voltageSoCFig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

        configVoltageSoCFig = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 505,
                'width': 1100,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        voltageSoCFig.show(config=configVoltageSoCFig)

        return batteryData, trendData

    def changeStyle(self, fig, xLabel, yLabel, stackPlot):
        # choose the figure font
        font_dict = dict(family='Times New Roman',
                         size=24,
                         color='black'
                         )

        # general figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                          plot_bgcolor='white',  # background color
                          # width=850,  # figure width
                          # height=300,  # figure height
                          margin=dict(r=5, t=5, b=5),  # remove white space
                          legend=dict(
                              title_font_family="Times New Roman",
                              font=dict(family='Times New Roman',
                                        size=19,
                                        color='black'
                                        ),
                              bgcolor="White",
                              bordercolor="Black",
                              borderwidth=3,
                              yanchor="top",
                              y=0.99,
                              xanchor="right",
                              x=1.15
                          )
                          )

        if stackPlot == False:
            fig.update_yaxes(title_text=yLabel,  # axis label
                             showline=True,  # add line at x=0
                             linecolor='black',  # line color
                             linewidth=3,  # line size
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
                             linewidth=3,
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
                linewidth=3,  # line size
                mirror='all',  # add ticks to top/right axes
                type="category",
            )

            fig.update_yaxes(title_text='Balancing control signal',
                             row=7, col=1)  # axis label

            fig.update_xaxes(
                showline=True,
                showticklabels=False,
                linecolor='black',
                linewidth=3,
                mirror='all',
            )

            fig.update_xaxes(title_text=xLabel,
                             showticklabels=True, row=14, col=1)

        return fig


if __name__ == "__main__":

    # Lead-acid data
    # 23/3/2023 Broken cell
    # cellDataPlotting('Data\\Cyclon_2.5Ah_LeadAcid\\23-03-2023', 2.5).plotBatteryDataCharge()

    # 24/3/2023 no soc calibration
    # cellDataPlotting('Data\\Cyclon_2.5Ah_LeadAcid\\24-03-2023', 2.5).plotCBControlData()

    # 27/3/2023 with soc calibration, charging data before changing the cells
    ##LeadAcidBatteryData, LeadAcidTrendData = cellDataPlotting('Data\\Cyclon_2.5Ah_LeadAcid\\27-03-2023\\Balancing', "Data\\PowerSupply\\27-3-2023-Charge.csv", 2.5, 'cellCB_9').plotCBControlData()
    #cellDataPlotting('Data\\Cyclon_2.5Ah_LeadAcid\\27-03-2023\\Charging', 2.5).plotBatteryDataCharge()

    # 28/3/2023 charge data
    # cellDataPlotting('Data\\Cyclon_2.5Ah_LeadAcid\\28-03-2023',"Data\\PowerSupply\\28-3-2023-Charge.csv", 2.5).plotBatteryDataCharge()

    # Lithium-ion data
    # 12/4/2023 (Failed CB)
    # cellDataPlotting("Data\\BAK_29_NMC\\12-04-2023","Data\\PowerSupply\\27-3-2023-Charge.csv", 2.9).plotCBControlData()

    # 13/4/2023 (CB with one higher than the other and charging)
    ##lithiumBatteryData, lithiumTrendData = cellDataPlotting("Data\\BAK_29_NMC\\13-04-2023\\Balancing", "Data\\PowerSupply\\13-4-2023-Charge.csv", 2.9, 'cellCB_2').plotCBControlData()
    ##cellDataPlotting("Data\\BAK_29_NMC\\13-04-2023\\Charging", "Data\\PowerSupply\\13-4-2023-Charge.csv", 2.9, 'cellCB_2').plotBatteryDataCharge()

    # 14/4/2023 (Discharging)
    ##cellDataPlotting("Data\\BAK_29_NMC\\14-04-2023\\Discharging", "Data\\PowerSupply\\13-4-2023-Charge.csv", 2.9, 'cellCB_2').plotBatteryDataDischarge("Data\\BAK_29_NMC\\14-04-2023\\SoCData\\dischargeData.jpg")

    # 19/4/2023 (State of health efc test)
    ##cellDataPlotting("Data\\BAK_29_NMC\\18-04-2023\\continuous", "Data\\PowerSupply\\19-4-2023.csv", 2.9, 'cellCB_2').plotBatteryDataStateofHealth("Data\\BAK_29_NMC\\18-04-2023\\SoC\\SoHdata.jpg")

    # 22/4/2023 (State of health capacity test charge)
    ##cellDataPlotting("Data\\BAK_29_NMC\\21-04-2023", "Data\\PowerSupply\\21-4-2023.csv", 2.9, 'cellCB_2').plotBatteryDataStateofHealthCapacity()

    # 24/4/2023 (State of health capacity test discharge failed)
    ##cellDataPlotting("Data\\BAK_29_NMC\\24-04-2023", "Data\\PowerSupply\\21-4-2023.csv", 2.9, 'cellCB_2').plotBatteryDataDischarge("Data\\BAK_29_NMC\\14-04-2023\\SoCData\\dischargeData.jpg")
    
    # 26/4/2023 (State of health capacity test discharge)
    ##cellDataPlotting("Data\\BAK_29_NMC\\26-04-2023\\Discharging", "Data\\PowerSupply\\21-4-2023.csv", 2.9, 'cellCB_2').plotBatteryDataStateofHealthCapacityDischarge("Data\\BAK_29_NMC\\26-04-2023\\SoCData\\dischargeData.jpg")

    # 28/4/2023 (State of health capacity test discharge)
    cellDataPlotting("Data\\BAK_29_NMC\\28-04-2023\\Discharging", "Data\\PowerSupply\\21-4-2023.csv", 2.9, 'cellCB_2').plotBatteryDataStateofHealthCapacityDischarge("Data\\BAK_29_NMC\\28-04-2023\\SoCData\\dischargeData.jpg")

    """ def changeStyle(fig, xLabel, yLabel):
        # choose the figure font
        font_dict = dict(family='Times New Roman',
                         size=24,
                         color='black'
                         )

        # general figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                          plot_bgcolor='white',  # background color
                          # width=850,  # figure width
                          # height=700,  # figure height
                          margin=dict(r=5, t=43, b=5),  # remove white space
                          legend=dict(
                              title_font_family="Times New Roman",
                              font=dict(family='Times New Roman',
                                        size=19,
                                        color='black'
                                        ),
                              bgcolor="White",
                              bordercolor="Black",
                              borderwidth=3,
                              yanchor="top",
                              y=0.99,
                              xanchor="right",
                              x=1.15
                          )
                          )

        fig.update_yaxes(title_text=yLabel,  # axis label
                            showline=True,  # add line at x=0
                            linecolor='black',  # line color
                            linewidth=3,  # line size
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
                            linewidth=3,
                            ticks='outside',
                            tickfont=font_dict,
                            mirror='allticks',
                            tickwidth=2.4,
                            tickcolor='black',
                            gridcolor='lightgray'
                            )

        fig.update_xaxes(title_text=xLabel,
                            showticklabels=True, row=14, col=1)

        return fig

    fig = make_subplots(rows=2, cols=2, vertical_spacing=0.25, horizontal_spacing=0.25)

    for batteryNumber in range(14):
        fig.add_trace(go.Scatter(x=lithiumBatteryData['Time(s)'], y=lithiumBatteryData['cellSoC_' + str(batteryNumber + 1)],
                                 mode='lines',
                                 name='cellSoC_' + str(batteryNumber + 1)),
                      row=1, col=2)

        fig.add_trace(go.Scatter(x=lithiumTrendData['Time(s)'], y=lithiumTrendData['filteredCellVoltage_' + str(batteryNumber + 1)],
                                 mode='lines',
                                 name='filteredCellVoltage_' + str(batteryNumber + 1)),
                      row=1, col=1)

        fig.add_trace(go.Scatter(x=LeadAcidBatteryData['Time(s)'], y=LeadAcidBatteryData['cellSoC_' + str(batteryNumber + 1)],
                                 mode='lines',
                                 name='cellSoC_' + str(batteryNumber + 1)),
                      row=2, col=2)

        fig.add_trace(go.Scatter(x=LeadAcidTrendData['Time(s)'], y=LeadAcidTrendData['filteredCellVoltage_' + str(batteryNumber + 1)],
                                 mode='lines',
                                 name='filteredCellVoltage_' + str(batteryNumber + 1)),
                      row=2, col=1)

    fig = changeStyle(fig, 'Time(s)', "Default")

    # Update xaxis properties
    fig.update_xaxes(title_text="Time(s)</br></br>(a)", row=1, col=1)
    fig.update_xaxes(title_text="Time(s)</br></br>(b)", row=1, col=2)
    fig.update_xaxes(title_text="Time(s)<br>(c)", row=2, col=1)
    fig.update_xaxes(title_text="Time(s)<br>(d)", row=2, col=2)

    # Update yaxis properties
    fig.update_yaxes(title_text="N18650CL-29 Voltage (mV)", row=1, col=1)
    fig.update_yaxes(title_text="N18650CL-29 SoC (%)", row=1, col=2)
    fig.update_yaxes(title_text="0810-0004 Voltage (mV)", row=2, col=1)
    fig.update_yaxes(title_text="0810-0004 SoC (%)", row=2, col=2)

    newnames = {'cellSoC_1': 'Cell 1', 'cellSoC_2': 'Cell 2', 'cellSoC_3': 'Cell 3', 'cellSoC_4': 'Cell 4', 'cellSoC_5': 'Cell 5',
                'cellSoC_6': 'Cell 6', 'cellSoC_7': 'Cell 7', 'cellSoC_8': 'Cell 8', 'cellSoC_9': 'Cell 9', 'cellSoC_10': 'Cell 10',
                'cellSoC_11': 'Cell 11', 'cellSoC_12': 'Cell 12', 'cellSoC_13': 'Cell 13', 'cellSoC_14': 'Cell 14',
                'filteredCellVoltage_1': 'Cell 1', 'filteredCellVoltage_2': 'Cell 2', 'filteredCellVoltage_3': 'Cell 3', 'filteredCellVoltage_4': 'Cell 4', 'filteredCellVoltage_5': 'Cell 5',
                'filteredCellVoltage_6': 'Cell 6', 'filteredCellVoltage_7': 'Cell 7', 'filteredCellVoltage_8': 'Cell 8', 'filteredCellVoltage_9': 'Cell 9', 'filteredCellVoltage_10': 'Cell 10',
                'filteredCellVoltage_11': 'Cell 11', 'filteredCellVoltage_12': 'Cell 12', 'filteredCellVoltage_13': 'Cell 13', 'filteredCellVoltage_14': 'Cell 14'}

    fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

    fig.update_traces(selector=dict(name='Cell 1'),
                          marker=dict(color='blue'))
    fig.update_traces(selector=dict(name='Cell 2'),
                        marker=dict(color='green'))
    fig.update_traces(selector=dict(name='Cell 3'),
                        marker=dict(color='red'))
    fig.update_traces(selector=dict(name='Cell 4'),
                        marker=dict(color='purple'))
    fig.update_traces(selector=dict(name='Cell 5'),
                        marker=dict(color='orange'))
    fig.update_traces(selector=dict(name='Cell 6'),
                        marker=dict(color='yellow'))
    fig.update_traces(selector=dict(name='Cell 7'),
                        marker=dict(color='brown'))
    fig.update_traces(selector=dict(name='Cell 8'),
                        marker=dict(color='pink'))
    fig.update_traces(selector=dict(name='Cell 9'),
                        marker=dict(color='gray'))
    fig.update_traces(selector=dict(name='Cell 10'),
                        marker=dict(color='black'))
    fig.update_traces(selector=dict(name='Cell 11'),
                        marker=dict(color='cyan'))
    fig.update_traces(selector=dict(name='Cell 12'),
                        marker=dict(color='magenta'))
    fig.update_traces(selector=dict(name='Cell 13'),
                        marker=dict(color='olive'))
    fig.update_traces(selector=dict(name='Cell 14'),
                        marker=dict(color='teal'))
    
    fig.update_traces(showlegend=False, row=1, col=2)
    fig.update_traces(showlegend=False, row=2, col=1)
    fig.update_traces(showlegend=False, row=2, col=2)

    fig.update_layout(hovermode='x',
                        legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.9))

    config = {
        'toImageButtonOptions': {
            'format': 'png',  # one of png, svg, jpeg, webp
            'filename': 'custom_image',
            'height': 800,
            'width': 1050,
            'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    fig.show(config=config) """
