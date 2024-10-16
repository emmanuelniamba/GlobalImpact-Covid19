import pandas as pd
import dash
from dash import html, dcc
import plotly.graph_objects as go
from sklearn.datasets import load_wine

dash.register_page(__name__, path='/dataset', name="Dataset", order=1)


####################### LOAD DATASET #############################
df = pd.read_csv("data/pmi_unemployment_data.csv")
#wine = load_wine()
#wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)

def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, align='left'),
        cells=dict(values=df.values.T, align='left'))
    ]
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
    return fig

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.H2("Dataset Explorer", className="fw-bold text-center"),
    dcc.Graph(id="dataset", figure=create_table()),
])