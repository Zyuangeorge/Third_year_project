import sys

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

sys.path.append('.')

class ocvDataPlotting:
    def __init__(self, fileName):
        
        self.fileName = fileName

    def plotBatteryData(self):

        data = pd.read_csv(self.fileName, header=2, index_col=0)

        """ data['Amps (mA)'] = data['Amps'].map(lambda x: x * 1000)
        data['Volts (mV)'] = data['Volts'].map(lambda x: x * 1000)

        fig = make_subplots(rows=2, cols=2, subplot_titles=("Cell Current", 'Cell Voltage', 'Cell Ah', 'Cell Wh'))

        # Update xaxis properties
        fig.update_xaxes(title_text="Time(s)", row=1, col=1)
        fig.update_xaxes(title_text="Time(s)", row=1, col=2)
        fig.update_xaxes(title_text="Time(s)", row=2, col=1)
        fig.update_xaxes(title_text="Time(s)", row=2, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Current (mA)", row=1, col=1)
        fig.update_yaxes(title_text="Voltage (mV)", row=1, col=2)
        fig.update_yaxes(title_text="Amp-hr (Ah)", row=2, col=1)
        fig.update_yaxes(title_text="Watt-hr (wh)", row=2, col=2) """

        """ fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Amps (mA)'], 
                                    mode='lines',
                                    name='Current (mA)'),
                                    row=1, col=1)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Volts (mV)'],
                                mode='lines',
                                name='Voltages (mV)'),
                                row=1, col=2)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Amp-hr'], 
                                mode='lines',
                                name='Amp-hr (Ah)'),
                                row=2, col=1)
        
        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Watt-hr'], 
                                mode='lines',
                                name='Watt-hr (Wh)'),
                                row=2, col=2) """

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Volts'],
                                mode='lines',
                                name='Voltages (V)'), secondary_y=False,)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Amps'], 
                                mode='lines',
                                name='Current (A)'), secondary_y=True,)

        fig.update_layout(title='Battery SoC-OCV Data', hovermode='x', legend=dict(orientation="h", yanchor="bottom",y=1.02,xanchor="right",x=1))

        # Set x-axis title
        fig.update_xaxes(title_text="Time (hr)")

        # Set y-axes titles
        fig.update_yaxes(title_text="Voltages (V)", secondary_y=False)
        fig.update_yaxes(title_text="Current (A)", secondary_y=True)

        fig.show()

ocvPlot = ocvDataPlotting("./Data/OcvData/CLN_char_25deg - 009.csv")
ocvPlot_2 = ocvDataPlotting("./Data/OcvData/BAK-2.9-char-25C - 009.csv")
ocvPlot.plotBatteryData()
ocvPlot_2.plotBatteryData()
