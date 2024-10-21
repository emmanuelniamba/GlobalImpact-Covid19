import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/', name="Name of Tab=Global", order=0)

# Load the GDP dataset
# Make sure to change the path to where your dataset is located
df = pd.read_csv(r"data\gdp_data.csv")

# Melt the DataFrame for easier plotting
df_melted = df.melt(id_vars=['Country Name', 'Country Code'], 
                     value_vars=[str(year) + ' [YR' + str(year) + ']' for year in range(2010, 2024)],
                     var_name='Year', value_name='GDP')

# Convert GDP to numeric, removing any non-numeric characters if necessary
df_melted['GDP'] = pd.to_numeric(df_melted['GDP'], errors='coerce')

####################### PAGE LAYOUT #############################

content = ''' 
'''

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Covid 19 Combined Dataset Overview"),
        "<Put a brief description>",
        html.Br(), html.Br(),
        "Put links of all the datasets. Citations are important.",
    ]),

    # Year selection dropdown
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': str(year) + ' [YR' + str(year) + ']'} for year in range(2010, 2024)],
            value='2020 [YR2020]',  # Default year
            clearable=False
        ),
    ], style={'width': '50%', 'margin': '20px auto'}),

    # World map for GDP visualization
    dcc.Graph(id='gdp-world-map'),

    html.Div(children=[
        html.Br(),
        content,
        "", html.Br(),
        "",
        html.Br(), html.Br(),
        html.B("Metrics"),
        html.Br(),
        html.B("GDP over the years"),
    ])
    
], className="p-4 m-2", style={"background-color": "#e3f2fd"})

# Callback to update the map based on selected year
@dash.callback(
    Output('gdp-world-map', 'figure'),
    Input('year-dropdown', 'value')
)
def update_map(selected_year):
    filtered_df = df_melted[df_melted['Year'] == selected_year]

    fig = px.choropleth(
        filtered_df,
        locations='Country Code',
        locationmode='ISO-3',  # Use ISO-3 country codes
        color='GDP',
        hover_name='Country Name',
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'GDP': 'GDP'},
        title=f'GDP by Country in {selected_year.split(" ")[0]}',
    )
    
    fig.update_geos(projection_type="mercator")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    return fig
