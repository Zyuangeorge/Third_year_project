import sys

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

sys.path.append('.')

class ocvDataPlotting():
    def __init__(self, fileName):
        
        self.fileName = fileName

    def plotBatteryData(self):

        data = pd.read_csv(self.fileName, header=2, index_col=0)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Volts'],
                                mode='lines',
                                name='Voltages (V)'), secondary_y=False,)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Amps'], 
                                mode='lines',
                                name='Current (A)'), secondary_y=True,)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Temp 1'], 
                                mode='lines',
                                name='Temperature (C)'), secondary_y=False,)

        fig.update_layout(title='Battery Voltage/Current-Time Data', hovermode='x', legend=dict(orientation="h", yanchor="bottom",y=1.02,xanchor="right",x=1))

        # Set x-axis title
        fig.update_xaxes(title_text="Time (s)")

        # Set y-axes titles
        fig.update_yaxes(title_text="Voltages (V)", secondary_y=False)
        fig.update_yaxes(title_text="Current (A)", secondary_y=True)

        fig.show()

ocvPlot = ocvDataPlotting("D:\Project Data\MP_Cycle_Testing\Full_Test_Data\BAK_29\BAK_29_1_200.csv")

ocvPlot.plotBatteryData()
