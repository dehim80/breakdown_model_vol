from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

app.layout = html.Div([

    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):

    df = pd.read_csv('./hist2022-07-28-(20-20-58)sec.csv')

    fig = go.Figure(go.Candlestick(
        x=df['time'],
        open=df['open'],
        close=df['close'],
        low = df['low'],
        high=df['high']


    ))
    fig.update_layout(margin=dict(t=0,b=0,l=200,r=200))
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


app.run_server(debug=True)