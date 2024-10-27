import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/EmploymentLabour', name="Employment & Labour Market", order=4)




################################### DATA #########################################

df = pd.read_csv("data/economic_data.csv", index_col='date', parse_dates=True)
df['unemployment rate'] = df['unemployment rate'].str.replace('%', '').astype(float)

country_options = [{'label': country, 'value': country} for country in df['country'].unique()]
default_country = "France"





################################### PAGE LAYOUT #########################################

layout = html.Div(children=[
   
    html.Div([
        html.H1("Impact of Covid-19 on Unemployment Rates", className="fw-bold text-center"),
        html.Br(),
        html.P("The following graphs provide a comprehensive analysis of unemployment rates across multiple countries during different time periods. The data shows significant fluctuations in unemployment rates during the COVID-19 pandemic, with some countries experiencing more severe impacts. Countries with stronger social protection measures or targeted policies managed to stabilize employment rates more effectively. This analysis will help us better understand the global economic uncertainties and recovery trends post-pandemic."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         
    html.Br(),
    html.Div([
        html.Br(),
        html.H3("Global Unemployment Analysis", style={'padding': '5px', 'border-radius': '5px'}),
        html.Br(),
        dcc.Graph(id='unemployment-map'),
    ], className='box', style={'margin': '10px', 'padding': '15px'}),

    
    html.Div([
        html.Div([
            html.Br(),
            html.H3("Unemployment Rate Over Time", style={'padding': '5px', 'border-radius': '5px'}),
            html.Br(),
            dcc.Dropdown(
                id='country-dropdown',
                options=country_options,
                value=default_country,
                clearable=False,
                placeholder = 'Select a Country',
            ),
            html.Br(),
            dcc.Graph(id="unemployment-plot", style = {'width': '100%','padding': '10px'}),
            html.Br(),
            html.Br(),
        ], className='box', style={'width': '70%', 'padding': '10px'}),
        

        html.Div([
            html.Br(),
            html.Div([
                html.P("The COVID-19 pandemic caused global unemployment rates to soar as lockdowns and reduced demand led to business closures and layoffs. In 2020, the International Labour Organization (ILO) reported an estimated loss of 255 million full-time jobs worldwide, with global working hours dropping by 8.8%, a figure four times greater than the 2009 financial crisis."),
                html.P("Youth and women were disproportionately affected, particularly in sectors like retail, hospitality, and tourism. Unemployment rates in advanced economies rose from an average of 5.4% in 2019 to over 7% in 2020, while in low- and middle-income countries, job losses hit informal and low-income workers especially hard. Recovery has been uneven, with unemployment remaining elevated in sectors slow to rebound."),
                html.P("Unemployment rates in advanced economies rose from an average of 5.4% in 2019 to over 7% in 2020, while in low- and middle-income countries, job losses hit informal and low-income workers especially hard. Recovery has been uneven, with unemployment remaining elevated in sectors slow to rebound."),
            ], className = 'box_comment fs-5 text-center',style={'padding': '10px', 'border-radius': '5px'}),
            html.Br(),
        ], className='box', style={'width': '30%', 'padding': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin': '20px'}),

    html.Br(),
    html.Br(),
    html.Br(),
])





################################### CALLBACKS #########################################

@callback(
    Output('unemployment-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_unemployment_map(selected_country):
    fig = px.choropleth(
        df.reset_index(),
        locations='country',
        locationmode='country names',
        color='unemployment rate',
        hover_name='country',
        # animation = "date",
        scope='world',
        color_continuous_scale='Viridis',  
        projection="natural earth"
    )
    fig.update_layout(title_x=0.5, margin={"r":0, "t":50, "l":0, "b":0}, geo=dict(showframe=False))
    return fig


@callback(
    Output('unemployment-plot', 'figure'),
    Input('country-dropdown', 'value')
)
def update_unemployment_plot(selected_country):
    filtered_df = df[df['country'] == selected_country]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['unemployment rate'], mode='lines', name=selected_country))
    fig.update_layout(title=f"Unemployment Rate Over Time for {selected_country}", height=600, width=900)
    return fig
