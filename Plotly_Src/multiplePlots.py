# Import functions in other folders
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from PySide6.QtCore import QDateTime
import numpy as np
import pandas as pd
import sys
import gc
import os

# Expend file path
sys.path.append('.')

class DataPlotting():
    def __init__(self, batteryData) -> None:
        self.batteryData = batteryData
        self.app = Dash(__name__)


class Battery():
    def __init__(self, type, rawData, cycleData) -> None:
        self.rawData = rawData  # Battery dataset path
        self.cycleNumber = cycleData  # Cycle number data
        self.type = type  # Type data

    def getCapacity(self):
        """Capacity data handler"""
        # Capacity data for battery 1
        self.capacity_1 = self.rawData[0:self.cycleNumber,
                                       0] / self.rawData[0, 0] * 100.0
        # Capacity data for battery 2
        self.capacity_2 = self.rawData[self.cycleNumber:,
                                       0] / self.rawData[self.cycleNumber, 0] * 100.0

    def getEfficiency(self):
        """Efficiency data handler"""
        # Efficiency data for battery 1
        self.efficiency_1 = self.rawData[0:self.cycleNumber,
                                         1] / self.rawData[0:self.cycleNumber, 2] * 100.0
        # Efficiency data for battery 2
        self.efficiency_2 = self.rawData[self.cycleNumber:,
                                         1] / self.rawData[self.cycleNumber:, 2] * 100.0

    def getInternalResistance(self):
        """Internal resistance data handler"""
        pass

    def returnData(self):
        """Handler for returning overall data"""
        data_1 = np.empty(shape=(self.cycleNumber, 5), dtype=np.float32)
        data_1[:,0] = np.array(list(range(self.cycleNumber)))
        data_1[:,1] = self.capacity_1
        data_1[:,2] = self.efficiency_1
        data_1[:,3] = np.zeros(self.cycleNumber)
        data_1[:,4] = np.full(self.cycleNumber, 1.0)

        data_2 = np.empty(shape=(self.rawData.shape[0] - self.cycleNumber, 5), dtype=np.float32)
        data_2[:,0] = np.array(list(range(0, self.rawData.shape[0] - self.cycleNumber)))
        data_2[:,1] = self.capacity_2
        data_2[:,2] = self.efficiency_2
        data_2[:,3] = np.zeros(self.rawData.shape[0] -self.cycleNumber)
        data_2[:,4] = np.full(self.rawData.shape[0] -self.cycleNumber, 2.0)

        # Create output dataframe
        data = np.concatenate((data_1, data_2), axis=0)
        colName = ['Cyc#', 'Capacity', 'Efficiency',
                   'InternalResistance', 'BatteryNo']
        outputData = pd.DataFrame(data=data, columns=colName, dtype=np.float32)
        outputData['BatteryType'] = self.type

        return outputData


