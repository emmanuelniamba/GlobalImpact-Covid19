import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import country_converter as cc
import logging


dash.register_page(__name__, path = '/Government_consumption.csv', name = "Government_Consumption on the world", order = 11)


####################### DATA #############################

logger = logging.getLogger('country_converter')
logger.setLevel(logging.ERROR)

dataD=  pd.read_csv("data/owid-covid-data.csv", sep=',' )

dataR = pd.read_csv("data/Government_consumption.csv", sep=',', skiprows=4, header=None)

def load_process(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    new_data = data[selected_columns]
    data.columns = data.columns.astype(str)
    value_vars = [col for col in data.columns[4:] if col != 'nan']
    melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='Gov_Consump')
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    filtered_data = melted_data[melted_data['year'].isin([2018, 2019, 2020, 2021, 2022, 2023])]
    unique_years = filtered_data['year'].unique()
    sorted_data = filtered_data.sort_values('Country Name')
    sorted_data = filtered_data.sort_values(['Country Name', 'year'])
    sorted_data['year'] = sorted_data['year'].astype(int)
    sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
    sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')
    nan_count_continent = sorted_data['continent'].isnull().sum()
    nan_count_gov_consump = sorted_data['Gov_Consump'].isnull().sum()
    nan_counts_by_year = sorted_data.groupby('year')['Gov_Consump'].apply(lambda x: x.isnull().sum())
    sorted_data = sorted_data[sorted_data['continent'] != 'not found']
    return sorted_data

def continent_Gov_Consump(data):
    gov_consump_by_continent_year = data.groupby(['continent', 'year'])['Gov_Consump'].sum().reset_index()
    return gov_consump_by_continent_year

def iso_country(data):
    data['iso_alpha'] = cc.convert(names=sorted_data['location'], to='ISO3')
    return data
import pandas as pd
import country_converter as cc
import numpy as np

def load_and_process_death_data(data):

    # Keep only relevant columns
    columns_to_keep = ['continent', 'location', 'date', 'total_cases', 'total_deaths', 'population']
    data = data[columns_to_keep]

    # Extract the year from the date
    data['year'] = pd.to_datetime(data['date']).dt.year

    # Get the last value for each year and location
    last_value_per_year = data.groupby(['year', 'location'], as_index=False, sort=False).last()
    data = last_value_per_year.drop(columns=['date'])

    # Manually map continents if missing
    manual_mapping = {
        'Africa': 'Africa',
        'Asia': 'Asia',
        'Europe': 'Europe',
        'North America': 'North America',
        'Oceania': 'Oceania',
        'South America': 'South America',
    }

    nan_continent_rows = data['continent'].isnull()
    continent_values = data.loc[nan_continent_rows, 'location'].apply(lambda x: cc.convert(names=x, to='continent', not_found=None))
    data.loc[nan_continent_rows, 'continent'] = data.loc[nan_continent_rows, 'location'].map(manual_mapping).fillna(pd.Series(continent_values, index=data.loc[nan_continent_rows, 'location'].index))

    # Define coefficient of variation function
    def coefficient_of_variation(group):
        std_dev = group.std()
        mean = group.mean()
        if mean == 0:
            return np.nan  # Handle cases where the mean is zero
        return (std_dev / mean)

    # Calculate coefficient of variation for cases and deaths by continent
    continent_evolution_cases = data.groupby('continent')['total_cases'].apply(coefficient_of_variation)
    continent_evolution_deaths = data.groupby('continent')['total_deaths'].apply(coefficient_of_variation)

    # Create a DataFrame to store the results
    continent_evolution_df = pd.DataFrame({
        'Coefficient_of_Variation_Cases': continent_evolution_cases,
        'Coefficient_of_Variation_Deaths': continent_evolution_deaths,
    })

    # Function to replace NaN values using continent coefficient of variation
    def replace_nan_with_continent_evolution(df, continent_evolution_df):
        df_copy = df.copy()  # Create a copy to avoid modifying the original DataFrame

        for column in ['total_cases', 'total_deaths']:
            for index, row in df_copy.iterrows():
                if pd.isnull(row[column]):
                    continent = row['continent']
                    if continent in continent_evolution_df.index:
                        # Find the previous non-NaN value for the same location and year.
                        previous_value = None
                        for prev_index in range(index - 1, -1, -1):
                            prev_row = df_copy.iloc[prev_index]
                            if prev_row['location'] == row['location'] and prev_row['year'] == row['year'] and not pd.isnull(prev_row[column]):
                                previous_value = prev_row[column]
                                break

                        if previous_value is not None:
                            # Replace NaN with previous value multiplied by the coefficient of variation.
                            df_copy.loc[index, column] = previous_value * continent_evolution_df.loc[continent, f'Coefficient_of_Variation_{column.split("_")[1]}']
                        else:
                            # Find the next non-NaN value for the same location and year.
                            next_value = None
                            for next_index in range(index + 1, len(df_copy)):
                                next_row = df_copy.iloc[next_index]
                                if next_row['location'] == row['location'] and next_row['year'] == row['year'] and not pd.isnull(next_row[column]):
                                    next_value = next_row[column]
                                    break
                            if next_value is not None:
                                # Replace NaN with next value divided by the coefficient of variation.
                                df_copy.loc[index, column] = next_value / continent_evolution_df.loc[continent, f'Coefficient_of_Variation_{column.split("_")[1]}']
        return df_copy

    # Apply the function to replace NaN values
    data_filled = replace_nan_with_continent_evolution(data, continent_evolution_df)

    # Remove specific locations and year 2024
    names_to_remove = ['Hong Kong', 'Western Sahara']
    data_filled = data_filled[~data_filled['location'].isin(names_to_remove)]
    data_filled = data_filled[data_filled['year'] != 2024]

    return data_filled

