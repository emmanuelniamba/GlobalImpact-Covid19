import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import country_converter as cc
import logging


dash.register_page(__name__, path = '/Consumption_data.csv', name = "Private_Consumption on the world", order = 14)

dataT = pd.read_csv("data/international-tourist-trips.csv", sep=',')

####################### DATA #############################

logger = logging.getLogger('country_converter')
logger.setLevel(logging.ERROR)

dataR = pd.read_csv("data/Consumption_data.csv", sep=',', skiprows=4, header=None)

def load_process(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    new_data = data[selected_columns]
    data.columns = data.columns.astype(str)
    value_vars = [col for col in data.columns[4:] if col != 'nan']
    melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='Consumption')
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    filtered_data = melted_data[melted_data['year'].isin([2018, 2019, 2020, 2021, 2022, 2023])]
    unique_years = filtered_data['year'].unique()
    sorted_data = filtered_data.sort_values('Country Name')
    sorted_data = filtered_data.sort_values(['Country Name', 'year'])
    sorted_data['year'] = sorted_data['year'].astype(int)
    sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
    sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')
    nan_count_continent = sorted_data['continent'].isnull().sum()
    nan_count_consumption = sorted_data['Consumption'].isnull().sum()
    nan_counts_by_year = sorted_data.groupby('year')['Consumption'].apply(lambda x: x.isnull().sum())
    sorted_data = sorted_data[sorted_data['continent'] != 'not found']
    return sorted_data

def continent_Consumption(data):
    consumption_by_continent_year = data.groupby(['continent', 'year'])['Consumption'].sum().reset_index()
    return consumption_by_continent_year

def iso_country(data):
    data['iso_alpha'] = cc.convert(names=sorted_data['location'], to='ISO3')
    return data

def process_tourism_data(df):
    # Step 1: Select relevant columns
    columns_to_keep = ['Entity', 'Year', 'Inbound arrivals of tourists']
    df = df[columns_to_keep]

    # Step 2: Check for NaN values
    nan_exists = df.isnull().values.any()
    nan_counts = df.isnull().sum().to_dict()
    
    # Print NaN information
    print("NaN values exist:", nan_exists)
    if nan_exists:
        print("NaN value counts per column:", nan_counts)

    # Step 3: Rename columns
    df = df.rename(columns={'Entity': 'location'})
    df = df.rename(columns={'Year': 'year'})
    df = df.rename(columns={'Inbound arrivals of tourists': 'Nb_tourists'})

    # Step 4: Filter data for the years 2018 to 2023
    df_filtered = df[(df['year'] >= 2018) & (df['year'] <= 2023)]
    
    return df_filtered
def continent_Tourist(data):
    consumption_by_continent_year = data.groupby(['continent', 'year'])['Nb_tourists'].sum().reset_index()
    return consumption_by_continent_year


# Example usage:
data_tourist = process_tourism_data(dataT)
# ####################### WIDGETS #############################

# Dropdown for 1
sorted_data = load_process(dataR)
data1 = continent_Consumption(sorted_data)

data_columns1 = {
    "Consumption": data1["Consumption"],
    "Year": data1["year"],
    "Continent": data1["continent"]
}

categories1 = list(data_columns1.keys())

cat_dropdown1 = dcc.Dropdown(
    id="cat_column",
    options=categories1,
    value=categories1[0],
    clearable=False
)

# Graph id 1
graph1 = dcc.Graph(id="Consumption_graph1")

# ####################### CHART #############################

def update_graph_continent(data):
    fig = px.line(data, x='year', y='Consumption', color='continent')
    fig.update_layout(title='Consumption by Continent and Year')
    return fig

# Dropdown for 2
sorted_data = load_process(dataR)
data2 = iso_country(sorted_data)
data_columns2 = {
    "Consumption": data2["Consumption"],
    "Year": data2["year"],
    "iso_alpha": data2["iso_alpha"]
}