class Dataset():
    def __init__(self, dataPath) -> None:
        self.dataPath = dataPath  # Dataset path
        self.filePath = []  # List of file paths
        self.batteryType = []  # Battery types
        self.batteries = []  # list of batteries
        # Error dictionary
        self.error = {'Position': [], 'Cycle': [], 'Condition': []}

    def getBatteryInfo(self):
        """Handler for getting get battery information"""
        self.batteryType = os.listdir(self.dataPath)

        print("\n")
        print("Battery Types: ")
        print(self.batteryType)
        print("\n")

        for type in self.batteryType:
            # This is the folder path of each battery
            prePath = str(self.dataPath + "\\" + type)
            self.filePath.append([os.path.join(prePath, file) for file in os.listdir(
                prePath + "\\")])  # Get each csv file path according to the battery type

    def filterBatteryCapAndEffData(self, rawData, file):
        """Handler for filtering battery capacity and efficiency data"""
        # Total cycle number of the battery
        totalCycle = int(rawData['Cyc#'].max())

        # Discharging point and Charging point
        # [0] is capacity data
        # [1] is watt-hr data
        pointDischarging = np.zeros((2,), dtype=np.float32)
        pointCharging = np.zeros((2,), dtype=np.float32)

        # Capacity and efficiency data
        # Column 0 is capacity data
        # Column 1 is discharging watt-hr data
        # Column 2 is charging watt-hr data
        dataSet = np.zeros((totalCycle, 3), dtype=np.float32)

        for cycle in range(totalCycle):
            # Find discharging data
            # Filter the data based on these conditions
            filteredData = rawData.loc[
                (rawData['Cyc#'] == float(cycle)) &
                (rawData['Amps'] < 0.0) &
                (rawData['Volts'] < 3.0) &
                (rawData['Volts'] > 2.99) &
                (rawData['ES'] > 120.0)]

            if filteredData.shape[0] == 1:  # There should only be one point
                pointDischarging[0] = filteredData['Amp-hr'].values[0]
                pointDischarging[1] = filteredData['Watt-hr'].values[0]
            else:
                # If there is an error in the data, using the maximum capacity value as the capacity data in this cycle
                pointDischarging[0] = rawData.loc[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['ES'] > 120.0), 'Amp-hr'].max()
                pointDischarging[1] = rawData.loc[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['ES'] > 120.0), 'Watt-hr'].max()

                # Record the error
                self.error['Position'].append(file[47:]) # Remove the previous path
                self.error['Cycle'].append(cycle)
                self.error['Condition'].append("Discharging")

            # Find charging data
            try:
                # Filter the data based on these conditions and combine the index into a list
                indexList = rawData[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['Amps'] > 0.0) &
                    (rawData['ES'] > 120.0)].index.tolist()

                for index in indexList:
                    if rawData.loc[index + 1, 'Cyc#'] == cycle + 1:
                        pointCharging[0] = rawData.loc[index, 'Amp-hr']
                        pointCharging[1] = rawData.loc[index, 'Watt-hr']

            except:
                # If there is no such data then using the maximum capacity value as the capacity data in this cycle
                pointCharging[0] = rawData.loc[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['ES'] > 120.0), 'Amp-hr'].max()
                pointCharging[1] = rawData.loc[
                    (rawData['Cyc#'] == float(cycle)) &
                    (rawData['ES'] > 120.0), 'Watt-hr'].max()

                # Record the error
                self.error['Position'].append(file[47:])
                self.error['Cycle'].append(cycle)
                self.error['Condition'].append("Charging")

            # Combine data
            dataSet[cycle][0] = (pointDischarging[0] + pointCharging[0]) * 0.5
            dataSet[cycle][1] = pointDischarging[1]
            dataSet[cycle][2] = pointCharging[1]

        return dataSet

    def getBatteryData(self, name, fileList):
        """Handler for getting raw data for one type of battery"""

        # Create an numpy array to store capacity and efficiency data for two batteries with the same type
        capAndEffData = np.empty((1, 3), dtype=np.float32)

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
                # Complete instruction
                dataLoading += 1
                print("\rComplete: %.0f %%" %
                      (dataLoading * 100 / dataLoadingTotal), end="")

                batteryData = pd.read_csv(file, header=2, usecols=[
                    'Cyc#', 'Step', 'Amp-hr', 'Watt-hr', 'Amps', 'Volts', 'ES'], dtype=np.float32)

                capAndEffValue = self.filterBatteryCapAndEffData(
                    batteryData, file)

                capAndEffData = np.append(
                    capAndEffData, capAndEffValue, axis=0)

            if i == 0:
                # Record cycle number for the first battery
                cycleData = capAndEffData.shape[0] - 1

        # Delete row 1 values
        capAndEffData = np.delete(capAndEffData, 0, axis=0)

        return capAndEffData, cycleData

    def instanceBatteries(self):
        for i in range(len(self.batteryType)):
            # Get the battery data based on the battery type
            capAndEffData, cycleData = self.getBatteryData(
                self.batteryType[i], self.filePath[i])

            battery = Battery(self.batteryType[i], capAndEffData, cycleData)
            battery.getCapacity()
            battery.getEfficiency()
            battery.getInternalResistance()

            self.batteries.append(battery)

        self.error = pd.DataFrame(self.error)
        print("\n")
        print("Error:")
        print(self.error)
        print("\n")

    def exportErrorLog(self):
        outputDir = 'Third_year_project/Data/Error'

        self.error = pd.DataFrame(columns=['A', 'B', 'C'], index=[0,1,2])

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        time = QDateTime.currentDateTime()
        timeInfo = time.toString("dd-MM-yyyy-mm-hh")
        fileName = outputDir + "/" + str(timeInfo) + ".csv"

        try:
            self.error.to_csv(fileName, index=False, line_terminator='\n')
        except:
            print("\n")
            print("Output error log error!")

        gc.collect()  # Collect garbage

    def combineData(self):
        """Handler for combining all the battery data"""
        outputData = pd.DataFrame()

        for battery in self.batteries:
            batteryData = battery.returnData()
            
            outputData = pd.concat([outputData, batteryData], axis=0,
                                   join='outer', ignore_index=True)
            print(outputData)


if __name__ == "__main__":
    data = Dataset("D:\Project Data\MP_Cycle_Testing\Full_Test_Data")
    data.getBatteryInfo()
    data.instanceBatteries()
    data.exportErrorLog()
    data.combineData()