def continent_total_deaths(data):
    gov_consump_by_continent_year = data.groupby(['continent', 'year'])['total_cases'].sum().reset_index()
    return gov_consump_by_continent_year
# ####################### WIDGETS #############################

# Dropdown for 1
sorted_data = load_process(dataR)
data1 = continent_Gov_Consump(sorted_data)

data_columns1 = {
    "Gov_Consump": data1["Gov_Consump"],
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
graph1 = dcc.Graph(id="Gov_Consump_graph1")

# ####################### CHART #############################

def update_graph_continent(data):
    fig = px.line(data, x='year', y='Gov_Consump', color='continent')
    fig.update_layout(title='Government Consumption by Continent and Year')
    return fig

# Dropdown for 2
sorted_data = load_process(dataR)
data2 = iso_country(sorted_data)
data_columns2 = {
    "Gov_Consump": data2["Gov_Consump"],
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
graph2 = dcc.Graph(id="Gov_Consump_graph2")

# ####################### CHART #############################

def plot_choropleth_map(data):
    fig = px.choropleth(
        data,
        locations="iso_alpha",
        color="Gov_Consump",  
        hover_name="location",
        animation_frame="year",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    return fig

# Dropdown for 3
data_death = load_and_process_death_data(dataD)
sorted_data = load_process(dataR)
combined_data = pd.merge(sorted_data[['continent','year','location']], data_death, on=['year','location','continent'], how='inner')
data3=continent_total_deaths(combined_data)

data_columns3 = {
    "total_cases": data3["total_cases"],
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
graph3 = dcc.Graph(id="Gov_Consump_graph3")

def update_graph_continent(data):
    fig = px.line(data, x='year', y='total_cases', color='continent')
    fig.update_layout(title='total_cases by Continent and Year')
    return fig
# ####################### PAGE LAYOUT #############################

# Layout
layout = html.Div(children=[
    html.Br(),
    html.H2("Impact of Covid-19 on Government Consumption", className="fw-bold text-center"),
    html.Br(),
    html.Div([html.Label("Select Category for Graph 1"), cat_dropdown1]),
    html.Br(),
    graph1,
    html.Br(),
    html.Div([html.Label("Select Category for Graph 2"), cat_dropdown2]),
    html.Br(),
    graph2
])

layout = html.Div(
    style={
        'backgroundColor': '#f9f9f9',  # Light grey background for the entire layout
        'padding': '20px',             # Padding around the layout
        'font-family': 'Arial, sans-serif',  # Modern font
    },
    children=[
        html.Br(),
        html.H2("Impact of Covid-19 on Government Consumption", className="fw-bold text-center", style={'margin-bottom': '20px', 'color': '#333'}),  # Centered title with color
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
                html.P(" There is a clear correlation between rising COVID-19 cases and increased government consumption, as higher case numbers led to greater spending on healthcare, testing, and public health measures.This direct link between rising infections and public spending highlights how the pandemic strained both health systems and economies worldwide.", 
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
    Output("Gov_Consump_graph1", "figure"),
    [Input("cat_column", "value")]
)
def update_graph1(selected_category1):
    return update_graph_continent(data1)  # Pass the data1 as argument

@callback(
    Output("Gov_Consump_graph2", "figure"),
    [Input("cat_column", "value")]
)
def update_graph2(selected_category2):
    return plot_choropleth_map(data2)  # Pass the data2 as argument
 
@callback(
    Output("Gov_Consump_graph3", "figure"),
    [Input("cat_column", "value")]
)
def update_graph3(selected_category3):
    return update_graph_continent(data3)