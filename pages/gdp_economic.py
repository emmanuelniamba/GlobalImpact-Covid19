
# # # # First 4 rows contain information about the dataset
# # # data = pd.read_csv("data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_31631.csv", sep=',', skiprows=4, header=None)

# # # # column_names = data.iloc[0]
# # # # data.columns = column_names
# # # data = data.drop(data.index[0])

# # # # Select columns for analysis
# # # selected_columns = ['Country Name', 2020.0, 2021.0, 2022.0, 2023.0]
# # # new_data = data[selected_columns]

# # # # Reshape the data
# # # melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=data.columns[4:], var_name='year', value_name='GDP')
# # # melted_data['year'] = pd.to_numeric(melted_data['year'])

# # # # Filter the data for relevant years
# # # filtered_data = melted_data[melted_data['year'].isin([2018,2019,2020, 2021, 2022, 2023])]

# # # data_gdp = filtered_data.sort_values(['Country Name', 'year'])
# # # data_gdp['year'] = data_gdp['year'].astype(int)
# # # sorted_data = data_gdp.rename(columns={'Country Name': 'location'})
# # # sorted=sorted_data.copy()
# # # sorted['continent'] = cc.convert(names=sorted_data['location'], to='continent')


# # # ####################### SCATTER CHART #############################
# # # def create_gdp_line_chart(sorted_data):
# # #     fig = px.line(sorted_data, 
# # #                 x='year', 
# # #                 y='GDP', 
# # #                 color='Country Name', 
# # #                 title='GDP Growth Over Time (2020-2023)',
# # #                 labels={'year': 'Year', 'GDP': 'GDP Growth Rate'},
# # #                 markers=True)
# # #     return fig

# # # ####################### WIDGETS #############################
# # # # Dropdowns for selecting country and year
# # # country_dropdown = dcc.Dropdown(
# # #     id="country_dropdown",
# # #     options=[{"label": country, "value": country} for country in sorted_data['Country Name'].unique()],
# # #     value="India",  # Default value
# # #     clearable=False
# # # )

# # # year_dropdown = dcc.Dropdown(
# # #     id="year_dropdown",
# # #     options=[{"label": str(year), "value": year} for year in sorted_data['year'].unique()],
# # #     value=2023,  # Default value
# # #     clearable=False
# # # )

# # # ####################### PAGE LAYOUT #############################
# # # layout = html.Div(children=[
# # #     html.Br(),
# # #     html.H2("Explore GDP Growth Over Time", className="fw-bold text-center"),
# # #     "Select Country", country_dropdown, 
# # #     "Select Year", year_dropdown,
# # #     html.Br(),
# # #     dcc.Graph(id="gdp_graph")
# # # ])

# # # ####################### CALLBACKS ###############################
# # # @callback(Output("gdp_graph", "figure"), 
# # #           [Input("country_dropdown", "value"), Input("year_dropdown", "value")])

# # # def update_gdp_chart(selected_country, selected_year):
# # #     # Filter data based on dropdown inputs
# # #     filtered_data = sorted_data[(sorted_data['Country Name'] == selected_country) & (sorted_data['year'] == selected_year)]
    
# # #     # Create the chart
# # #     fig = px.bar(filtered_data, 
# # #                  x='year', 
# # #                  y='GDP', 
# # #                  title=f'GDP Growth for {selected_country} in {selected_year}',
# # #                  labels={'year': 'Year', 'GDP': 'GDP Growth Rate'})
# # #     return fig


# import pandas as pd
# import dash
# from dash import dcc, html, callback
# import plotly.express as px
# from dash.dependencies import Input, Output
# import country_converter as cc


# dash.register_page(__name__, path='/gdp_economic', name="GDP and Economic Growth", order=10)


# ####################### DATA #############################

# # data = pd.read_csv("/Users/prachikansal/Desktop/centrale med/mock project/GlobalImpact-Covid19/data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_31631.csv", sep=',', skiprows=4, header=None)
# data = pd.read_csv("data/gdp_data.csv", sep=',')
# # link to the dataset: https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CD&country=#

# data = data.drop(data.index[-1:-6:-1]) # As the last 5 rows are blank and just contain null values, drop them

# years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]
# for year in years:
#     data.rename(columns={f'{year} [YR{year}]': f'{year}'}, inplace=True)

# pre_covid_years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"]
# post_covid_years = ["2022","2023"]

# data['Pre_Covid'] = data[pre_covid_years].apply(pd.to_numeric, errors = 'coerce').mean(axis=1)
# data['Post_Covid'] = data[post_covid_years].apply(pd.to_numeric, errors = 'coerce').mean(axis=1)

# selected_columns = ["Country Name","Pre_Covid","2020","2021","Post_Covid"]
# filtered_data = data[selected_columns]

# melted_data = filtered_data.melt(id_vars = ['Country Name'], 
#                         value_vars = ['Pre_Covid', '2020', '2021', 'Post_Covid'], 
#                         var_name = 'Year', 
#                         value_name = 'GDP')

# '''
# The dataset contains GDP data for 268 countries, from the year 1960-2023. We only consider data from the past decade, so 2010-2023. 
# 2010-2019 is grouped as the Pre-Covid era.
# 2020, 2021 are visualized individually to study the pattern of GDP accurately
# 2022-2023 is grouped as the Post-Covid era.
# '''

# ####################### WIDGETS #############################

# # # Dropdown for selecting country
# # country_dropdown = dcc.Dropdown( 
# #     id = "country_dropdown",
# #     options = data["Country Name"].unique(),
# #     value = "World",  # Default value
# #     clearable = False
# # )

# ####################### CHART #############################

# def create_gdp_line_chart(data):
#   fig = px.line(data, 
#                 x = 'Year',
#                 y = 'GDP',
#                 color='Country Name',
#                 title='Impact of Covid-19 on GDP',
#                 labels={'Year': 'Phase', 'GDP': 'GDP (in USD)'},
#                 markers=True)
#   return fig


# ####################### PAGE LAYOUT #############################

# layout = html.Div(children=[
#     html.Br(),
#     html.H2("Impact of Covid-19 on GDP", className="fw-bold text-center"),
#     # "Select Country", country_dropdown, 
#     # "Select Year", year_dropdown,
#     html.Br(),
#     dcc.Graph(id="tourism", figure=create_gdp_line_chart(melted_data))
# ])


# '''2. GDP and Economic Growth
# Page Name: "GDP & Economic Growth"
# Purpose: Analyze the impact of COVID-19 on the GDP of different countries and regions.

# Content:
# Time-series analysis of GDP growth pre- and post-COVID.
# Comparative analysis of GDP contraction and recovery across regions.
# Highlight top countries with the biggest growth and decline.

# Visualizations:
# Line chart: Global GDP growth trends over time.
# Bar chart: GDP change comparison between countries.
# Scatter plot: GDP growth vs. unemployment rate.
# '''