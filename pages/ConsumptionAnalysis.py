import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import country_converter as cc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import logging
import numpy as np



dash.register_page(__name__, path = '/ConsumptionAnalysis', name = "Consumption Statistics", order = 6)




########################################### DATA #################################################

logger = logging.getLogger('country_converter')
logger.setLevel(logging.ERROR)
dataT = pd.read_csv("data/international-tourist-trips.csv", sep=',')
dataD=  pd.read_csv("data/owid-covid-data.csv", sep=',' )
dataC = pd.read_csv("data/Consumption_data.csv", sep=',', skiprows=4, header=None)
dataR = pd.read_csv("data/Government_consumption.csv", sep=',', skiprows=4, header=None)

def load_process(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    data = data[selected_columns]
    data.columns = data.columns.astype(str)
    value_vars = [col for col in data.columns[4:] if col != 'nan']
    melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='Gov_Consump')
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    filtered_data = melted_data[melted_data['year'].isin([2018, 2019, 2020, 2021, 2022, 2023])]
    sorted_data = filtered_data.sort_values('Country Name')
    sorted_data = filtered_data.sort_values(['Country Name', 'year'])
    sorted_data['year'] = sorted_data['year'].astype(int)
    sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
    sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')
    sorted_data = sorted_data[sorted_data['continent'] != 'not found']
    return sorted_data

def load_process_consumption(data):
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

def continent_Gov_Consump(data):
    gov_consump_by_continent_year = data.groupby(['continent', 'year'])['Gov_Consump'].sum().reset_index()
    return gov_consump_by_continent_year

def iso_country(data):
    data['iso_alpha'] = cc.convert(names=data['location'], to='ISO3')
    return data


def load_and_process_death_data(data):
    columns_to_keep = ['continent', 'location', 'date', 'total_cases', 'total_deaths', 'population']
    data = data[columns_to_keep]

    data['year'] = pd.to_datetime(data['date']).dt.year

    last_value_per_year = data.groupby(['year', 'location'], as_index=False, sort=False).last()
    data = last_value_per_year.drop(columns=['date'])

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

    def coefficient_of_variation(group):
        std_dev = group.std()
        mean = group.mean()
        if mean == 0:
            return np.nan  
        return (std_dev / mean)

    continent_evolution_cases = data.groupby('continent')['total_cases'].apply(coefficient_of_variation)
    continent_evolution_deaths = data.groupby('continent')['total_deaths'].apply(coefficient_of_variation)

    continent_evolution_df = pd.DataFrame({
        'Coefficient_of_Variation_Cases': continent_evolution_cases,
        'Coefficient_of_Variation_Deaths': continent_evolution_deaths,
    })

    def replace_nan_with_continent_evolution(df, continent_evolution_df):
        df_copy = df.copy()  

        for column in ['total_cases', 'total_deaths']:
            for index, row in df_copy.iterrows():
                if pd.isnull(row[column]):
                    continent = row['continent']
                    if continent in continent_evolution_df.index:
                        previous_value = None
                        for prev_index in range(index - 1, -1, -1):
                            prev_row = df_copy.iloc[prev_index]
                            if prev_row['location'] == row['location'] and prev_row['year'] == row['year'] and not pd.isnull(prev_row[column]):
                                previous_value = prev_row[column]
                                break

                        if previous_value is not None:
                            df_copy.loc[index, column] = previous_value * continent_evolution_df.loc[continent, f'Coefficient_of_Variation_{column.split("_")[1]}']
                        else:
                            next_value = None
                            for next_index in range(index + 1, len(df_copy)):
                                next_row = df_copy.iloc[next_index]
                                if next_row['location'] == row['location'] and next_row['year'] == row['year'] and not pd.isnull(next_row[column]):
                                    next_value = next_row[column]
                                    break
                            if next_value is not None:
                                df_copy.loc[index, column] = next_value / continent_evolution_df.loc[continent, f'Coefficient_of_Variation_{column.split("_")[1]}']
        return df_copy

    data_filled = replace_nan_with_continent_evolution(data, continent_evolution_df)
    names_to_remove = ['Hong Kong', 'Western Sahara']
    data_filled = data_filled[~data_filled['location'].isin(names_to_remove)]
    data_filled = data_filled[data_filled['year'] != 2024]

    return data_filled


def continent_total_deaths(data):
    gov_consump_by_continent_year = data.groupby(['continent', 'year'])['total_cases'].sum().reset_index()
    return gov_consump_by_continent_year


