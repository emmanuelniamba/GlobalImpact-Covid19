import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/', name="Homepage", order=0)

# Load the HDI dataset
# Make sure to change the path to where your HDI dataset is located
df = pd.read_csv("data/hdi_data.csv")

# Rename columns to make them more accessible
df = df.rename(columns={'Country': 'Country Name', 'Value': 'HDI'})

####################### PAGE LAYOUT #############################

content = '''
Global Economic Overview

Welcome to the Covid-19 Global Economic Impact Dashboard, an interactive platform that explores COVID-19's profound impact on the global economy. This dashboard provides a high-level summary and detailed breakdown of the pandemic's effects on crucial economic indicators, including GDP growth, unemployment, inflation, trade, and more. Dive into data-backed insights to see how different countries and sectors have responded to and are recovering from the global economic shock of COVID-19.

Key Indicators at a Glance

GDP Decline: Track GDP fluctuations over time and identify the most affected regions, analyzing both immediate impacts and trends toward recovery.
Unemployment Rates: See changes in global and regional employment, highlighting sectors like tourism, manufacturing, and healthcare that faced the hardest hits.
Inflation Trends: Discover how inflation evolved amidst supply chain disruptions, affecting essential commodities and services worldwide.
Explore the Data

Our homepage offers visual snapshots to guide your exploration:

Global Heatmap: Examine the world map highlighting the worst-hit regions by GDP decline and unemployment rates.
Economic Trends: Follow a line graph showcasing global trends in GDP, stock markets, and unemployment rates over time, providing context for the economic challenges and resilience witnessed since the start of the pandemic.
Each section of DAnalysis goes deeper into specific areas, from trade to government responses, giving a comprehensive understanding of COVID-19’s economic legacy. Start your journey here and uncover the global economic story through data.



'''

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Home"),
        "",
        html.Br(), html.Br(),
        "",
    ]),

    # HDI heatmap
    dcc.Graph(id='hdi-world-map'),

    html.Div(children=[
        html.Br(),
        content,
        "", html.Br(),
        "",
        html.Br(), html.Br(),
        html.B(""),
        html.Br(),
        html.B(""),
    ])
    
], className="p-4 m-2", style={"background-color": "#e3f2fd"})

# Callback to update the map with HDI data
@dash.callback(
    Output('hdi-world-map', 'figure'),
    Input('hdi-world-map', 'id')  # Static input for page load
)
def update_map(_):
    fig = px.choropleth(
        df,
        locations='Country Name',
        locationmode='country names',  # Use country names
        color='HDI',
        hover_name='Country Name',
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'HDI': 'HDI'},
        title='Human Development Index (HDI) by Country',
        range_color=(0, 1)  # Set color scale range for HDI from 0 to 1
    )
    
    fig.update_geos(projection_type="mercator")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    return fig
