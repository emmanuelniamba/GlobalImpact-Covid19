import dash  
from dash import dcc, html , callback
import plotly.express as px  
import pandas as pd  
from dash.dependencies import Input, Output  
import plotly.express as px
from plotly.subplots import make_subplots
import country_converter as cc
import plotly.graph_objects as go
import logging

# Register the page for the dashboard
dash.register_page(__name__, path='/Export2.csv', name="Export2 on the world", order=21)

logger = logging.getLogger('country_converter')
logger.setLevel(logging.ERROR)

# Load Export data
dataR = pd.read_csv("data/Export.csv", sep=',', skiprows=4, header=None)

# Load Manufacturing data
dataM = pd.read_csv("data/manufacturing.csv", sep=',', skiprows=4, header=None)

# Function to process Export data
def load_process_export(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    
    # Keep necessary columns
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    data = data[selected_columns]
    
    # Rename columns for easier access
    data.columns = data.columns.astype(str)
    data = data.rename(columns={'Country Name': 'location'})
    
    # Calculate the difference between 2020 and 2019 for each country
    data['diff_2020_2019_export'] = data['2020.0'] - data['2019.0']
    
    # Melt the dataframe to long format for year-based analysis
    value_vars = ['2018.0', '2019.0', '2020.0', '2021.0', '2022.0', '2023.0']
    melted_data = pd.melt(data, id_vars=['location', 'diff_2020_2019_export'], value_vars=value_vars, var_name='year', value_name='Export')
    
    # Convert year column to numeric
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    
    # Sort data by location and year
    melted_data = melted_data.sort_values(['location', 'year'])
    melted_data['year'] = melted_data['year'].astype(int)
    
    # Add continent information
    melted_data['continent'] = cc.convert(names=melted_data['location'], to='continent')
    
    # Filter out rows where continent is not found
    melted_data = melted_data[melted_data['continent'] != 'not found']
    
    return melted_data


# Function to process Manufacturing data and calculate the difference between 2020 and 2019
def load_process_manufacturing(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    
    # Keep necessary columns
    selected_columns = ['Country Name',  2019.0, 2020.0]
    data = data[selected_columns]
    
    # Rename columns for easier access
    data.columns = data.columns.astype(str)
    data = data.rename(columns={'Country Name': 'location'})
    
    # Calculate the difference between 2020 and 2019 for each country
    data['diff_2020_2019_manufacturing'] = data['2020.0'] - data['2019.0']
    
    # Melt the dataframe to long format for year-based analysis
    value_vars = [ '2019.0', '2020.0']
    melted_data = pd.melt(data, id_vars=['location', 'diff_2020_2019_manufacturing'], value_vars=value_vars, var_name='year', value_name='Manufacturing')
    
    # Convert year column to numeric
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    
    # Sort data by location and year
    melted_data = melted_data.sort_values(['location', 'year'])
    melted_data['year'] = melted_data['year'].astype(int)
    
    # Add continent information
    melted_data['continent'] = cc.convert(names=melted_data['location'], to='continent')
    
    # Filter out rows where continent is not found
    melted_data = melted_data[melted_data['continent'] != 'not found']
    
    return melted_data
def iso_country(data):
   
   data['iso_alpha'] = cc.convert(names=data['location'], to='ISO3')
   return data

# Load and process data
export_data_not_iso = load_process_export(dataR)
manufacturing_data_not_iso = load_process_manufacturing(dataM)
export_data=iso_country(export_data_not_iso)
manufacturing_data=iso_country(manufacturing_data_not_iso)
# Layout of the app  
layout = html.Div(
    style={
        'backgroundColor': '#f9f9f9',  # Light grey background similar to the image
        'padding': '20px',             # Add padding to the entire layout
        'font-family': 'Arial, sans-serif',  # Clean, modern font
    },
    children=[
        # Top container for dropdown and title
        html.Div(
            style={
                'display': 'flex',           # Flexbox for side-by-side layout
                'flex-direction': 'row',     # Elements side by side
                'justify-content': 'space-between',  # Spacing between elements
                'align-items': 'center',     # Vertically center align
                'margin-bottom': '20px',     # Add space below the section
            },
            children=[
                html.Label('Select a Country:', style={
                    'fontSize': '20px',     # Larger font size for the label
                    'margin-right': '10px', # Space between label and dropdown
                }),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': country, 'value': country} for country in export_data['location'].unique()],
                    placeholder="Select a country",  # No default value, user must select
                    style={
                        'width': '300px',   # Set a fixed width for the dropdown
                        'border-radius': '5px',  # Slight rounding for dropdown edges
                        'padding': '5px',   # Padding for the dropdown
                        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow effect
                    }
                ),
            ]
        ),

        # Container for the map (with a card-like appearance)
        html.Div(
            style={
                'backgroundColor': '#fff',  # White background for the card
                'padding': '20px',          # Padding inside the card
                'border-radius': '10px',    # Rounded corners
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow effect
                'margin-bottom': '20px',    # Space between this and the next section
            },
            children=[
                html.H4('World Export Map', style={'margin-bottom': '10px'}),  # Section title
                dcc.Graph(id='exports-map'),
            ]
        ),

        # Container for the line plot (also styled as a card)
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px',
            },
            children=[
                html.H4('Exports by Continent', style={'margin-bottom': '10px'}),  # Section title
                dcc.Graph(id='exports-lineplot'),
            ]
        ),

        # Section for exports comparison (styled as text in a card)
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px',
            },
            children=[
                html.H4('Exports Comparison (2019 vs 2020)', style={'margin-bottom': '10px'}),
                html.Div(id='exports-comparison', style={'fontSize': '18px'}),  # Display comparison text
            ]
        ),

        # Section for manufacturing comparison (styled as text in a card)
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-bottom': '20px',
            },
            children=[
                html.H4('Manufacturing Comparison (2019 vs 2020)', style={'margin-bottom': '10px'}),
                html.Div(id='manufacturing-comparison', style={'fontSize': '18px'}),  # Display comparison text
            ]
        ),

        # Placeholder for comments (styled like a card for consistency)
        html.Div(
            style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'margin-top': '20px',
            },
            children=[
                html.H3("Comments:", style={'margin-bottom': '10px'}),
                html.P("Try China,  the COVID-19 pandemic, China was the only country to significantly increase its exports, thanks to its strong manufacturing capabilities. The nation effectively utilized its infrastructure and skilled labor force to rapidly produce essential goods like medical supplies and electronics in response to global demand.", style={'fontSize': '16px'}),
            ]
        )
    ]
)