def process_tourism_data(df):
    columns_to_keep = ['Entity', 'Year', 'Inbound arrivals of tourists']
    df = df[columns_to_keep]

    nan_exists = df.isnull().values.any()
    nan_counts = df.isnull().sum().to_dict()
    
    print("NaN values exist:", nan_exists)
    if nan_exists:
        print("NaN value counts per column:", nan_counts)

    df = df.rename(columns={'Entity': 'location'})
    df = df.rename(columns={'Year': 'year'})
    df = df.rename(columns={'Inbound arrivals of tourists': 'Nb_tourists'})
    df_filtered = df[(df['year'] >= 2018) & (df['year'] <= 2023)]
    
    return df_filtered


def continent_Tourist(data):
    consumption_by_continent_year = data.groupby(['continent', 'year'])['Nb_tourists'].sum().reset_index()
    return consumption_by_continent_year


sorted_dataR = load_process(dataR)
data_gov_consupmtion_continet = continent_Gov_Consump(sorted_dataR)
gov_consupmtion_data = iso_country(sorted_dataR)

sorted_dataCC = load_process_consumption(dataC)
data_private_consupmtion_continet = continent_Consumption(sorted_dataCC)
sorted_dataC = load_process_consumption(dataC)
private_consupmtion_data = iso_country(sorted_dataC)

data_death = load_and_process_death_data(dataD)
combined_data = pd.merge(sorted_dataR[['continent','year','location']], data_death, on=['year','location','continent'], how='inner')
data_death_continent=continent_total_deaths(combined_data)
iso_data_death=iso_country(data_death)

data_tourist = process_tourism_data(dataT)
combined_data = pd.merge(sorted_dataCC[['continent','year','location']], data_tourist, on=['year','location'], how='inner')
data_tourist_continet=continent_Tourist(combined_data)







######################################### WIDGETS #########################################


def make_ctry_dropdown(category):
    if category == 'Gov_Consump':
        df = gov_consupmtion_data  
    elif category == 'Consumption':
        df = private_consupmtion_data  
    return [{'label': country, 'value': country} for country in df['location'].unique()]


options=[{'label': country, 'value': country} for country in gov_consupmtion_data['location'].unique()]

ctry_dropdown_Gov_Consump = dcc.Dropdown(
    id="Gov_Consump_column",
    options=make_ctry_dropdown("Gov_Consump"),  
    value="France",
    clearable=False
)

ctry_dropdown_Consumption = dcc.Dropdown(
    id="Consumption_column",
    options=make_ctry_dropdown("Consumption"),  
    value="France",
    clearable=False
)

radio_main_category1= dbc.RadioItems(
        id='main_category1', 
        className='radio',
        options = [
           dict(label='Government Consumption', value=0), 
           dict(label='Private Consumption', value=1), 
        ],
        value=0, 
        inline=True
    )





################################### PAGE LAYOUT ######################################

