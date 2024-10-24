'''
5. Trade and Supply Chains
Page Name: "Global Trade & Supply Chains"

Purpose: Analyze how COVID-19 impacted international trade, exports, imports, and supply chains.

Content:
Overview of how global trade volume decreased due to the pandemic.
Comparative analysis of export/import volumes across countries.
Analysis of specific industries affected (e.g., manufacturing, energy).

Visualizations:
Bar chart: Trade volume changes for key countries.
Line chart: Time-series showing export/import trends.
Scatter plot: Trade volume vs. stock market performance.
'''
'''
import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import country_converter as cc

dash.register_page(__name__, path='/trade', name="Trade and Supply Chains", order=5)

####################### DATA #############################
data = pd.read_csv("/Users/prachikansal/Desktop/centrale med/mock project/GlobalImpact-Covid19/data/Import.csv", sep=',', skiprows=4, header=None)
# link to the dataset: 

column_names = data.iloc[0]
data.columns = column_names
data = data.drop(data.index[0])

selected_columns = ['Country Name',2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
new_data = data[selected_columns]
melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=data.columns[4:], var_name='year', value_name='Import')

melted_data['year'] = pd.to_numeric(melted_data['year'])
filtered_data = melted_data[melted_data['year'].isin([2018,2019,2020, 2021, 2022, 2023])]

unique_years = filtered_data['year'].unique()

sorted_data = filtered_data.sort_values(['Country Name', 'year'])
sorted_data['year'] = sorted_data['year'].astype(int)
sorted_data = sorted_data.rename(columns={'Country Name': 'location'})

sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')

nan_count_continent = sorted_data['continent'].isnull().sum()
# print("Number of NaN values in 'continent':", nan_count_continent)
nan_count_continent = sorted_data['Import'].isnull().sum()
# print("Number of NaN values in 'Import':", nan_count_continent)

nan_counts_by_year = sorted_data.groupby('year')['Import'].apply(lambda x: x.isnull().sum())
# print(nan_counts_by_year)
sorted_data = sorted_data[sorted_data['continent'] != 'not found']

# Trouver l'Importation maximale en 2021 et le pays correspondant
max_Import_2021 = sorted_data[sorted_data['year'] == 2021]['Import'].idxmax()
max_Import_2021_row = sorted_data.loc[max_Import_2021]
max_Import_2021_country = max_Import_2021_row['location']
max_Import_2021_value = max_Import_2021_row['Import']

# Trouver l'Importation minimale en 2020 et le pays correspondant
min_Import_2020 = sorted_data[sorted_data['year'] == 2020]['Import'].idxmin()
min_Import_2020_row = sorted_data.loc[min_Import_2020]
min_Import_2020_country = min_Import_2020_row['location']
min_Import_2020_value = min_Import_2020_row['Import']

Import_by_continent_year = sorted_data.groupby(['continent', 'year'])['Import'].sum().reset_index()

data_2020 = sorted_data[sorted_data['year'] == 2020]
top_3_Gov_Concump_by_continent = data_2020.groupby('continent')[['location','Import']].apply(lambda x: x.nlargest(3, 'Import')).reset_index(level=0)
# print(top_3_Gov_Concump_by_continent[['continent', 'location', 'Import']])

####################### WIDGETS #############################

# # Dropdown for selecting country
# country_dropdown = dcc.Dropdown( 
#     id = "country_dropdown",
#     options = data["Country Name"].unique(),
#     value = "World",  # Default value
#     clearable = False
# )

####################### CHART #############################

def update_graph_continent(data):
    fig = px.line(
        data, 
        x='year', 
        y='Import', 
        color='continent'
        )
    
    fig.update_layout(title='Import by Continent and Year')
    
    return fig


####################### PAGE LAYOUT #############################

layout = html.Div(children=[
    html.Br(),
    html.H2("Impact of Covid-19 on Imports", className="fw-bold text-center"),
    # "Select Country", country_dropdown, 
    # "Select Year", year_dropdown,
    html.Br(),
    dcc.Graph(id="imports", figure=update_graph_continent(Import_by_continent_year))
])
'''