categories2 = list(data_columns2.keys())

cat_dropdown2 = dcc.Dropdown(
    id="cat_column",
    options=categories2,
    value=categories2[0],
    clearable=False
)

# Graph id 2
graph2 = dcc.Graph(id="Consumption_graph2")

# ####################### CHART #############################

def plot_choropleth_map(data):
    fig = px.choropleth(
        data,
        locations="iso_alpha",
        color="Consumption",  
        hover_name="location",
        animation_frame="year",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    return fig


# Dropdown for 3
sorted_data = load_process(dataR)
combined_data = pd.merge(sorted_data[['continent','year','location']], data_tourist, on=['year','location'], how='inner')
data3=continent_Tourist(combined_data)

data_columns3 = {
    "Nb_tourists": data3["Nb_tourists"],
    "Year": data3["year"],
    "Continent": data3["continent"]
}

categories3 = list(data_columns3.keys())

cat_dropdown3 = dcc.Dropdown(
    id="cat_column",
    options=categories3,
    value=categories3[0],
    clearable=False
)

# Graph id 3
graph3 = dcc.Graph(id="Consumption_graph3")

# ####################### CHART #############################

def Tourist_graph_continent(data):
    fig = px.line(data, x='year', y='Nb_tourists', color='continent')
    fig.update_layout(title='Nb_tourists by Continent and Year')
    return fig

# ####################### PAGE LAYOUT #############################

# Layout


layout = html.Div(
    style={
        'backgroundColor': '#f9f9f9',  # Light grey background for the entire layout
        'padding': '20px',             # Padding around the layout
        'font-family': 'Arial, sans-serif',  # Modern font
    },
    children=[
        html.Br(),
        html.H2("Impact of Covid-19 on Consumption", className="fw-bold text-center", style={'margin-bottom': '20px', 'color': '#333'}),  # Centered title with color
        html.Br(),

        # Dropdown for Graph 1
        html.Div(
            style={
                'backgroundColor': '#fff',  # White background for dropdown section
                'padding': '15px',          # Padding inside the dropdown section
                'border-radius': '10px',    # Rounded corners
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow effect
                'margin-bottom': '20px',    # Space below the section
            },
            children=[
                html.Label("Select Category for Graph 1", style={'fontSize': '18px', 'margin-bottom': '10px'}),
                cat_dropdown1,
            ]
        ),
        html.Br(),
        graph1,
        html.Br(),

        # Dropdown for Graph 2
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '15px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px',
            },
            children=[
                html.Label("Select Category for Graph 2", style={'fontSize': '18px', 'margin-bottom': '10px'}),
                cat_dropdown2,
            ]
        ),
        html.Br(),
        graph2,

        # Comment section
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-top': '30px',
            },
            children=[
                html.H3("Comment:", style={'margin-bottom': '10px'}),
                html.P(" Since the tourism was cut in all world during covid it's logic to think that it is the main lead of this small decreas of consumption.", 
                        style={'fontSize': '16px', 'color': '#555'}),
            ]
        ),
        # Dropdown for Graph 3
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '15px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px',
            },
            children=[
                html.Label("Select Category for Graph 2", style={'fontSize': '18px', 'margin-bottom': '10px'}),
                cat_dropdown3,
            ]
        ),
        html.Br(),
        graph3
    ]
)

# ####################### CALLBACKS ###############################

@callback(
    Output("Consumption_graph1", "figure"),
    [Input("cat_column", "value")]
)
def update_graph1(selected_category1):
    return update_graph_continent(data1)

@callback(
    Output("Consumption_graph2", "figure"),
    [Input("cat_column", "value")]
)
def update_graph2(selected_category2):
    return plot_choropleth_map(data2)

@callback(
    Output("Consumption_graph3", "figure"),
    [Input("cat_column", "value")]
)
def update_graph3(selected_category3):
    return Tourist_graph_continent(data3)