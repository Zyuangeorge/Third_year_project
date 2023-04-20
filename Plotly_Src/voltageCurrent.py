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
        fig = self.changeStyle(fig)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Volts'],
                                 mode='lines',
                                 name='Voltages (V)'), secondary_y=False,)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Amps'],
                                 mode='lines',
                                 name='Current (A)'), secondary_y=True,)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Temp 1'],
                                 mode='lines',
                                 name='Temperature (C)'), secondary_y=False,)

        fig.update_layout(hovermode='x',
                          legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=0.9))

        # Set x-axis title
        fig.update_xaxes(title_text="Time (s)")

        # Set y-axes titles
        fig.update_yaxes(title_text="Voltages (V)", secondary_y=False)
        fig.update_yaxes(title_text="Current (A)", secondary_y=True)

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 500,
                'width': 600,
                'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        fig.show(config=config)

    def changeStyle(self, fig):
        # choose the figure font
        font_dict = dict(family='Times New Roman',
                         size=24,
                         color='black'
                         )

        # general figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                          plot_bgcolor='white',  # background color
                          width=1200,  # figure width
                          height=750,  # figure height
                          margin=dict(l=5, t=5, b=5),  # set left margin
                          legend=dict(
                              title_font_family="Times New Roman",
                              font=dict(family='Times New Roman',
                                        size=19,
                                        color='black'
                                        ),
                              bgcolor="White",
                              bordercolor="Black",
                              borderwidth=1
                          )
                          )

        fig.update_yaxes(
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

        fig.update_xaxes(
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

        return fig


ocvPlot = ocvDataPlotting(
    "D:\Project Data\MP_Cycle_Testing\Full_Test_Data\MOLI_42\MOLI_42_1_200.csv")

ocvPlot.plotBatteryData()
