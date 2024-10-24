'''
7. Stock Market and Financial Markets
Page Name: "Stock Markets & Financial Systems"

Purpose: Investigate the impact of COVID-19 on stock markets, currencies, and financial systems.

Content:
Stock market performance before, during, and after the pandemic.
Comparison of stock indices (e.g., S&P 500, FTSE 100, Nikkei 225) during COVID-19.
Currency volatility and its impact on international trade.

Visualizations:
Line chart: Stock market indices over time.
Scatter plot: Stock market performance vs. GDP growth.
Heatmap: Correlation between stock markets and other economic indicators (e.g., inflation, trade).
'''

import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go

dash.register_page(__name__, path='/stock_market', name="Stocks and Finances", order=5)




################################### DATA #########################################


###### STOCKS TRADED ######
def stocks_traded_data():
    data = pd.read_csv("data/StocksTraded.csv", sep=',')
    # link to the dataset: https://databank.worldbank.org/reports.aspx?source=2&series=CM.MKT.TRAD.CD&country=#
    data.rename(columns={"Country Name":"Country"}, inplace=True)

    years = ["2017","2018","2019","2020","2021","2022","2023"]
    for year in years:
        data.rename(columns={f'{year} [YR{year}]': f'{year}'}, inplace=True)

    selected_columns = ["Country","2017","2018","2019","2020","2021","2022"]
    filtered_data = data[selected_columns]
    df_cleaned = filtered_data.dropna(subset=['Country'])  
    df_cleaned = df_cleaned[~(df_cleaned.loc[:, "2017":"2022"].eq("..").all(axis=1))]  
    df_cleaned.replace("..", 0, inplace=True)

    melted_data = df_cleaned.melt(id_vars = ['Country'], 
                                value_vars = ["2017","2018","2019","2020","2021","2022"], 
                                var_name = 'Year', 
                                value_name = 'Stocks Traded'
                                )
    return melted_data


###### CURRENCY RATES ######
def currency_rates_data():
    data = pd.read_csv("data/CurrencyRates.csv", sep=',')
    # link to the dataset: https://databank.worldbank.org/reports.aspx?source=2&series=PA.NUS.FCRF&country=#
    data.rename(columns={"Country Name":"Country"}, inplace=True)

    years = ["2017","2018","2019","2020","2021","2022","2023"]
    for year in years:
        data.rename(columns={f'{year} [YR{year}]': f'{year}'}, inplace=True)

    selected_columns = ["Country","2017","2018","2019","2020","2021","2022","2023"]
    filtered_data = data[selected_columns]
    df_cleaned = filtered_data.dropna(subset=['Country'])  
    df_cleaned = df_cleaned[~(df_cleaned.loc[:, "2017":"2022"].eq("..").all(axis=1))]  
    df_cleaned.replace("..", 0, inplace=True)

    melted_data = df_cleaned.melt(id_vars = ['Country'], 
                                value_vars = ["2017","2018","2019","2020","2021","2022","2023"], 
                                var_name = 'Year', 
                                value_name = 'Currency Rates'
                                )
    
    melted_data['Currency Rates'] = pd.to_numeric(melted_data['Currency Rates'], errors='coerce').round(2)

    return melted_data

###### STOCK INDICES ######
def stock_indices_data():
    data_SP500 = pd.read_csv("data/Stock_SP_500.csv", sep=',')
    data_Russel_2000 = pd.read_csv("data/Stock_Russel_2000.csv", sep=',')
    data_OMX_Nordic40 = pd.read_csv("data/Stock_OMX_Nordic40.csv", sep=',')
    data_NYSE_Composite = pd.read_csv("data/Stock_NYSE_Comp.csv", sep=',')

    datasets_stocks = [
        (data_SP500, "SP 500"),
        (data_Russel_2000, "Russel 2000"),
        (data_OMX_Nordic40, "OMX Nordic 40"),
        (data_NYSE_Composite, "NYSE Composite"),
    ]

    data_stock = pd.DataFrame()

    for data, name in datasets_stocks:
        data['Date'] = pd.to_datetime(data['Date'])
        data['Year'] = data['Date'].dt.year

        data['Close/Last'] = pd.to_numeric(data['Close/Last'], errors='coerce')
        newdata = data.groupby('Year', as_index=False)['Close/Last'].mean(numeric_only=True)

        newdata.insert(0, 'Stock', name)
        data_stock = pd.concat([data_stock, newdata], axis=0, ignore_index=True)

    data_stock.rename(columns={'Close/Last':'Price(USD)'},inplace=True)
    return data_stock


