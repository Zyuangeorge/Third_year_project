import plotly.graph_objs as go
import plotly.subplots as sp

# Define the data for the digital signals
data = [
    {"name": "Signal 1", "data": [0, 0, 1, 1, 0, 1, 1, 0]},
    {"name": "Signal 2", "data": [1, 1, 0, 0, 1, 0, 0, 1]}
]

# Create a separate trace for each signal in a different subplot
traces = []
for i, signal in enumerate(data):
    y = signal["data"]
    trace = go.Scatter(x=list(range(len(y))), y=y, mode="lines+markers", name=signal["name"])
    traces.append(trace)

fig = sp.make_subplots(rows=len(data), cols=1)

for i, trace in enumerate(traces):
    fig.add_trace(trace, row=i+1, col=1)

fig.update_layout(title="Digital Timing Diagram", xaxis=dict(title="Time"))

fig.show()
