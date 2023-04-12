import gc
import os
import sys
import webbrowser
from datetime import datetime
from enum import Enum
from threading import Timer

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, dependencies, html

# Expend file path
sys.path.append('.')


class thresholdSetting(Enum):
    MINIMUMVOLTAGE = 3.0
    ESTHRESHOLD = 120.0


class DataPlotting():
    def __init__(self, batteryData) -> None:
        self.batteryData = batteryData
        self.app = Dash(__name__)
        # App callback
        self.app.callback(
            dependencies.Output(component_id='battery-graph',
                                component_property='figure'),
            [dependencies.Input(component_id='battery_data',
                                component_property='value'),
             dependencies.Input(component_id='battery_number',
                                component_property='value'),
             dependencies.Input(component_id='battery_type',
                                component_property='value'),
             dependencies.Input(component_id='show_trendline',
                                component_property='value')]
        )(self.update_graphs)

        # Graph colour setting
        self.colours = {
            'background': '#E0EEEE',
            'text': '#000000'
        }

        # Graph Download config
        self.config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 910,
                'width': 1100,
                'scale': 6  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        # Layout setting
        self.app.layout = html.Div([
            # Left side toolbar
            html.Div([
                html.H1(
                    children='Data Plotting for Batteries - Zhe',
                    style={
                        'textAlign': 'left',
                        'color': self.colours['text'],
                        'fontSize': 15
                    }
                ),
                html.Label('Batteries Data', style={
                           'color': self.colours['text']}),
                dcc.Dropdown(
                    id="battery_data",
                    options=[{'label': val, 'value': val} for val in [
                        'Capacity', 'Efficiency', 'InternalResistance_Discharge', 'InternalResistance_Charge']],
                    value=['Capacity'],
                    multi=True
                ),

                html.Label('Batteries Type', style={
                           'color': self.colours['text']}),
                dcc.Dropdown(
                    id="battery_type",
                    options=[{'label': val, 'value': val}
                             for val in self.batteryData['BatteryType'].unique()],
                    value=self.batteryData['BatteryType'].unique(),
                    multi=True
                ),

                html.Label('Battery Number', style={
                           'color': self.colours['text']}),
                dcc.Checklist(
                    id="battery_number",
                    options=[{'label': val, 'value': val}
                             for val in self.batteryData['BatteryNo'].unique()],
                    value=[1.0],
                    inline=True
                ),

                dcc.Checklist(
                    id='show_trendline',
                    options=[{'label': 'Show Trendline', 'value': 'show'}],
                    value=[]
                ),

            ], style={
                'width': '18%',
                'float': 'left',
                'position': 'fixed',
                'padding': '10px',
                'height': '100%',
                'background-color': self.colours['background']
            }),

            # Right side graph
            html.Div([
                dcc.Graph(id='battery-graph', config=self.config)
            ], style={
                'width': '80%',
                'float': 'right',
                'height': '100%',
            })
        ])

    def update_graphs(self, battery_data, battery_number, battery_type, show_trendline):
        """Handler used to update graph based on the user action"""
        # Filter the data based on battery type
        filtered_data = self.batteryData[self.batteryData['BatteryNo'].isin(battery_number) &
                                         self.batteryData['BatteryType'].isin(battery_type)]

        # Define X and Y axis name
        xAxis = 'Cyc#'
        yAxis = filtered_data[battery_data].columns

        # Create figure
        fig = px.line(filtered_data,
                      x=xAxis,
                      y=yAxis,
                      color=filtered_data['BatteryType'],
                      line_dash=filtered_data['BatteryNo'],
                      markers=False,
                      # template='simple_white',
                      )

        # Add trendline
        if show_trendline == ['show']:
            for data in battery_data:
                fig.add_traces(px.scatter(filtered_data, x=xAxis,
                                          y=data, color=filtered_data['BatteryType'], symbol=filtered_data['BatteryNo'], trendline="lowess").data)

            for i in range(len(battery_number)*len(battery_data)*len(battery_type)):
                fig.data[i].update(visible=False)

            trendLineData = fig.data[-len(battery_number)
                                     * len(battery_type)*2+1::2]

            for traceData in trendLineData:
                traceData.update(showlegend=True)

            # Improve visualisation
            fig.update_traces(visible=False, selector=dict(mode="markers"))

            trendLine_2 = []
            for k, trace in enumerate(fig.data):
                if trace.mode is not None and trace.mode == 'lines' and '2.0' in trace.name:
                    trendLine_2.append(k)
            for id in trendLine_2:
                fig.data[id].update(line={'dash': 'dot'})

            del trendLine_2
            gc.collect()

        fig = self.changeStyle(fig, "Cycle", "Nominal Value (%)")

        return fig

    def changeStyle(self, fig, xLabel, yLabel):
        # choose the figure font
        font_dict = dict(family='Times New Roman',
                         size=18,
                         color='black'
                         )

        # general figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                          plot_bgcolor='white',  # background color
                          yaxis_range=[50, 140],
                          width=1200,  # figure width
                          height=750,  # figure height
                          margin=dict(l=20, t=20, b=10),  # set left margin
                          legend=dict(
                              title_font_family="Times New Roman",
                              font=font_dict,
                              bgcolor="White",
                              bordercolor="Black",
                              borderwidth=1
                          )
                          )

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

        return fig

    def autoOpen(self):
        """Handler used to open the graph automatically"""
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://127.0.0.1:8050')