def make_ctry_dropdown(s):
    if (s == "Stocks Traded"):
        df = stocks_traded_data()
        l = df["Country"].unique().tolist()
        return l
    
    elif (s == "Currency"):
       df = currency_rates_data()
       l = df["Country"].unique().tolist()
       return l
   

################################### WIDGETS #########################################

radio_main_category= dbc.RadioItems(
        id='main_category', 
        className='radio',
        options = [
           dict(label='Stocks Traded', value=0), 
           dict(label='Currency Rates', value=1), 
           dict(label='Stock Indices', value=2)
        ],
        value=0, 
        inline=True
    )

# drop_map = dcc.Dropdown(
#         id = 'drop_map',
#         clearable=False,
#         searchable=False, 
#         style= {
#            'margin': '4px', 
#            'box-shadow': '0px 0px #ebb36a', 
#            'border-color': '#ebb36a'
#         }        
#     )

# ctry_dropdown_stocks_traded = make_ctry_dropdown("Stocks Traded")
# ctry_dropdown_currency = make_ctry_dropdown("Currency")

ctry_dropdown_stocks_traded = dcc.Dropdown(id="stocks_traded_column", options = make_ctry_dropdown("Stocks Traded"), value = "France", clearable=False)
ctry_dropdown_currency = dcc.Dropdown(id="currency_column", options = make_ctry_dropdown("Currency"), value = "France", clearable=False)




################################### GRAPHS AND CHARTS #########################################

def stocks_traded_chart(ctry):
  data = stocks_traded_data()
  filtered_data = data[data["Country"] == ctry]
  fig = px.line(filtered_data, 
                x = 'Year',
                y = 'Stocks Traded',
                color = 'Country',
                title = f'Impact of Covid-19 on Stocks Traded in {ctry}',
                labels = {'Year': 'Year', 'Stocks Traded': 'Stocks Traded (in USD)'},
                markers = True)
  return fig


def currency_rates_chart(ctry):
  data = currency_rates_data()
  filtered_data = data[data["Country"] == ctry]
  fig = px.line(filtered_data, 
                x = 'Year',
                y = 'Currency Rates',
                color = 'Country',
                title = f'Impact of Covid-19 on Currency Rates in {ctry}',
                labels = {'Year': 'Year', 'Currency Rates': 'Currency Rates (as per USD)'},
                markers = True)
  return fig


def currency_rates_chart_overall():
  data = currency_rates_data()
  fig = px.line(data, 
                x = 'Year',
                y = 'Currency Rates',
                color = 'Country',
                title = 'Impact of Covid-19 on Currency Rates',
                labels = {'Year': 'Year', 'Currency Rates': 'Currency Rates (as per USD)'},
                markers = True)
  return fig


def stock_indices_chart():
  data = stock_indices_data()
  fig = px.line(data, 
                x = 'Year',
                y = 'Price(USD)',
                color = 'Stock',
                title = f'Impact of Covid-19 on Top Stock Indices',
                markers = True)
  return fig



################################### PAGE LAYOUT #########################################

# layout = html.Div(children=[

#     html.Div([
#        html.H2("Impact of Covid-19 on Stock Market and the Financial Sector", className="fw-bold text-center"),
#     ],className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    
#     html.Div([
#        html.Div([html.Label("Select Country"), ctry_dropdown_stocks_traded]),
#        html.Br(),
#        dcc.Graph(id="stocks_traded_graph"),
#     ],className='box', style={'width': '50%', 'float': 'left'}),

        
#     html.Div([
#        html.Div([html.Label("Select Country"), ctry_dropdown_currency]),
#        html.Br(),
#        dcc.Graph(id="currency_graph"),
#     ],className='box', style={'width': '50%', 'float': 'right'}),

