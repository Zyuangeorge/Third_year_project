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

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = self.changeStyle(fig)
        
        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Volts'],
                                mode='lines',
                                name='Voltages (V)'), secondary_y=False,)

        fig.add_trace(go.Scatter(x=data['TestTime'], y=data['Amps'], 
                                mode='lines',
                                name='Current (A)'), secondary_y=True,)
        
        fig.update_layout(hovermode='x', legend=dict(orientation="h", yanchor="bottom",y=1.02,xanchor="right",x=1))

        # Set x-axis title
        fig.update_xaxes(title_text="Time (hr)")

        # Set y-axes titles
        fig.update_yaxes(title_text="Voltages (V)", secondary_y=False)
        fig.update_yaxes(title_text="Current (A)", secondary_y=True)

        config = {
            'toImageButtonOptions': {
                'format': 'png',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 910,
                'width': 1100,
                'scale': 6  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        fig.show(config=config)

    def changeStyle(self, fig):
        # choose the figure font
        font_dict = dict(family='Times New Roman',
                        size=18,
                        color='black'
                        )

        # general figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                        plot_bgcolor='white',  # background color
                        width=1200,  # figure width
                        height=750,  # figure height
                        #margin=dict(l=20,t=20,b=10), # set left margin
                        legend=dict(
                            title_font_family="Times New Roman",
                            font=font_dict,
                            bgcolor="White",
                            bordercolor="Black",
                            borderwidth=1
                        )
                        )

        fig.update_yaxes(
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

        fig.update_xaxes(
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
    
ocvPlot = ocvDataPlotting("./Data/OcvData/CLN_char_25deg - 009.csv")
ocvPlot.plotBatteryData()
