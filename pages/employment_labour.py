
import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import country_converter as cc


dash.register_page(__name__, path = '/employment_labour', name = "Employment & Labour Marker", order = 40)


####################### DATA #############################

data = pd.read_csv("data/unemployment.csv", sep=',')
# link to the dataset: https://rshiny.ilo.org/dataexplorer0/?lang=en&segment=indicator&id=UNE_2EAP_SEX_AGE_RT_A

col_names_changed = {'ref_area.label':'Country', 'sex.label':'Gender', 'time':'Year', 'obs_value':'Unemployment_Rate'}
data = data[list(col_names_changed.keys())]

for k,v in col_names_changed.items():
    data.rename(columns={f'{k}': f'{v}'}, inplace=True)

'''
Structure of the dataset:
For each country, we have the unemployment rates for the years 2014-2024, for three different categories.
We analyse the total unemployment rate, male unemployment rate and female unemployment rates separately.
'''
categories = {"Total":"Sex: Total", "Male":"Sex: Male", "Female":"Sex: Female"}

def filter_data(category):
    df = data[data["Gender"] == categories[category]]
    df = df[["Country","Year","Unemployment_Rate"]]
    return df


# ####################### WIDGETS #############################

# Dropdown for selecting category
cat_dropdown = dcc.Dropdown(id="cat_column", options = list(categories.keys()), value = "Total", clearable=False)

# ####################### CHART #############################

def create_unemployment_chart(col):
    data_filtered = filter_data(col)
    fig = px.line(data_filtered, 
                  x="Year", 
                  y="Unemployment_Rate", 
                  color="Country", 
                  title='Impact of Covid-19 on Unemployment Rate',
                  labels={'Year': 'Year', 'Unemployment_Rate': 'Unemployment (%)'},
                  markers=True)
    return fig

# ####################### PAGE LAYOUT #############################

layout = html.Div(children=[
    html.Br(),
    html.H2("Impact of Covid-19 on Unemployment Rates", className="fw-bold text-center"),
    # "Select Country", country_dropdown, 
    # "Select Year", year_dropdown,
    html.Br(),
    html.Div([html.Label("Select Category"), cat_dropdown]),
    html.Br(),
    dcc.Graph(id="unemployment_graph")
])

# ####################### CALLBACKS ###############################
@callback(Output("unemployment_graph", "figure"), 
          [Input("cat_column", "value")]
        )

def update_graph(cat_column):
    return create_unemployment_chart(cat_column)


'''

3. Employment and Labor Market
Page Name: "Employment & Labor Market"

Purpose: Focus on how COVID-19 affected global employment, labor force participation, and unemployment rates.

Content:
Comparative analysis of unemployment rates across countries.
Relationship between GDP and unemployment rate (Phillips Curve).
Impact on different sectors (e.g., tourism, healthcare).

Visualizations:
Bar chart: Country-wise unemployment rates during and after COVID.
Scatter plot: GDP vs. unemployment rate.
Time-series plot: Unemployment trends across countries or regions.

'''
