
import dash  
from dash import dcc, html , callback
import plotly.express as px  
import pandas as pd  
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output  , State
from plotly.subplots import make_subplots
import country_converter as cc
import plotly.graph_objects as go


dash.register_page(__name__, path='/trade', name="Trade Market", order=3)



################################### DATA #########################################

dataR = pd.read_csv("data/Export.csv", sep=',', skiprows=4, header=None)
dataI = pd.read_csv("data/Import.csv", sep=',', skiprows=4, header=None)
dataM = pd.read_csv("data/manufacturing.csv", sep=',', skiprows=4, header=None)


###### EXPORT ######
def load_process_export(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    data = data[selected_columns]

    data.columns = data.columns.astype(str)
    data = data.rename(columns={'Country Name': 'location'})
    data['diff_2020_2019_export'] = data['2020.0'] - data['2019.0']
    
    value_vars = ['2018.0', '2019.0', '2020.0', '2021.0', '2022.0', '2023.0']
    melted_data = pd.melt(data, id_vars=['location', 'diff_2020_2019_export'], value_vars=value_vars, var_name='year', value_name='Export')
    
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    melted_data = melted_data.sort_values(['location', 'year'])
    melted_data['year'] = melted_data['year'].astype(int)
    melted_data['continent'] = cc.convert(names=melted_data['location'], to='continent')    
    melted_data = melted_data[melted_data['continent'] != 'not found']
    
    return melted_data

def continent_Export(data):
  Import_by_continent_year = data.groupby(['continent', 'year'])['Export'].sum().reset_index()
  return Import_by_continent_year



###### MANUFACTURING ######
def load_process_manufacturing(data):
  column_names = data.iloc[0]
  data.columns = column_names
  data = data.drop(data.index[0])
  selected_columns = ['Country Name',2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
  new_data = data[selected_columns]
  data.columns = data.columns.astype(str)
  value_vars = [col for col in data.columns[4:] if col != 'nan']
  melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='Manufacturing')
  melted_data['year'] = pd.to_numeric(melted_data['year'])
  filtered_data = melted_data[melted_data['year'].isin([2018,2019,2020, 2021, 2022, 2023])]
  unique_years = filtered_data['year'].unique()
  sorted_data = filtered_data.sort_values('Country Name')
  sorted_data = filtered_data.sort_values(['Country Name', 'year'])
  sorted_data['year'] = sorted_data['year'].astype(int)
  sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
    
  return sorted_data


###### IMPORT ######
def load_process_import(data):
  column_names = data.iloc[0]
  data.columns = column_names
  data = data.drop(data.index[0])
  selected_columns = ['Country Name',2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
  new_data = data[selected_columns]
  data.columns = data.columns.astype(str)
  value_vars = [col for col in data.columns[4:] if col != 'nan']
  melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='Import')
  melted_data['year'] = pd.to_numeric(melted_data['year'])
  filtered_data = melted_data[melted_data['year'].isin([2018,2019,2020, 2021, 2022, 2023])]
  unique_years = filtered_data['year'].unique()
  sorted_data = filtered_data.sort_values('Country Name')
  sorted_data = filtered_data.sort_values(['Country Name', 'year'])
  sorted_data['year'] = sorted_data['year'].astype(int)
  sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
  sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')
  nan_count_continent = sorted_data['continent'].isnull().sum()
  nan_count_continent = sorted_data['Import'].isnull().sum()
  nan_counts_by_year = sorted_data.groupby('year')['Import'].apply(lambda x: x.isnull().sum())
  sorted_data = sorted_data[sorted_data['continent'] != 'not found']
  return sorted_data

def continent_Import(data):  
  Import_by_continent_year = data.groupby(['continent', 'year'])['Import'].sum().reset_index()
  return Import_by_continent_year

def iso_country(data):   
   data['iso_alpha'] = cc.convert(names=data['location'], to='ISO3')
   return data
   

###### LOADING AND PROCESSING DATA ######    
export_data_not_iso = load_process_export(dataR)
manufacturing_data = load_process_manufacturing(dataM)
export_data=iso_country(export_data_not_iso)
import_data_not_iso=load_process_import(dataI)
export_data_continent=continent_Export(export_data_not_iso)
import_data_continent=continent_Import(import_data_not_iso)
import_data=iso_country(import_data_not_iso)



###### MAKING THE DROPDOWN ######
def make_ctry_dropdown(category):
    if category == "Export":
        df = export_data  
    elif category == "Import":
        df = import_data  

    return [{'label': country, 'value': country} for country in df['location'].unique()]


options=[{'label': country, 'value': country} for country in export_data['location'].unique()]




######################################### WIDGETS #########################################

ctry_dropdown_Export = dcc.Dropdown(
    id="Export_column",
    options=make_ctry_dropdown("Export"),  
    value="France",
    clearable=False
)

ctry_dropdown_Import = dcc.Dropdown(
    id="Import_column",
    options=make_ctry_dropdown("Import"),  
    value="France",
    clearable=False
)

radio_main_category= dbc.RadioItems(
        id='main_category', 
        className='radio',
        options = [
           dict(label='Export ', value=0), 
           dict(label='Import', value=1), 
        ],
        value=0, 
        inline=True
    )






################################### PAGE LAYOUT #########################################


layout = html.Div(children=[

    # HEADING
    html.Div([
       html.H1("Impact of Covid-19 on Trade Market", className="fw-bold text-center"),
       html.Br(),
       html.P("The COVID-19 pandemic disrupted global trade markets, leading to supply chain bottlenecks, reduced consumer demand, and volatile prices. Many industries faced significant losses, while e-commerce and digital services saw accelerated growth as consumer behavior shifted online."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         

    # RADIO BUTTONS TO SELECT THE METRIC
    html.Div([
        html.Label("CHOOSE A METRIC TO KNOW MORE"), 
        html.Br(),
        html.Br(),
        radio_main_category,
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

    
    # LAYOUT BASED ON THE BUTTON
    html.Div(id = 'dynamic_layout')
])
    




################################### CALLBACKS #########################################
  
@callback(
    Output('dynamic_layout', 'children'),
    Input("main_category", "value")
)
def display_layout(main_category):
    
    if main_category == 0:  # Exports selected

        
        ret = html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    dcc.Dropdown(
                        id='export_country',
                        options=[{'label': country, 'value': country} for country in export_data['location'].unique()],
                        value=export_data['location'].unique()[0],
                        placeholder='Choose a country'
                    ),
                    html.Br(),
                    dcc.Graph(id='export-lineplot-country'),
                    html.Br(),
                    dcc.Graph(id='manufacturing-lineplot'),
                ], className='box', style={'width': '50%', 'padding': '10px'}),
                
                html.Div([
                    html.Br(),
                    html.H4("Overall Analysis of the Exports Sector"),
                    html.Br(),
                    dcc.Graph(id='exports-lineplot'),
                    html.Br(),
                    dcc.Graph(id='exports-map'),
                    html.Br(),
                ], className='box', style={'width': '50%', 'padding': '10px'}),
            ], style={'display': 'flex', 'width': '100%'}),
        
            html.Div([    
                html.Div([
                    html.Br(),
                    html.Div([
                        html.Div([
                        html.P("During the COVID-19 pandemic, global exports encountered unprecedented challenges as countries imposed strict lockdown measures to curb the spread of the virus. These lockdowns not only restricted the movement of people but also led to significant disruptions in supply chains, creating a ripple effect that was felt worldwide. Industries heavily reliant on cross-border raw materials faced severe production declines, as restrictions on trade and transportation hampered their ability to source essential components. This resulted in a marked decrease in export volumes, with many nations grappling with an oversupply of finished goods and a backlog of orders."),
                        ], className='box_comment fs-5 text-center'),
                    ], className="col-md-4"),

                    html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.P("Impact on Global Exports (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("Overall decline by ~7.6%", className="fw-bold text-info display-5 text-center"),
                    html.P("(driven by disrupted supply chains and trade restrictions)", className="fs-5 text-center"),
                    ], className="col-md-4"),
                    
                    html.Div([
                        html.Div([
                        html.P("Manufacturing activity experienced a sharp decline across numerous sectors globally, with the automobile and electronics industries among the hardest hit. Factories that relied on just-in-time manufacturing processes were particularly vulnerable, as delays in raw material shipments halted production lines. The automotive sector, for example, saw many plants temporarily shut down, leading to significant financial losses and layoffs. Recovery from these setbacks varied considerably across countries. Nations with robust domestic supply chains and diversified sourcing strategies managed to bounce back faster, rapidly ramping up production as lockdowns eased."),
                        ], className='box_comment fs-5 text-center'),
                    ], className="col-md-4"),
                ], className='row mb-5'),
            ],className = 'box', style={'width': '100%'}),
        ])
    

    elif main_category == 1:  # Imports selected
        
        ret = html.Div([
        
            html.Div([
                html.Div([
                    html.Br(),
                    dcc.Graph(id='imports-map'),
                    html.Br(),
                ], className='box', style={'width': '50%', 'padding': '10px'}),
            
                html.Div([
                    html.Br(),
                    dcc.Graph(id='imports-lineplot'),
                    html.Br(),
                ], className='box', style={'width': '50%', 'padding': '10px'}),
            ], style={'display': 'flex', 'width': '100%'}),
        
            html.Div([    
                html.Div([
                    html.Br(),
                        html.Div([
                            html.Div([
                                html.P("The COVID-19 pandemic led to significant disruptions in global imports, primarily due to widespread border restrictions, reduced international shipping capacity, and logistical challenges arising from lockdown measures. Many countries prioritized the importation of essential goods, such as medical supplies, pharmaceuticals, and food products, to ensure public health and safety. As a result, imports of non-essential items, including luxury goods and electronics, experienced a sharp decline. The shift in focus toward essential commodities caused substantial imbalances in global trade, as industries dependent on a broad spectrum of imported raw materials struggled to maintain production schedules."),
                            ], className='box_comment fs-5 text-center'),
                        ], className="col-md-4"),

                        html.Div([
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.P("Global Imports Decline (2020)", className="fw-bold text-primary fs-4 text-center"),
                            html.P("Overall reduction by ~9%", className="fw-bold text-info display-5 text-center"),
                            html.P("(driven by lower consumer demand and restricted cross-border movement)", className="fs-5 text-center"),
                        ], className="col-md-4"),

                        html.Div([
                            html.Div([
                                html.P("Countries heavily reliant on imports for their manufacturing sectors faced the most severe impacts. Industries such as electronics and automotive experienced significant slowdowns as supply chains were interrupted, leading to production delays and decreased output. The automotive sector, for instance, saw factories temporarily shut down due to shortages of critical components sourced from overseas. Recovery varied widely among nations, with some adapting more swiftly to new trade dynamics than others. As countries began to reassess and reconfigure their supply chains, the path to recovery involved navigating new regulations and logistical hurdles while striving to restore normalcy in international trade."),
                            ], className='box_comment fs-5 text-center'),
                        ], className="col-md-4"),
                    ], className='row mb-5')
                ],className = 'box', style={'width': '100%'}),
            ])

    return ret