class Battery():
    def __init__(self, type, rawData, cycleData) -> None:
        self.rawData = rawData  # Battery dataset path
        self.cycleNumber = cycleData  # Cycle number data
        self.type = type  # Type data
        # Error dictionary
        self.error = {'BatteryType': [], 'BatterNumber': [],
                      'Cycle': [], 'DataType': [], 'DataValue': []}

    def getCapacity(self):
        """Capacity data handler"""
        # Calculate the nominal capacity of the battery : (Current Capacity Ah) / (Initial Capacity Ah)
        self.capacity_1 = self.rawData[0:self.cycleNumber,
                                       0] / self.rawData[0, 0] * 100.0

        self.capacity_2 = self.rawData[self.cycleNumber:,
                                       0] / self.rawData[self.cycleNumber, 0] * 100.0

    def getEfficiency(self):
        """Efficiency data handler"""
        # Calculate the efficiency of the battery: (Discharging Efficiency Wh/Charging Efficiency Wh) * 100%
        self.efficiency_1 = self.rawData[0:self.cycleNumber,
                                         1] / self.rawData[0:self.cycleNumber, 2] * 100.0

        self.efficiency_2 = self.rawData[self.cycleNumber:,
                                         1] / self.rawData[self.cycleNumber:, 2] * 100.0

    def getInternalResistance(self):
        """Internal resistance data handler"""
        # Calculate the nominal internal resistance of the battery : (Current average IR) / (Initial average IR)
        # IR for battery 1
        # Discharge DCIR
        self.internalResistance_1_D = self.rawData[0:self.cycleNumber,
                                                   3] / self.rawData[0, 3] * 100.0

        # Charge DCIR
        self.internalResistance_1_C = self.rawData[0:self.cycleNumber,
                                                   4] / self.rawData[0, 4] * 100.0

        # IR for battery 2
        # Discharge DCIR
        self.internalResistance_2_D = self.rawData[self.cycleNumber:,
                                                   3] / self.rawData[self.cycleNumber, 3] * 100.0

        # Charge DCIR
        self.internalResistance_2_C = self.rawData[self.cycleNumber:,
                                                   4] / self.rawData[self.cycleNumber, 4] * 100.0

    def returnData(self):
        """Handler for organising the data"""
        # Data for battery 1
        # [0] Cycle number
        # [1] Capacity
        # [2] Efficiency
        # [3] Discharge internal resistance
        # [4] Charge internal resistance
        # [5] Battery number
        data_1 = np.empty(shape=(self.cycleNumber, 6), dtype=np.float32)
        data_1[:, 0] = np.array(list(range(self.cycleNumber)))
        data_1[:, 1] = self.capacity_1
        data_1[:, 2] = self.efficiency_1
        data_1[:, 3] = self.internalResistance_1_D
        data_1[:, 4] = self.internalResistance_1_C
        data_1[:, 5] = np.full(self.cycleNumber, 1.0)

        data_2 = np.empty(
            shape=(self.rawData.shape[0] - self.cycleNumber, 6), dtype=np.float32)
        data_2[:, 0] = np.array(
            list(range(0, self.rawData.shape[0] - self.cycleNumber)))  # Change the start of the cycle number from 1
        data_2[:, 1] = self.capacity_2
        data_2[:, 2] = self.efficiency_2
        data_2[:, 3] = self.internalResistance_2_D
        data_2[:, 4] = self.internalResistance_2_C
        data_2[:, 5] = np.full(self.rawData.shape[0] - self.cycleNumber, 2.0)

        # Create output dataframe
        # Combine the battery data for 1 and 2 in vertical axis
        data = np.concatenate((data_1, data_2), axis=0)
        colName = ['Cyc#', 'Capacity', 'Efficiency',
                   'InternalResistance_Discharge', 'InternalResistance_Charge', 'BatteryNo']
        outputData = pd.DataFrame(data=data, columns=colName, dtype=np.float32)
        outputData['BatteryType'] = self.type

        # Data cleaning, record all the error data
        for x in outputData.index:
            if outputData.loc[x, "Capacity"] > 110 or outputData.loc[x, "Capacity"] < 0 or outputData.loc[x, "Capacity"] == np.nan:
                self.error['BatteryType'].append(
                    outputData.loc[x, "BatteryType"])
                self.error['BatterNumber'].append(
                    outputData.loc[x, "BatteryNo"])
                self.error['Cycle'].append(outputData.loc[x, 'Cyc#'])
                self.error['DataType'].append("Capacity")
                self.error['DataValue'].append(outputData.loc[x, 'Capacity'])

            if outputData.loc[x, "Efficiency"] > 110 or outputData.loc[x, "Efficiency"] < 0 or outputData.loc[x, "Efficiency"] == np.nan:
                self.error['BatteryType'].append(
                    outputData.loc[x, "BatteryType"])
                self.error['BatterNumber'].append(
                    outputData.loc[x, "BatteryNo"])
                self.error['Cycle'].append(outputData.loc[x, 'Cyc#'])
                self.error['DataType'].append("Efficiency")
                self.error['DataValue'].append(outputData.loc[x, 'Efficiency'])

            if outputData.loc[x, "InternalResistance_Discharge"] > 250 or outputData.loc[x, "InternalResistance_Discharge"] < 0 or outputData.loc[x, "InternalResistance_Discharge"] == np.nan:
                self.error['BatteryType'].append(
                    outputData.loc[x, "BatteryType"])
                self.error['BatterNumber'].append(
                    outputData.loc[x, "BatteryNo"])
                self.error['Cycle'].append(outputData.loc[x, 'Cyc#'])
                self.error['DataType'].append("InternalResistance_Discharge")
                self.error['DataValue'].append(
                    outputData.loc[x, 'InternalResistance_Discharge'])

            if outputData.loc[x, "InternalResistance_Charge"] > 250 or outputData.loc[x, "InternalResistance_Charge"] < 0 or outputData.loc[x, "InternalResistance_Charge"] == np.nan:
                self.error['BatteryType'].append(
                    outputData.loc[x, "BatteryType"])
                self.error['BatterNumber'].append(
                    outputData.loc[x, "BatteryNo"])
                self.error['Cycle'].append(outputData.loc[x, 'Cyc#'])
                self.error['DataType'].append("InternalResistance_Charge")
                self.error['DataValue'].append(
                    outputData.loc[x, 'InternalResistance_Charge'])

        # self.exportErrorLog()
        del self.error
        gc.collect()

        del self.rawData, self.cycleNumber, self.type
        del self.capacity_1, self.capacity_2, self.efficiency_1, self.efficiency_2, self.internalResistance_1_D, self.internalResistance_1_C, self.internalResistance_2_D, self.internalResistance_2_C
        del data_1, data_2, data, colName
        gc.collect()

        return outputData

    def exportErrorLog(self):
        """Handler used for outputting the error log to the Data/Error folder"""
        outputDir = './Data/Error'

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        time = datetime.now()
        timeInfo = time.strftime("%d-%m-%Y-%H-%M-%S")
        fileName = outputDir + "/" + \
            str(timeInfo) + "-" + str(self.type) + ".csv"

        try:
            self.error = pd.DataFrame(self.error)
            print("\n")
            print("Error:")
            print(self.type)
            print("See error log for detailed information.")
            self.error.to_csv(fileName, index=False, line_terminator='\n')
        except:
            print("\n")
            print("Output error log error!")

        del self.error
        gc.collect()


