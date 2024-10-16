# import pandas as pd
# import dash
# from dash import dcc, html, callback
# import plotly.express as px
# from dash.dependencies import Input, Output
# import country_converter as cc

# # Register the page for multi-page Dash apps
# dash.register_page(__name__, path='/relationship', name="GDP Analysis", order=3)

# ####################### DATASET #############################
# # Load the dataset
# data = pd.read_csv("data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_31631.csv", sep=',', skiprows=4, header=None)

# # Set proper column names
# column_names = data.iloc[0]
# data.columns = column_names
# data = data.drop(data.index[0])

# # Select columns for analysis
# selected_columns = ['Country Name', 2020.0, 2021.0, 2022.0, 2023.0]
# new_data = data[selected_columns]

# # Reshape the data
# melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=data.columns[4:], var_name='year', value_name='GDP')
# melted_data['year'] = pd.to_numeric(melted_data['year'])

# # Filter the data for relevant years
# filtered_data = melted_data[melted_data['year'].isin([2018,2019,2020, 2021, 2022, 2023])]

# data_gdp = filtered_data.sort_values(['Country Name', 'year'])
# data_gdp['year'] = data_gdp['year'].astype(int)
# sorted_data = data_gdp.rename(columns={'Country Name': 'location'})
# sorted=sorted_data.copy()
# sorted['continent'] = cc.convert(names=sorted_data['location'], to='continent')


# ####################### SCATTER CHART #############################
# def create_gdp_line_chart(sorted_data):
#     fig = px.line(sorted_data, 
#                 x='year', 
#                 y='GDP', 
#                 color='Country Name', 
#                 title='GDP Growth Over Time (2020-2023)',
#                 labels={'year': 'Year', 'GDP': 'GDP Growth Rate'},
#                 markers=True)
#     return fig

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

# ####################### PAGE LAYOUT #############################
# layout = html.Div(children=[
#     html.Br(),
#     html.H2("Explore GDP Growth Over Time", className="fw-bold text-center"),
#     "Select Country", country_dropdown, 
#     "Select Year", year_dropdown,
#     html.Br(),
#     dcc.Graph(id="gdp_graph")
# ])

# ####################### CALLBACKS ###############################
# @callback(Output("gdp_graph", "figure"), 
#           [Input("country_dropdown", "value"), Input("year_dropdown", "value")])

# def update_gdp_chart(selected_country, selected_year):
#     # Filter data based on dropdown inputs
#     filtered_data = sorted_data[(sorted_data['Country Name'] == selected_country) & (sorted_data['year'] == selected_year)]
    
#     # Create the chart
#     fig = px.bar(filtered_data, 
#                  x='year', 
#                  y='GDP', 
#                  title=f'GDP Growth for {selected_country} in {selected_year}',
#                  labels={'year': 'Year', 'GDP': 'GDP Growth Rate'})
#     return fig