# Callback for export
@callback(
    [
        Output('exports-map', 'figure'),
        Output('exports-lineplot', 'figure'),
        Output('export-lineplot-country', 'figure'),
        Output('manufacturing-lineplot', 'figure')
    ],
    Input("export_country", "value")
)

def update_country_graphs(export_country):
    
    map_fig = px.choropleth(
        export_data,
        locations="iso_alpha",
        color="Export",
        animation_frame="year",
        title="Export by Countries",
        labels={'Export': 'Export Value'}
    )

    
    export_data_country = export_data_not_iso[export_data_not_iso['location'] == export_country]
    export_lineplot_country_fig = px.line(
        export_data_country,
        x='year',
        y='Export',
        title=f"Export Over Time for {export_country}",
        labels={'Export': 'Export Value', 'year': 'Year'}
    )
    
    
    line_fig = px.line(
        export_data_continent,
        x='year',
        y='Export',
        color='continent',
        title="Export by Continent",
        labels={'Export': 'Export Value', 'year': 'Year'}
    )
    
    
    manufacturing_data_country = manufacturing_data[manufacturing_data['location'] == export_country]
    manufacturing_fig = px.line(
        manufacturing_data_country,
        x='year',
        y='Manufacturing',
        title=f"Manufacturing Value Analysis for {export_country}",
        labels={'Manufacturing': 'Manufacturing Value', 'year': 'Year'}
    )

    return map_fig, line_fig, export_lineplot_country_fig, manufacturing_fig



# Callback for import
@callback(
    [
        Output('imports-map', 'figure'),
        Output('imports-lineplot', 'figure')
    ],
    Input("main_category", "value")
)

def update_import_graphs(main_category):
    
    if main_category == 1:
        imports_map_fig = px.choropleth(
            import_data,
            locations="iso_alpha",
            color="Import",
            animation_frame="year",
            title="Import by Countries",
            labels={'Import': 'Import Value'}
        )
        imports_map_fig.update_geos(showcoastlines=True, coastlinecolor="Black")

        
        imports_lineplot_fig = px.line(
            import_data_continent,
            x='year',
            y='Import',
            color='continent',
            title="Import by Continent",
            labels={'Import': 'Import Value', 'year': 'Year'}
        )

        return imports_map_fig, imports_lineplot_fig
    
    return go.Figure(), go.Figure()