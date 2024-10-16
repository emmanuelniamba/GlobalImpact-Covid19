import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
from sklearn.datasets import load_wine

dash.register_page(__name__, path='/distribution', name="Distribution", order=2)

####################### LOAD DATASET #############################
df = pd.read_csv("data/pmi_unemployment_data.csv")
#wine = load_wine()
#wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)


####################### HISTOGRAM ###############################
def create_population_chart(country="australia", date="2021-06-01"):
    filtered_df = df[(df.country==country) & (df.date<date)]
    filtered_df = filtered_df.sort_values(by="unemployment rate", ascending=False)

    fig = px.bar(filtered_df, x="country", y="unemployment rate", color="country",
                   title="{} on {}".format(country, date),
                   text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

####################### WIDGETS ################################
# This decides data for the dropdowns in different tabs
continents = df.country.unique()
dates = df["date"].unique()

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="australia",clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=dates, value="2020-01-01",clearable=False)

# year_map = dcc.Dropdown(id="year_map", options=dates, value="2021-06-01",clearable=False)
# var_map = dcc.Dropdown(id="var_map", options=["Population", "GDP per Capita", "Life Expectancy"], value="Life Expectancy",clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.H2("Explore Distribution of Feature Values", className="fw-bold text-center"),
    html.Br(),
    dcc.Tab([html.Br(), "Name of dropdown here - country", cont_population, "Name of dropdown here - dates", year_population, html.Br(),
        dcc.Graph(id="population")], label="Name of Dropdown-Population"),
    dcc.Graph(id="histogram")
])

####################### CALLBACKS ################################
@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
def update_histogram(dist_column):
    return create_population_chart(dist_column)
