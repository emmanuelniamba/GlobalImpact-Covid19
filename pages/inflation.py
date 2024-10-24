# '''
# 4. Inflation and Prices
# Page Name: "Inflation & Prices"

# Purpose: Explore inflation rates during COVID-19, especially the effects of supply chain disruptions.
# Content:
# Comparison of inflation rates across countries.
# Impact of COVID-19 on essential commodities and services.
# Discussion of supply chain challenges and price fluctuations.
# Visualizations:
# Line chart: Inflation rate trends over time.
# Heatmap: Correlation between inflation and other variables (unemployment, trade).
# Bubble chart: Inflation vs. GDP growth vs. population.
# '''

# import pandas as pd
# import dash
# from dash import dcc, html, callback
# import plotly.express as px
# from dash.dependencies import Input, Output
# import country_converter as cc


# dash.register_page(__name__, path = '/inflation', name = "Inflation and Prices", order = 4)


# ####################### DATA #############################

# data = pd.read_csv("data/consumer_prices.csv", sep=',')
# # link to the dataset: https://unctadstat.unctad.org/datacentre/dataviewer/US.Cpi_A

# col_names_changed = {'ref_area.label':'Country', 'sex.label':'Gender', 'time':'Year', 'obs_value':'Unemployment_Rate'}
# data = data[list(col_names_changed.keys())]

# for k,v in col_names_changed.items():
#     data.rename(columns={f'{k}': f'{v}'}, inplace=True)

# '''
# Structure of the dataset:
# For each country, we have the unemployment rates for the years 2014-2024, for three different categories.
# We analyse the total unemployment rate, male unemployment rate and female unemployment rates separately.
# '''
# categories = {"Total":"Sex: Total", "Male":"Sex: Male", "Female":"Sex: Female"}

# def filter_data(category):
#     df = data[data["Gender"] == categories[category]]
#     df = df[["Country","Year","Unemployment_Rate"]]
#     return df


# # ####################### WIDGETS #############################

# # Dropdown for selecting category
# cat_dropdown = dcc.Dropdown(id="cat_column", options = list(categories.keys()), value = "Total", clearable=False)

# # ####################### CHART #############################

# def create_unemployment_chart(col):
#     data_filtered = filter_data(col)
#     fig = px.line(data_filtered, 
#                   x="Year", 
#                   y="Unemployment_Rate", 
#                   color="Country", 
#                   title='Impact of Covid-19 on Unemployment Rate',
#                   labels={'Year': 'Year', 'Unemployment_Rate': 'Unemployment (%)'},
#                   markers=True)
#     return fig

# # ####################### PAGE LAYOUT #############################

# layout = html.Div(children=[
#     html.Br(),
#     html.H2("Impact of Covid-19 on Unemployment Rates", className="fw-bold text-center"),
#     # "Select Country", country_dropdown, 
#     # "Select Year", year_dropdown,
#     html.Br(),
#     html.Div([html.Label("Select Category"), cat_dropdown]),
#     html.Br(),
#     dcc.Graph(id="unemployment_graph")
# ])

# # ####################### CALLBACKS ###############################
# @callback(Output("unemployment_graph", "figure"), 
#           [Input("cat_column", "value")]
#         )

# def update_graph(cat_column):
#     return create_unemployment_chart(cat_column)

