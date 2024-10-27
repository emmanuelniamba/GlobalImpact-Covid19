import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/GovtExpenditure', name="Government Expenditure", order=11)





####################### DATA #############################

file_path = 'data/US.GovExpenditures_20241023_083612.csv'
data = pd.read_csv(file_path)

data = data[(data['Year'] >= 2018) & (data['Year'] <= 2021)]

data['Year'] = data['Year'].astype(int)
filtered_data = data.drop([col for col in data.columns if 'MissingValue' in col], axis=1)




####################### WIDGETS #############################

radio_main_category = dbc.RadioItems(
    id='expenditure_category',
    className='radio',
    options=[
        dict(label='Agriculture', value='Agriculture, sylviculture, peche et chasse_Dollars_des_tatsUnis_aux_prix_courants_en_millions_Value'),
        dict(label='Healthcare', value='Protection de l\'environnement_Dollars_des_tatsUnis_aux_prix_courants_en_millions_Value'),
        dict(label='Energy', value='Combustibles et energie_Dollars_des_tatsUnis_aux_prix_courants_en_millions_Value')
    ],
    value='Agriculture, sylviculture, peche et chasse_Dollars_des_tatsUnis_aux_prix_courants_en_millions_Value',  # Set default to a valid value
    inline=True
)




####################### PAGE LAYOUT #############################

layout = html.Div(children=[

    html.Div([
       html.H1("Impact of Covid-19 on Government Expenditure", className="fw-bold text-center"),
       html.Br(),
       html.P("Here we discuss the impact of public expenditures on various sectors during the COVID-19 pandemic across multiple countries. Gain insights into changes in investment across agriculture, healthcare, energy, and other sectors."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         
    html.Div([
        html.Label("CHOOSE A METRIC TO KNOW MORE"),
        html.Br(),
        html.Br(),
        radio_main_category,
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

    html.Div([
        html.Div([
            html.Br(),
            html.Label("Select Country"),
            dcc.Dropdown(
                id="country_dropdown",
                options=[{'label': country, 'value': country} for country in filtered_data['Economy_Label'].unique()],
                value=filtered_data['Economy_Label'].unique()[0],
                clearable=False,
            ),
            html.Br(),
            dcc.Graph(id="expenditure_graph"),
        ], className='box', style={'width': '60%', 'padding': '20px'}),

        html.Div([
            html.H3("Interpretation", style={'padding': '10px', 'border-radius': '10px'}),
            html.P(id="interpretation"),
            html.Br(),
            html.Br(),
            html.P("The COVID-19 pandemic led to a significant increase in government expenditures worldwide. Spending surged in healthcare for vaccines, medical infrastructure, and public health measures, while social protection programs expanded to support unemployed and vulnerable populations. Many governments introduced stimulus packages and relief programs to sustain businesses and stabilize economies. Education spending shifted towards remote learning and infrastructure for safe reopening, while green energy and sustainable infrastructure gained traction as part of long-term recovery strategies. This unprecedented spending has implications for national debt and future fiscal policies.", className = 'box_comment fs-5 text-center'),
            html.Br()
        ], className='box', style={'width': '35%', 'padding': '20px'}),
        
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin': '20px'}),

    html.Div([
        html.Div([
            html.Br(),
            html.Br(),
            html.H3("Key Facts and Figures on Government Expenditure", style={'background-color': 'white', 'padding': '5px', 'border-radius': '5px'}),
            html.Br(),
        ], style={'margin': '10px', 'padding': '10px'}),

        html.Div([
            html.H4("Agriculture Expenditure", className="fw-bold"),
            html.P("During the pandemic, government expenditure in agriculture increased by an average of 10% in many countries to support food security and rural employment.", 
                   className='box_comment', style={'padding': '10px', 'border-radius': '5px'}),
        ], className='box', style={'width': '35%', 'margin': '10px'}),

        html.Div([
            html.H4("Healthcare Investment", className="fw-bold"),
            html.P("Healthcare spending surged in 2020, with increases of over 20% globally to address rising demands on health infrastructure, testing, and vaccine development.", 
                   className='box_comment', style={'padding': '10px', 'border-radius': '5px'}),
        ], className='box', style={'width': '35%', 'margin': '10px'}),

        html.Div([
            html.H4("Energy Sector Support", className="fw-bold"),
            html.P("Energy investments experienced a mixed trend; while renewable energy projects continued, fossil fuel investments faced cuts in many countries.", 
                   className='box_comment', style={'padding': '10px', 'border-radius': '5px'}),
        ], className='box', style={'width': '35%', 'margin': '10px'}),

    ], style={'display': 'flex', 'justify-content': 'space-around', 'margin': '20px'}),

    html.Br(),
    html.Br(),
    html.Br(),
])





####################### CALLBACKS #############################

@callback(
    [
        Output("expenditure_graph", "figure"),
        Output("interpretation", "children")
    ],
    [
        Input("country_dropdown", "value"),
        Input("expenditure_category", "value")
    ]
)

def update_expenditure_graph(selected_country, selected_category):
    filtered_country_data = filtered_data[filtered_data['Economy_Label'] == selected_country]
    
    fig = px.line(
        filtered_country_data,
        x='Year',
        y=selected_category,
        title=f'Government Expenditure in {selected_country}',
        markers=True
    )

    change = filtered_country_data[selected_category].diff().mean()
    interpretation = f"Analysis of expenditures for {selected_country}:\n"

    if change < 0:
        interpretation += f" Average decrease of {abs(change):.2f} million USD, possibly due to the reduced sectoral activity during COVID-19.\n"
    elif change > 0:
        interpretation += f" Average increase of {change:.2f} million USD, possibly indicating an increase in this sector during the pandemic.\n"
    else:
        interpretation += f" Expenditures were relatively stable over this period.\n"

    return fig, interpretation
