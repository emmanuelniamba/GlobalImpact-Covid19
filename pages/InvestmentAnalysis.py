import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Output
import country_converter as cc
import logging

dash.register_page(__name__, path='/InvestmentAnalysis', name="Investment Statistics", order=13)





####################### DATA #############################

logger = logging.getLogger('country_converter')
logger.setLevel(logging.ERROR)

dataR = pd.read_csv("data/Investment_data.csv", sep=',', skiprows=4, header=None)

def load_process(data):
    column_names = data.iloc[0]
    data.columns = column_names
    data = data.drop(data.index[0])
    selected_columns = ['Country Name', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0]
    new_data = data[selected_columns]
    data.columns = data.columns.astype(str)
    value_vars = [col for col in data.columns[4:] if col != 'nan']
    melted_data = pd.melt(data, id_vars=['Country Name'], value_vars=value_vars, var_name='year', value_name='Investment')
    melted_data['year'] = pd.to_numeric(melted_data['year'])
    filtered_data = melted_data[melted_data['year'].isin([2018, 2019, 2020, 2021, 2022, 2023])]
    sorted_data = filtered_data.sort_values(['Country Name', 'year'])
    sorted_data['year'] = sorted_data['year'].astype(int)
    sorted_data = sorted_data.rename(columns={'Country Name': 'location'})
    sorted_data['continent'] = cc.convert(names=sorted_data['location'], to='continent')
    sorted_data = sorted_data[sorted_data['continent'] != 'not found']
    return sorted_data

def continent_Investment(data):
    return data.groupby(['continent', 'year'])['Investment'].sum().reset_index()

def iso_country(data):
    data['iso_alpha'] = cc.convert(names=data['location'], to='ISO3')
    return data

sorted_data = load_process(dataR)
data1 = continent_Investment(sorted_data)
data2 = iso_country(sorted_data)






####################### CHARTS #############################

def update_graph_continent(data):
    fig = px.line(data, x='year', y='Investment', color='continent')
    fig.update_layout(
        title='Investment by Continent Over the Years',
        title_x=0.5,
        font=dict(family="Arial, sans-serif", size=12)
    )
    return fig

def plot_choropleth_map(data):
    fig = px.choropleth(
        data,
        locations="iso_alpha",
        color="Investment",
        hover_name="location",
        animation_frame="year",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig.update_layout(
        title='Global Investment Over Time',
        title_x=0.5,
        font=dict(family="Arial, sans-serif", size=12)
    )
    return fig





####################### PAGE LAYOUT #############################


layout = html.Div(children=[

    html.Div([
       html.H1("Impact of Covid-19 on Investment", className="fw-bold text-center"),
       html.Br(),
       html.P("The COVID-19 pandemic significantly impacted global investment flows, with many regions facing downturns due to economic uncertainty and market disruptions. Investments were redirected toward healthcare and technology sectors, while industries like tourism and hospitality saw declines."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
        
    # Row 1
    html.Div([
        html.Div([
            html.Br(),
            dcc.Graph(id="Investment_graph1", figure=update_graph_continent(data1)),
        ],className='box', style={'width':'60%','margin': '10px'}),
                
            
        html.Div([
            html.Br(),
            html.H3("Investment Insights"),
            html.Br(),
            html.Div([
                html.P("During the Covid-19 pandemic, investments were significantly impacted worldwide, with sharp declines in various sectors. This visualization highlights the changes in investment by continent, showing how different regions experienced fluctuations due to the economic effects of the pandemic."),
                html.P("For major companies, especially in the U.S., economic downturns and unfavorable financial conditions led to negative returns. This data provides insights into how investments shifted over time in response to global market dynamics.")
            ],className='box_comment fs-5 text-center'),
        ], className='box', style={'width':'40%','margin': '10px'}),
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
            dcc.Graph(id="Investment_graph2", figure=plot_choropleth_map(data2))
        ]
    ),

    html.Br(),
    html.Br(),
    html.Br(),
])
