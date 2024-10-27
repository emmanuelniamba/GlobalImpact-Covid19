import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import country_converter as cc
import logging

dash.register_page(__name__, path='/GDPEconomic', name="GDP and Economic Growth", order=1)

logger = logging.getLogger('country_converter')
logger.setLevel(logging.ERROR)





######################## DATA ###############################

dataR = pd.read_csv("data/GDP.csv", sep=',', skiprows=4, header=None)

def load_process(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    new_data = data[selected_columns]
    data.columns = data.columns.astype(str)
    value_vars = [col for col in data.columns[4:] if col != 'nan']
    melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='GDP')
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    filtered_data = melted_data[melted_data['year'].isin([2018, 2019, 2020, 2021, 2022, 2023])]
    sorted_data = filtered_data.sort_values(['Country Name', 'year'])
    sorted_data['year'] = sorted_data['year'].astype(int)
    sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
    sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')
    sorted_data = sorted_data[sorted_data['continent'] != 'not found']
    return sorted_data

def continent_gdp(data):
    gdp_by_continent_year = data.groupby(['continent', 'year'])['GDP'].sum().reset_index()
    return gdp_by_continent_year

def iso_country(data):
    data['iso_alpha'] = cc.convert(names=data['location'], to='ISO3')
    return data

sorted_data = load_process(dataR)
data1 = continent_gdp(sorted_data)
data2 = iso_country(sorted_data)





###################### GRAPHS ###############################

def update_graph_continent(data):
    fig = px.line(data, x='year', y='GDP', color='continent')
    fig.update_layout(title='GDP by Continent and Year')
    return fig

def plot_choropleth_map(data):
    fig = px.choropleth(
        data,
        locations="iso_alpha",
        color="GDP",
        hover_name="location",
        animation_frame="year",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    return fig







###################### PAGE LAYOUT ###############################

layout = html.Div(children=[

    html.Div([
       html.H1("Impact of Covid-19 on GDP", className="fw-bold text-center"),
       html.Br(),
       html.P("The COVID-19 pandemic had a significant impact on global GDP, leading to economic contractions in many countries. Various sectors faced downturns, and recovery has been uneven across regions. This overview examines GDP trends during this tumultuous period."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
        
    # Row 1
    html.Div([
        html.Div([
            html.Br(),
            dcc.Graph(id="GDP_graph1", figure=update_graph_continent(data1)),
        ], className='box', style={'width':'60%', 'margin': '10px'}),
                
        html.Div([
            html.Br(),
            html.H3("GDP Insights"),
            html.Br(),
            html.Div([
                html.P("The impact of the COVID-19 pandemic on GDP has been profound, affecting both developed and developing economies. This visualization illustrates the GDP changes by continent, highlighting how different regions experienced varying degrees of economic contraction and recovery."),
                html.P("For many nations, economic activities were disrupted, leading to a decrease in consumer spending, investments, and trade. Understanding these trends is essential for analyzing future economic policies and recovery strategies.")
            ], className='box_comment fs-5 text-center'),
        ], className='box', style={'width':'40%', 'margin': '10px'}),
        
    ], style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px'}),

    # Row 2
    html.Div(
        style={
            'backgroundColor': '#fff',
            'padding': '15px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'margin-top': '20px'
        },
        children=[
            dcc.Graph(id="GDP_graph2", figure=plot_choropleth_map(data2))
        ]
    ),

    html.Div([
        html.Div([
            html.Br(),
            html.Div([
                html.P("The COVID-19 pandemic caused a significant decline in global GDP, primarily due to widespread lockdowns and disruptions in economic activity. Many countries experienced sharp contractions in their economies, affecting production, trade, and employment levels.", 
                    className='box_comment fs-5 text-center'),
            ], className="col-md-6"),

            html.Div([
                html.P("Developing nations faced steeper GDP declines compared to developed countries, as they often lacked the fiscal space to implement effective stimulus measures. The recovery has been uneven, with some regions rebounding faster than others, highlighting the need for tailored economic policies.",
                    className='box_comment fs-5 text-center'),
            ], className="col-md-6"),
        ], className='row mb-5'),
    ], className='box', style={'width': '100%'}),

    html.Br(),
    html.Br(),
    html.Br(),
])


