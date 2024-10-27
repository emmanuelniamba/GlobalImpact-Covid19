import dash
from dash import dcc, html, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import country_converter as coco


dash.register_page(__name__, path='/ConsumerConfidence', name="Consumer Confidence Analysis", order=70)






####################### DATA #############################

df = pd.read_csv("data/consumer_idx.csv")

df_long = pd.melt(df, id_vars=['Time period'], var_name='date', value_name='consumer_confidence')
df_long['date'] = pd.to_datetime(df_long['date'], errors='coerce')  
df_long.rename(columns={'Time period': 'country'}, inplace=True)
df_long.dropna(inplace=True) 

df_long['iso_alpha'] = coco.convert(names=df_long['country'], to='ISO3')
df_long['continent'] = coco.convert(names=df_long['country'], to='continent')

df_long['year'] = df_long['date'].dt.year
df_continent = df_long.groupby(['continent', 'year'])['consumer_confidence'].mean().reset_index()






####################### PAGE LAYOUT #############################

layout = html.Div(children=[

    html.Div([
       html.H1("Impact of Covid-19 on Consumer Confidence", className="fw-bold text-center"),
       html.Br(),
       html.P("Consumer confidence declined during COVID-19 across all continents due to widespread economic uncertainty, job losses, and health concerns. Lockdowns and business closures led to reduced incomes and unemployment, making consumers cautious about spending. Fear of the virus and the unpredictability of the crisis further fueled pessimism about the economic future, causing a sharp drop in confidence."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

    html.Div([
        html.Div([
            html.Br(),
            html.H3("Consumer Confidence by Country:", style={'padding': '5px', 'border-radius': '5px'}),
            html.Br(),
            dcc.Graph(id="consumer-confidence-map"),
            html.Br(),
        ], className='box', style={'width': '50%', 'padding': '10px'}),

        html.Div([
            html.Br(),
            html.H4("Consumer Confidence Trends by Continent", style={'padding': '5px', 'border-radius': '5px'}),
            html.Br(),
            dcc.Graph(id="consumer-confidence-continent-line"),
            html.Br(),
        ], className='box', style={'width': '50%', 'padding': '10px'}),
    ], style={'display': 'flex', 'width':'100%','justify-content': 'space-between', 'margin': '20px'}),

    html.Div([
        html.Div([

            html.Br(),
            html.Div([
                html.Br(),
                html.P("U.S. Consumer Confidence Index (2020)", className="fw-bold text-primary fs-4 text-center"),
                html.P("↓ 30%", className="fw-bold text-info display-5 text-center"),  
                html.P("(Decline due to uncertainty in job security and financial markets)", className="fs-5 text-center"),  
            ], className="col-md-3"),

            html.Div([
                html.Br(),
                html.P("Eurozone Consumer Confidence (2020)", className="fw-bold text-primary fs-4 text-center"),
                html.P("↓ 22%", className="fw-bold text-info display-5 text-center"),  
                html.P("(Impacted by lockdowns, restrictions, and decreased spending)", className="fs-5 text-center"),  
            ], className="col-md-3"),

            html.Div([
                html.Br(),
                html.P("Japan’s Consumer Confidence Index (2020)", className="fw-bold text-primary fs-4 text-center"),
                html.P("↓ 18% ", className="fw-bold text-info display-5 text-center"),  
                html.P("(Reduced confidence due to virus concerns and economic slowdown)", className="fs-5 text-center"),  
            ], className="col-md-3"),

            html.Div([
                html.Br(),
                html.P("China Consumer Confidence Index (2020)", className="fw-bold text-primary fs-4 text-center"),
                html.P("↓ 12%", className="fw-bold text-info display-5 text-center"),  
                html.P("(Decreased spending despite early recovery from lockdowns)", className="fs-5 text-center"),  
            ], className="col-md-3"),

            html.Div([
                html.P("Consumer confidence globally dropped significantly due to COVID-19, driven by job insecurity, reduced income, and heightened uncertainty. The declines in consumer confidence impacted economic recovery, as spending fell across sectors.", 
                    className='box_comment fs-5 text-center'),
            ], className="col-md-6"),

            html.Div([
                html.P("Countries with strict lockdowns and prolonged restrictions observed the steepest declines in consumer confidence, affecting both large and small businesses as demand for goods and services shrank.",
                    className='box_comment fs-5 text-center'),
            ], className="col-md-6"),
        ], className='row mb-5'),
    ],className='box',style={'width':'100%'}),

    html.Br(),
    html.Br(),
    html.Br(),
])






####################### CALLBACKS #############################

@callback(
    Output('consumer-confidence-map', 'figure'),
    Input('consumer-confidence-map', 'id')  
)

def update_consumer_confidence_map(_):
    fig = px.choropleth(
        df_long,
        locations='iso_alpha',
        color='consumer_confidence',
        animation_frame='year',
        title='Global Consumer Confidence Trends Over Time',
        color_continuous_scale='Viridis'
    )
    return fig


@callback(
    Output('consumer-confidence-continent-line', 'figure'),
    Input('consumer-confidence-map', 'id')  
)
def update_continent_line_plot(_):
    fig = px.line(
        df_continent,
        x='year',
        y='consumer_confidence',
        color='continent',
        title='Consumer Confidence Trends by Continent',
        markers=True
    )
    return fig