layout = html.Div(children=[

    html.Div([
       html.H1("Impact of Covid-19 on Consumption Trends", className="fw-bold text-center"),
       html.Br(),
       html.P("COVID-19 led to a surge in government consumption as nations increased spending on healthcare, social safety nets, and economic relief to manage the crisis. Meanwhile, private consumption declined due to lockdowns, reduced income, and economic uncertainty, shifting the balance of GDP reliance towards government expenditure."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         
    html.Div([
        html.Label("CHOOSE A METRIC TO KNOW MORE"), 
        html.Br(),
        html.Br(),
        radio_main_category1,
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

    html.Div(id = 'dynamic_layout1'),

    html.Br(),
    html.Br(),
    html.Br(),
])
    




################################### CALLBACKS #########################################
  
@callback(
    Output('dynamic_layout1', 'children'),
    Input("main_category1", "value")
)
def display_layout(main_category1):
    
    if main_category1 == 0:  

        ret = html.Div([

            html.Div([               
                html.Div([
                    html.Br(),
                    html.H4("Overall Analysis"),
                    html.Br(),
                    dcc.Graph(id='gov-consupmtion-map'),
                    html.Br(),
                    dcc.Graph(id='Total-death-map'),
                    html.Br(),
                ], className='box', style={'width': '50%', 'padding': '10px'}),

                html.Div([
                    html.Br(),
                    dcc.Dropdown(
                        id='data_death_country',
                        options=[{'label': country, 'value': country} for country in data_death['location'].unique()],
                        value=data_death['location'].unique()[0],
                        placeholder='Choose a country'
                    ),
                    html.Br(),
                    dcc.Graph(id='gov-consupmtion-lineplot'),
                    html.Br(),
                    dcc.Graph(id='Total-cases-lineplot'),
                    html.Br(),
                ], className='box', style={'width': '50%', 'padding': '10px'}),
            ], style={'display': 'flex', 'width': '100%'}),
        

            html.Div([    
                html.Div([
                    html.Br(),
                    html.Div([
                        html.Div([
                        html.P("During the COVID-19 pandemic, governmental consumption surged as countries ramped up spending to manage the crisis. Lockdown measures and health emergencies forced governments to allocate significant resources toward public health systems, social safety nets, and economic stimulus packages. This increased spending was aimed at supporting overwhelmed healthcare services, providing financial aid to individuals and businesses, and maintaining essential public services amidst widespread disruption. "),
                        html.P("As private consumption and investment declined, government expenditure became a crucial driver of GDP. However, this sharp rise in governmental consumption often led to higher fiscal deficits, as many nations faced the challenge of balancing emergency spending with long-term economic recovery."),
                        ], className='box_comment fs-5 text-center'),
                    ], className="col-md-4"),

                    html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.P("Impact on Global Governmental Consumption(2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("Overall Increase by ~10-15%", className="fw-bold text-info display-5 text-center"),
                    html.P("(Driven by healthcare spending, economic relief, public services, crisis management)", className="fs-5 text-center"),
                    ], className="col-md-4"),
                    
                    html.Div([
                        html.Div([
                        html.P("High mortality rates, such as those seen during health crises, can significantly strain government budgets. Increased spending on healthcare, social welfare, and economic stimulus becomes essential to counter the drop in productivity and stabilize the economy."),
                        html.P("Manufacturing sectors like automotive and electronics, heavily impacted by labor shortages and supply chain disruptions, may require government support to prevent mass layoffs and stabilize production."),
                        html.P("Countries with limited domestic supply chains face even greater fiscal pressures, as emergency imports and reactive spending can divert funds from essential services and disrupt long-term financial planning."),
                        ], className='box_comment fs-5 text-center'),
                    ], className="col-md-4"),
                ], className='row mb-5'),
            ],className = 'box', style={'width': '100%'}),
        ])
    

    elif main_category1 == 1:
      ret = html.Div([
          html.Div([              
              html.Div([
                    html.Br(),
                    html.H4("Overall Analysis"),
                    html.Br(),
                    dcc.Graph(id='Consupmtion-map'),
                    html.Br(),
                    dcc.Graph(id='Consupmtion-lineplot'),
                    html.Br(),
                ], className='box', style={'width': '50%', 'padding': '10px'}),
            
          html.Div([
              html.Br(),
              dcc.Graph(id='Nb-tourists-lineplot'),  # New line plot added here
              html.Br(),
              html.P("In tourism-dependent countries, the collapse in global travel due to restrictions and safety concerns severely impacted private consumption. Nations reliant on international visitors saw sharp declines in tourism-related spending, which is essential for local businesses in hospitality, retail, and entertainment sectors.", className = 'box_comment fs-5 text-center'),
              html.P("These industries, already vulnerable to economic cycles, faced drastic slowdowns, leading to layoffs, wage cuts, and even permanent closures, particularly for small and medium-sized businesses that lacked the resources to survive prolonged closures. The reduction in tourism spending affected entire local economies, reducing demand for a wide range of goods and services, from transportation to food supplies.",className = 'box_comment fs-5 text-center'),
              html.P("Some countries attempted to mitigate these losses by promoting domestic tourism, with mixed success, as consumer behavior shifted and many remained cautious about travel. The uneven pace of recovery across countries and sectors highlighted broader economic imbalances, with some nations better adapting to new consumer priorities and health-related travel regulations, while others struggled to revive their tourism and service sectors fully.",className = 'box_comment fs-5 text-center'),
          ], className='box', style={'width': '50%', 'padding': '10px'}),
          ], style={'display': 'flex', 'width': '100%'}),
      

          html.Div([    
              html.Div([
                  html.Br(),
                      html.Div([
                          html.Div([
                              html.P("The COVID-19 pandemic had a transformative effect on private consumption, fundamentally altering spending patterns and reshaping the global economy. Lockdowns and social distancing measures led to a sudden contraction in consumer demand for many services and non-essential goods, particularly in industries such as retail, entertainment, and food services. With reduced incomes and heightened uncertainty, many households shifted their focus toward saving, further depressing demand in non-essential sectors."),
                              html.P("Spending on discretionary items like fashion, electronics, and recreation saw steep declines, while online shopping and home-based products, such as exercise equipment, home office supplies, and streaming services, saw significant increases."),
                              html.P("The pandemic also highlighted and accelerated global shifts toward e-commerce and digital consumption, as consumers increasingly turned to online shopping in lieu of physical stores. This rapid digital transition impacted traditional brick-and-mortar retail businesses, leading to widespread closures, especially for small businesses unable to pivot online as effectively."),
                          ], className='box_comment fs-5 text-center'),
                      ], className="col-md-4"),

                      html.Div([
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.P("Global Private Consumption Decline (2020)", className="fw-bold text-primary fs-4 text-center"),
                          html.P("Overall reduction by ~6-10% ", className="fw-bold text-info display-5 text-center"),
                          html.P("(Driven by lower consumer confidence, reduced household incomes, and widespread restrictions on movement)", className="fs-5 text-center"),
                      ], className="col-md-4"),

                      html.Div([
                          html.Div([
                              html.P("Globally, the shift impacted supply chains, causing delays and shortages in certain goods, as businesses were unprepared for sudden surges in demand for home-focused items and decreased demand in others. This led to disruptions in international trade, further affecting countries heavily reliant on exports."),
                              html.P("As private consumption declined, many economies faced reduced GDP growth, particularly in consumption-driven nations like the United States and China. The sudden drop in demand strained global supply chains and created ripple effects that extended to production, manufacturing, and logistics sectors worldwide. "),
                              html.P("Developing countries with limited fiscal capacity struggled even more, as lower private consumption reduced tax revenues and increased reliance on external borrowing to fund economic recovery initiatives. The long-term impact has resulted in uneven recoveries across regions, with countries facing challenges such as workforce shortages, inflation, and disrupted trade flows, which continue to shape the global economy’s post-pandemic landscape."),
                          ], className='box_comment fs-5 text-center'),
                      ], className="col-md-4"),
                  ], className='row mb-5')
              ], className = 'box', style={'width': '100%'}),
          ])
    
    return ret



@callback(
    [
        Output('gov-consupmtion-map', 'figure'),
        Output('gov-consupmtion-lineplot', 'figure'),
        Output('Total-cases-lineplot', 'figure'),
        Output('Total-death-map', 'figure')
    ],
    Input("data_death_country", "value")
)


def update_country_graphs(data_death_country):
    
    map_fig = px.choropleth(
        gov_consupmtion_data,
        locations="iso_alpha",
        color="Gov_Consump",
        animation_frame="year",
        title="Global Consumption Trends Over the Years",
        labels={"Gov_Consump": 'Value'}
    )

    line_fig = px.line(
        data_gov_consupmtion_continet,
        x='year',
        y='Gov_Consump',
        color='continent',
        title="Continent Specific Consumption Trends",
        labels={'Gov_Consump': 'Value', 'year': 'Year'}
    )
    
    data_death_data_country = data_death[data_death['location'] == data_death_country]
    data_death_fig = px.line(
        data_death_data_country,
        x='year',
        y='total_cases',
        title=f"Death Count Analysis for {data_death_country}",
        labels={'total_cases': 'Count', 'year': 'Year'}
    )
    total_deaths_map = px.choropleth(
        iso_data_death,
        locations="iso_alpha",
        color="total_deaths",
        animation_frame="year",
        range_color=[0, 400000] ,
        title="Global Death Count Due to Coronavirus",
        labels={"total_deaths": 'Count'}
    )

    return map_fig, line_fig, data_death_fig ,  total_deaths_map



@callback(
    [
        Output('Consupmtion-map', 'figure'),
        Output('Consupmtion-lineplot', 'figure'),
        Output('Nb-tourists-lineplot', 'figure')
    ],
    Input("main_category1", "value")
)

def update_private_consupmtion_graphs(main_category1):

    if main_category1 == 1:
        Consupmtion_map_fig = px.choropleth(
            private_consupmtion_data,
            locations="iso_alpha",
            color="Consumption",  
            animation_frame="year",
            title="Global Private Consumption Trends",
            labels={'Consumption': 'Value'}
        )
        Consupmtion_map_fig.update_geos(showcoastlines=True, coastlinecolor="Black")

        private_consupmtion_lineplot_fig = px.line(
            data_private_consupmtion_continet,
            x='year',
            y='Consumption',  
            color='continent',
            title="Private Consumption Trends by Continent",
            labels={'Consumption': 'Private Consumption Value', 'year': 'Year'}
        )

        Nb_tourists_lineplot_fig = px.line(
            data_tourist_continet,
            x='year',
            y='Nb_tourists',
            color='continent',
            title="Tourism Trends by Continent",
            labels={'Nb_tourists': 'Number of Tourists', 'year': 'Year'}
        )

        return Consupmtion_map_fig, private_consupmtion_lineplot_fig, Nb_tourists_lineplot_fig


    return go.Figure(), go.Figure(), go.Figure()
