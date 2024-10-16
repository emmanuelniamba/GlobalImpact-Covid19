import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import country_converter as cc

# Register the page for multi-page Dash apps
dash.register_page(__name__, path='/tourism', name="Tourism Analysis", order=4)

####################### DATASET #############################
# Load the dataset
data = pd.read_csv("data/international-tourist-trips.csv", sep=',')

columns_to_keep = ['Entity','Year','Inbound arrivals of tourists']
data = data[columns_to_keep]

def check_nan_values(df):
  nan_exists = df.isnull().values.any()
  nan_counts = df.isnull().sum().to_dict()
  return nan_exists, nan_counts

nan_exist, nan_counts = check_nan_values(data)

# print("NaN values exist:", nan_exist)
# if nan_exist:
#     print("NaN value counts per column:", nan_counts)

data = data.rename(columns={'Entity': 'location'})
data = data.rename(columns={'Year': 'year'})
data = data.rename(columns={'Inbound arrivals of tourists': 'Nb_tourists'})

data_filtered = data[(data['year'] >= 2018) & (data['year'] <= 2023)]


####################### SCATTER CHART #############################
def create_tourism_line_chart(data):
    fig = px.line(data, 
                x='year', 
                y='Nb_tourists', 
                color='location',
                markers=True)
    return fig

# ####################### WIDGETS #############################
# # Dropdowns for selecting country and year
# country_dropdown = dcc.Dropdown(
#     id="country_dropdown",
#     options=[{"label": country, "value": country} for country in sorted_data['Country Name'].unique()],
#     value="India",  # Default value
#     clearable=False
# )

# year_dropdown = dcc.Dropdown(
#     id="year_dropdown",
#     options=[{"label": str(year), "value": year} for year in sorted_data['year'].unique()],
#     value=2023,  # Default value
#     clearable=False
# )

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.H2("Explore Tourism Growth Over Time", className="fw-bold text-center"),
    html.Br(),
    dcc.Graph(id="tourism", figure=create_tourism_line_chart(data_filtered))
])

# ####################### CALLBACKS ###############################
# @callback(Output("gdp_graph", "figure"), 
#           [Input(data_filtered)])

# def update_gdp_chart(data_filtered):
#     return create_tourism_line_chart(data_filtered)