class Dataset():
    def __init__(self, dataPath) -> None:
        self.dataPath = dataPath  # Dataset path
        self.filePath = []  # List of file paths
        self.batteryType = []  # Battery types
        self.batteries = []  # list of batteries

    def getBatteryInfo(self):
        """Handler for getting get battery information"""
        self.batteryType = os.listdir(self.dataPath)

        print("\n")
        print("Battery Types: ")
        print(self.batteryType)
        print("\n")

        for type in self.batteryType:
            # This is the path of each battery data
            prePath = str(self.dataPath + "\\" + type)
            # Combine all the paths into one list
            self.filePath.append([os.path.join(prePath, file) for file in os.listdir(
                prePath + "\\")])  # Get each csv file path according to the battery type

    def filterOutData(self, rawData, file):
        """Handler for filtering battery capacity and efficiency data"""
        # Total cycle number of the battery
        totalCycle = int(rawData['Cyc#'].max())

        # Discharging point and Charging point
        # Row 0 is capacity data
        # Row 1 is watt-hr data
        # Row 2 is voltage point 1 for DCIR calculation (Before switching off or current step)
        # Row 3 is voltage point 2 for DCIR calculation
        # Row 4 is current point 1 for DCIR calculation (Before switching off or current step)
        # Row 5 is current point 2 for DCIR calculation
        dischargingPoints = np.zeros((6,), dtype=np.float32)
        chargingPoints = np.zeros((6,), dtype=np.float32)

        # Output data set
        # Column 0 is capacity data
        # Column 1 is discharging watt-hr data
        # Column 2 is charging watt-hr data
        # Column 3 is discharging DCIR data
        # Column 4 is charging DCIR data
        dataSet = np.zeros((totalCycle, 5), dtype=np.float32)

        for cycle in range(totalCycle):
            # Find discharging data
            try:
                # Filter the data based on these conditions and combine the index into a list
                indexList_1 = rawData[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['Amps'] < 0.0) &
                    (rawData['Volts'] < thresholdSetting.MINIMUMVOLTAGE.value) &
                    (rawData['Volts'] > (thresholdSetting.MINIMUMVOLTAGE.value - 0.01)) &
                    (rawData['ES'] > thresholdSetting.ESTHRESHOLD.value)].index.tolist()

                for index in indexList_1:
                    # If the current value in the next line is 0
                    if rawData.loc[index + 1, 'Amps'] == 0 and rawData.loc[index + 1, 'ES'] == 0:
                        dischargingPoints[0] = rawData.loc[index, 'Amp-hr']
                        dischargingPoints[1] = rawData.loc[index, 'Watt-hr']
                        # The calculated internal resistance is Ro, calculated from current stop
                        # Voltage before current switching off
                        dischargingPoints[2] = rawData.loc[index, 'Volts']
                        # Voltage after current switching off
                        dischargingPoints[3] = rawData.loc[index + 1, 'Volts']
                        # Current before current switching off
                        dischargingPoints[4] = rawData.loc[index, 'Amps']
                        # Current after current switching off
                        dischargingPoints[5] = rawData.loc[index + 1, 'Amps']
            except:
                # If there is an error in the data, set the value to none
                dischargingPoints[0] == np.nan
                dischargingPoints[1] == np.nan
                dischargingPoints[2] == np.nan
                dischargingPoints[3] == np.nan
                dischargingPoints[4] == np.nan
                dischargingPoints[5] == np.nan

            # Find charging data
            try:
                # Filter the data based on these conditions and combine the index into a list
                indexList_2 = rawData[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['Amps'] > 0.0) &
                    (rawData['ES'] > thresholdSetting.ESTHRESHOLD.value)].index.tolist()

                indexList_3 = rawData[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['Amps'] == 0.0) &
                    (rawData['ES'] > thresholdSetting.ESTHRESHOLD.value)].index.tolist()

                for index in indexList_2:
                    # If next line is a new cycle
                    if rawData.loc[index + 1, 'Cyc#'] == cycle + 1 and rawData.loc[index + 1, 'ES'] == 0:
                        chargingPoints[0] = rawData.loc[index, 'Amp-hr']
                        chargingPoints[1] = rawData.loc[index, 'Watt-hr']

                for index in indexList_3:
                    # If next line is the start of charging process
                    if rawData.loc[index + 1, 'Amps'] > 0 and rawData.loc[index + 1, 'ES'] == 0:
                        # The calculated internal resistance is Ro, calculated from current step
                        # Voltage before current step
                        chargingPoints[2] = rawData.loc[index, 'Volts']
                        # Voltage after current step
                        chargingPoints[3] = rawData.loc[index + 1, 'Volts']
                        # Current before current step
                        chargingPoints[4] = rawData.loc[index, 'Amps']
                        # Current after current step
                        chargingPoints[5] = rawData.loc[index + 1, 'Amps']
            except:
                chargingPoints[0] == np.nan
                chargingPoints[1] == np.nan
                chargingPoints[2] == np.nan
                chargingPoints[3] == np.nan
                chargingPoints[4] == np.nan
                chargingPoints[5] == np.nan

            # Combine data
            # Calculate capacity data
            dataSet[cycle][0] = (dischargingPoints[0] +
                                 chargingPoints[0]) * 0.5

            # Assign efficiency data
            dataSet[cycle][1] = dischargingPoints[1]
            dataSet[cycle][2] = chargingPoints[1]

            # Calculate internal resistance data
            dataSet[cycle][3] = (dischargingPoints[3] - dischargingPoints[2]) / \
                (dischargingPoints[5] - dischargingPoints[4])
            dataSet[cycle][4] = (
                chargingPoints[3] - chargingPoints[2]) / (chargingPoints[5] - chargingPoints[4])

        del rawData, file, indexList_1, indexList_2, indexList_3
        del dischargingPoints, chargingPoints, totalCycle
        gc.collect()

        return dataSet

    def getBatteryData(self, name, fileList):
        """Handler for getting raw data for one type of battery"""

        # Create an numpy array to store capacity, efficiency and internal resistance data for two batteries with the same type
        filteredData = np.empty((1, 5), dtype=np.float32)

        # Index used to sort the battery 1 and 2
        index = len(self.dataPath) + len(name) * 2 + 2

        for i in range(2):
            print("\nBattery Type: " + name + "_" + str(i + 1))
            # Create battery data file name list for battery 1 and 2
            batteryDataList = list(filter(lambda x: (
                x[index:(index + 3)] == '_' + str(i + 1) + '_' and x[-4:] == '.csv'), fileList))

            # Sort the data in the cycle order
            batteryDataList.sort(key=lambda x: int(x[(index + 3): -4]))

            dataLoading = 0
            dataLoadingTotal = len(batteryDataList)

            for file in batteryDataList:
                # User instruction
                dataLoading += 1
                print("\rComplete: %.0f %%" %
                      (dataLoading * 100 / dataLoadingTotal), end="")

                # Read CSV file
                batteryData = pd.read_csv(file, header=2, usecols=[
                    'Cyc#', 'Step', 'Amp-hr', 'Watt-hr', 'Amps', 'Volts', 'ES'], dtype=np.float32)

                filteredDataValue = self.filterOutData(
                    batteryData, file)

                # Combine all the capacity and efficiency data
                filteredData = np.append(
                    filteredData, filteredDataValue, axis=0)

                del batteryData, filteredDataValue
                gc.collect()

            if i == 0:
                # Record cycle number for the first battery
                cycleData = filteredData.shape[0] - 1

        # Delete row 1 values, (All the values are 0)
        filteredData = np.delete(filteredData, 0, axis=0)

        return filteredData, cycleData

    def instanceBatteries(self):
        """Handler used to instance the batteries"""
        for i in range(len(self.batteryType)):
            # Get the battery data based on the battery type
            filteredData, cycleData = self.getBatteryData(
                self.batteryType[i], self.filePath[i])

            battery = Battery(self.batteryType[i], filteredData, cycleData)
            battery.getCapacity()
            battery.getEfficiency()
            battery.getInternalResistance()

            self.batteries.append(battery)

            del filteredData, cycleData, battery
            gc.collect()

    def combineData(self):
        """Handler for combining all the battery data"""
        outputData = pd.DataFrame()

        for battery in self.batteries:
            batteryData = battery.returnData()

            # Combine all the data in the vertical axis
            outputData = pd.concat([outputData, batteryData], axis=0,
                                   join='outer', ignore_index=True)

            del batteryData

        del self.batteries, self.batteryType, self.filePath, self.dataPath
        gc.collect()

        return outputData


if __name__ == "__main__":
    dataset = Dataset("D:\Project Data\MP_Cycle_Testing\Full_Test_Data")
    dataset.getBatteryInfo()
    dataset.instanceBatteries()
    data = dataset.combineData()
    plotPage = DataPlotting(data)
    Timer(1, plotPage.autoOpen).start()
    plotPage.app.run_server(debug=False)