#     html.Div([
#        html.Div([html.Label("Overall Currency Graph")]),
#        html.Br(),
#        dcc.Graph(id="currency_graph_overall",figure = currency_rates_chart_overall()),
#     ],className='box', style={'width': '100%'}),

#     html.Div([
#        html.Div([html.Label("Stock Indices Graph")]),
#        html.Br(),
#        dcc.Graph(id="stock_indices_graph",figure = stock_indices_chart()),
#     ],className='box', style={'width': '100%'}),
# ])

layout = html.Div(children=[
   
    html.Div([
       html.H2("Impact of Covid-19 on Stock Market and the Financial Sector", className="fw-bold text-center"),
       html.Br(),
       html.P(["Overall, these metrics are interconnected and significantly impact the global economy. The COVID-19 pandemic has reshaped market dynamics, investor behavior, and economic policies, leading to shifts in how these metrics are perceived and evaluated. As the world moves towards recovery, understanding these metrics will be crucial for navigating the post-pandemic economic landscape."], className='box_comment'),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         
    html.Div([
        html.Label("CHOOSE A METRIC TO KNOW MORE"), 
        html.Br(),
        html.Br(),
        radio_main_category,
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

    # Flexbox for the two graphs in the first row
    html.Div([
        html.Div([html.Label("Select Country"), ctry_dropdown_stocks_traded, html.Br(), dcc.Graph(id="stocks_traded_graph")],
                 className='box', style={'width': '33%'}),

       html.Div([
          html.P(id="comment",
              className='box_comment', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
              ),
       ],className='box', style={'width': '33%'}),
        
        html.Div([html.Label("Select Country"), ctry_dropdown_currency, html.Br(), dcc.Graph(id="currency_graph")],
                 className='box', style={'width': '33%'}),
    ], style={'display': 'flex', 'width': '100%'}),
    
    # Full-width graphs below
    html.Div([
       html.Div([html.Label("Overall Currency Graph")]),
       html.Br(),
       dcc.Graph(id="currency_graph_overall", figure=currency_rates_chart_overall()),
    ], className='box', style={'width': '100%'}),

    html.Div([
       html.Div([html.Label("Stock Indices Graph")]),
       html.Br(),
       dcc.Graph(id="stock_indices_graph", figure=stock_indices_chart()),
    ], className='box', style={'width': '100%'}),
])




################################### CALLBACKS #########################################

@callback(
    [
       Output("stocks_traded_graph", "figure"), 
       Output("comment", "children"), 
    ],
    [
        Input('main_category', 'value'),
        Input("stocks_traded_column", "value"),        
        Input("currency_column", "value"),
    ]
)

def update_graph_st(main_category, stocks_traded_column,currency_column):
    if main_category == 0:
        comment = '''
        Description: This metric refers to the volume and value of stocks that are bought and sold on various stock exchanges in different countries. It includes the number of shares traded and the overall market capitalization of publicly listed companies.<br>
        
        
        Impact on Global Economy:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Investment and Capital Flow: High trading volumes indicate investor confidence and attract foreign investments, which can lead to economic growth.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Market Stability: Fluctuations in stock trading can reflect economic stability or uncertainty. A declining market can lead to decreased consumer spending and business investment.<br>
        <br>
        Impact of COVID-19:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Volatility: The onset of the pandemic caused unprecedented market volatility, with stock markets experiencing significant drops due to uncertainty.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Sector Disparities: Different sectors reacted variably; for example, technology stocks surged while travel and hospitality stocks plummeted.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Stimulus Measures: Government stimulus packages influenced stock prices, as they reassured investors about economic recovery.
        '''

        return [
            stocks_traded_chart(stocks_traded_column),
            comment
            ]
    
    elif main_category == 1:
        comment = '''
        Description: Currency exchange rates represent the value of one currency in relation to another. These rates fluctuate based on various factors, including economic indicators, interest rates, and geopolitical events.
        Impact on Global Economy:
        Trade Balance: Exchange rates impact imports and exports. A weaker currency makes exports cheaper and imports more expensive, influencing trade balances.
        Inflation and Interest Rates: Currency depreciation can lead to inflation, prompting central banks to adjust interest rates, which can affect borrowing costs and economic growth.
        
        Impact of COVID-19:
        Increased Volatility: The pandemic led to increased volatility in currency markets, with many currencies experiencing sharp fluctuations.
        Policy Responses: Central banks' monetary policies (like lowering interest rates) and government interventions impacted currency values significantly.
        Safe-Haven Currencies: Currencies like the US dollar often strengthened as investors sought safety during market turmoil.        
        '''

        return [
            stocks_traded_chart(stocks_traded_column),
            comment
            ]
    
    elif main_category == 2:
        comment = '''
        Description: Stock indexes (like the S&P 500, FTSE 100, or Nikkei 225) are statistical measures that track the performance of a specific group of stocks, representing a portion of the stock market. They provide a snapshot of market trends and investor sentiment.
        Impact on Global Economy:
        Market Sentiment Indicator: Changes in stock indexes reflect investor sentiment and expectations about future economic performance.
        Pension Funds and Investments: Many pension funds and institutional investors track indexes, and significant changes can affect the financial health of these entities.
        
        Impact of COVID-19:
        Rapid Declines and Recoveries: Stock indexes saw steep declines at the start of the pandemic but later rebounded due to recovery optimism and stimulus measures.
        Sector Performance: COVID-19 influenced which stocks performed well (e.g., tech and healthcare) versus those that lagged (e.g., travel and hospitality).
        Long-Term Outlook: Investors began focusing on long-term economic recovery and shifts in consumer behavior, influencing index performance post-pandemic.    '''

        return [
            stock_indices_chart(),
            comment
            ]


@callback(Output("currency_graph", "figure"), 
          [Input("currency_column", "value")]
        )

def update_graph(currency_column):
    return currency_rates_chart(currency_column)





################################### PAGE LAYOUT #########################################

# layout = html.Div([
#     html.Div([
#         html.Div([
#             html.Div([
#                 html.Label("CHOOSE A METRIC TO KNOW MORE"), 
#                 html.Br(),
#                 html.Br(),
#                 radio_main_category
#             ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

#             html.Div([

#                 # First column 
#                 html.Div([
#                     html.Div([
#                        html.Label("TEST 123"), 
#                        html.Div([
#                           html.P(id='comment')
#                         ], className='box_comment', style={'padding-bottom': '15px'}),
#                    ],className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

#                     html.Div([
#                         html.Img(src='../assets/Inflation.png', style={'width': '100%', 'position': 'relative', 'opacity': '80%'})
#                     ])
#                 ], style={'width': '50%', 'float': 'left'}),

#                 # Second column 
#                 html.Div([
#                     html.Div([
#                         html.Label(id='choose_product', style={'margin': '10px'}),
#                         drop_map
#                     ], className='box'),
#                     html.Div([
#                         html.Label("TEST 123"), 
#                         # drop_map
#                     ], className='box'),
#                 ], style={'width': '50%', 'float': 'left'}),

#             ], className='row'),      

#         ], style={'width': '100%'}), # Adjusted width to fit full layout
        
#     ])
# ])



# ################################### CALLBACKS #########################################

# @callback(
#     [
#     #    Output('title_bar', 'children'),
#        Output('comment', 'children'),
#     ],
#     [
#        Input('main_category', 'value'),
#     ]
# )

# # Comment in the green box about the category
# def about_comment(value):
#     if value == 0:
#        comment = ["0"]
#     elif value == 1:
#        comment = ["1"]
#     elif value == 2:
#        comment = ["2"]
    
#     return comment


# @callback(
#     [
#        Output('choose_product', 'children')
#     ],
#     [
#        Input('main_category', 'value'),
#        Input('drop_map', 'value'),
#     ],
#     [State("drop_map","options")]
# )