# Callbacks for interactivity
@callback(
    Output('exports-map', 'figure'),
    Output('exports-lineplot', 'figure'),
    Output('exports-comparison', 'children'),
    Output('manufacturing-comparison', 'children'),
    Input('country-dropdown', 'value')
)
def update_dashboard(selected_country):
    
    if not selected_country:
        return map_fig, line_fig, "Please select a country.", "Please select a country."
    
    # Filter data for exports and manufacturing by selected country
    filtered_export_data = export_data[export_data['location'] == selected_country]
    filtered_manufacturing_data = manufacturing_data[manufacturing_data['location'] == selected_country]

    # Create map figure
    map_fig = px.choropleth(
        export_data,
        locations="iso_alpha",
        color="Export",
        hover_name="location",
        animation_frame="year",
        color_continuous_scale=px.colors.sequential.Plasma
    )

    # Create line plot by continent
    continent_data = export_data.groupby(['continent', 'year'])['Export'].sum().reset_index()
    line_fig = px.line(continent_data, x='year', y='Export', color='continent')
    line_fig.update_layout(title='Export by Continent and Year')

    # Export comparison (2019 vs 2020)
    export_2019 = filtered_export_data[filtered_export_data['year'] == 2019]['Export'].sum()
    export_2020 = filtered_export_data[filtered_export_data['year'] == 2020]['Export'].sum()
    export_comparison = f"Exports in 2019: {export_2019}, Exports in 2020: {export_2020}, Difference: {export_2020 - export_2019}"

    # Manufacturing comparison (2019 vs 2020)
    manufacturing_2019 = filtered_manufacturing_data[filtered_manufacturing_data['year'] == 2019]['Manufacturing'].sum()
    manufacturing_2020 = filtered_manufacturing_data[filtered_manufacturing_data['year'] == 2020]['Manufacturing'].sum()
    manufacturing_comparison = f"Manufacturing in 2019: {manufacturing_2019}, Manufacturing in 2020: {manufacturing_2020}, Difference: {manufacturing_2020 - manufacturing_2019}"

    return map_fig, line_fig, export_comparison, manufacturing_comparison



