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

dash.register_page(__name__, path='/stock_market', name="Stocks and Finances", order=2)




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


###### DROPDOWN CREATION ######
def make_ctry_dropdown(s):
    if (s == "Stocks Traded"):
        df = stocks_traded_data()
        l = df["Country"].unique().tolist()
        return l
    
    elif (s == "Currency"):
       df = currency_rates_data()
       l = df["Country"].unique().tolist()
       return l
   
    elif (s == "Stock"):
       df = stock_indices_data()
       l = df["Stock"].unique().tolist()
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

ctry_dropdown_stocks_traded = dcc.Dropdown(id="stocks_traded_column", options = make_ctry_dropdown("Stocks Traded"), value = "France", clearable=False)
ctry_dropdown_currency = dcc.Dropdown(id="currency_column", options = make_ctry_dropdown("Currency"), value = "France", clearable=False)
ctry_dropdown_stock = dcc.Dropdown(id="stock_column", options = make_ctry_dropdown("Stock"), value = "SP 500", clearable=False)






################################### GRAPHS AND CHARTS #########################################


def stocks_traded_chart(ctry):
  data = stocks_traded_data()
  if ctry == "Overall":
    filtered_data = data
  else:
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
    if ctry == "Overall":
        filtered_data = data
    else:
        filtered_data = data[data["Country"] == ctry]
  
    fig = px.line(filtered_data, 
                x = 'Year',
                y = 'Currency Rates',
                color = 'Country',
                title = f'Impact of Covid-19 on Currency Rates in {ctry}',
                labels = {'Year': 'Year', 'Currency Rates': 'Currency Rates (as per USD)'},
                markers = True)
    return fig


def stock_indices_chart(stock):
    data = stock_indices_data()
    if stock == "Overall":
        filtered_data = data
    else:
        filtered_data = data[data["Stock"] == stock]
    
    fig = px.line(filtered_data, 
        x = 'Year',
        y = 'Price(USD)',
        color = 'Stock',
        title = f'Impact of Covid-19 on {stock}',
        markers = True)
    
    return fig





################################### PAGE LAYOUT #########################################


layout = html.Div(children=[

    # HEADING
    html.Div([
       html.H1("Impact of Covid-19 on Stock Market and the Financial Sector", className="fw-bold text-center"),
       html.Br(),
       html.P("Overall, these metrics are interconnected and significantly impact the global economy. The COVID-19 pandemic has reshaped market dynamics, investor behavior, and economic policies, leading to shifts in how these metrics are perceived and evaluated. As the world moves towards recovery, understanding these metrics will be crucial for navigating the post-pandemic economic landscape."),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         

    # RADIO BUTTONS TO SELECT THE METRIC
    html.Div([
        html.Label("CHOOSE A METRIC TO KNOW MORE"), 
        html.Br(),
        html.Br(),
        radio_main_category,
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),


    # FIRST ROW FLEXBOX CONTAINERS
    html.Div([

        html.Div([
            html.Br(),
            html.Br(),
            dcc.Dropdown(id="opt_dropdown", placeholder="Choose an option: "), 
            html.Br(), 
            dcc.Graph(id="indiv_cat_graph")],
        className='box', style={'width': '33%'}),

        html.Div([
          html.Div(id="comment1"),
       ],className='box', style={'width': '33%'}),

        html.Div([
            html.Br(),
            html.Label("Overall Chart"),
            html.Br(), 
            html.Br(), 
            dcc.Graph(id="overall_graph")],
        className='box', style={'width': '33%'}),
        
    ], style={'display': 'flex', 'width': '100%'}),

    # SECOND ROW TEXT CONTAINER
    html.Div(id = "comment2" ,className='box', style={'width': '100%'}),

])
    




################################### CALLBACKS #########################################

# @callback(
#     [
#        Output("opt_dropdown","children"),
#        Output("comment", "children"), 
#        Output("indiv_cat_graph", "figure"), 
#        Output("overall_graph", "figure"), 
#     ],
#     [
#         Input('main_category', 'value'),
#         Input("stocks_traded_column", "value"),        
#         Input("currency_column", "value"),
#         Input("stock_column", "value"),
#     ]
# )


# def update_graph_st(main_category, stocks_traded_column, currency_column, stock_column):
#     if main_category == 0:
        
#         comment = '''
#         Description: This metric refers to the volume and value of stocks that are bought and sold on various stock exchanges in different countries. It includes the number of shares traded and the overall market capitalization of publicly listed companies.<br>
        
        
#         Impact on Global Economy:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;Investment and Capital Flow: High trading volumes indicate investor confidence and attract foreign investments, which can lead to economic growth.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;
#         <br>
#         Impact of COVID-19:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;
#         &nbsp;&nbsp;&nbsp;&nbsp;
#         &nbsp;&nbsp;&nbsp;&nbsp;Stimulus Measures: Government stimulus packages influenced stock prices, as they reassured investors about economic recovery.
#         '''
        
#         opt_dropdown = ctry_dropdown_stocks_traded

#         return [
#             opt_dropdown,
#             stocks_traded_chart(stocks_traded_column),
#             comment,
#             stocks_traded_chart("Overall"),
#             ]
    

#     elif main_category == 1:
#         comment = '''
#         Description: Currency exchange rates represent the value of one currency in relation to another. These rates fluctuate based on various factors, including economic indicators, interest rates, and geopolitical events.
#         Impact on Global Economy:
#         Trade Balance: Exchange rates impact imports and exports. A weaker currency makes exports cheaper and imports more expensive, influencing trade balances.
#         Inflation and Interest Rates: Currency depreciation can lead to inflation, prompting central banks to adjust interest rates, which can affect borrowing costs and economic growth.
        
#         Impact of COVID-19:
#         Increased Volatility: The pandemic led to increased volatility in currency markets, with many currencies experiencing sharp fluctuations.
#         Policy Responses: Central banks' monetary policies (like lowering interest rates) and government interventions impacted currency values significantly.
#         Safe-Haven Currencies: Currencies like the US dollar often strengthened as investors sought safety during market turmoil.        
#         '''

#         opt_dropdown = ctry_dropdown_currency

#         return [
#             opt_dropdown,
#             currency_rates_chart(currency_column),
#             comment,
#             currency_rates_chart("Overall"),
#             ]
    

#     elif main_category == 2:
#         comment = '''
#         Description: Stock indexes (like the S&P 500, FTSE 100, or Nikkei 225) are statistical measures that track the performance of a specific group of stocks, representing a portion of the stock market. They provide a snapshot of market trends and investor sentiment.
#         Impact on Global Economy:
#         Market Sentiment Indicator: Changes in stock indexes reflect investor sentiment and expectations about future economic performance.
#         Pension Funds and Investments: Many pension funds and institutional investors track indexes, and significant changes can affect the financial health of these entities.
        
#         Impact of COVID-19:
#         Rapid Declines and Recoveries: Stock indexes saw steep declines at the start of the pandemic but later rebounded due to recovery optimism and stimulus measures.
#         Sector Performance: COVID-19 influenced which stocks performed well (e.g., tech and healthcare) versus those that lagged (e.g., travel and hospitality).
#         Long-Term Outlook: Investors began focusing on long-term economic recovery and shifts in consumer behavior, influencing index performance post-pandemic.    '''

#         opt_dropdown = ctry_dropdown_stock

#         return [
#             opt_dropdown,
#             stock_indices_chart(stock_column),
#             comment,
#             stock_indices_chart("Overall"),
#             ]


@callback(
    [
        Output("opt_dropdown", "options"),
        Output("comment1", "children"),
        Output("indiv_cat_graph", "figure"),
        Output("overall_graph", "figure"),
        Output("comment2", "children"),
    ],
    [
        Input("main_category", "value"),
        Input("opt_dropdown", "value")
    ]
)

def update_graph_st(main_category, opt_dropdown_value):

    if main_category == 0:
        comment1 = html.Div([
            html.P("Stocks traded data refers to the number or volume of shares traded on a country’s stock exchanges over a given period. This data can indicate how active a market is, how accessible it is to investors, and the liquidity available for shares within that country.",
                   className='box_comment fs-5 text-center', 
                   style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
                   ),
            html.Br(),
            html.P("High trading volumes in major economies can indicate investor confidence, economic growth, or market accessibility, which can attract foreign investments. Alternatively, significant declines in trading volumes or sharp fluctuations often suggest economic instability, which can ripple through the global economy by affecting currency exchange rates, commodity prices, and international trade.",
                   className='box_comment fs-5 text-center', 
                   style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
                ),
        ])

        comment2 = html.Div([
                
                html.Br(),

                html.Div([
                    html.Div([
                        html.P("During COVID-19, many countries saw unprecedented levels of stock trading activity due to volatility, uncertainty, and government intervention. Panic selling at the pandemic's onset was followed by increased buying as markets rebounded, leading to some of the highest trading volumes ever recorded."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-4"),

                html.Div([
                    html.Br(),
                    html.P("Trading Volume in U.S. (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("15.63 billion shares", className="fw-bold text-info display-5 text-center"),  
                    html.P("(2019 average - 7 billion shares/day)", className="fs-5 text-center"),  
                ], className="col-md-4"),

                html.Div([
                    html.Div([
                        html.P("Global trading volumes rose by around 30% in the first quarter of 2020 compared to the same period in 2019, driven by sharp movements as investors reacted to COVID-19's evolving economic impact."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-4"),

        ], className='row mb-5')
        
        options = [{'label': country, 'value': country} for country in make_ctry_dropdown("Stocks Traded")]
        fig = stocks_traded_chart(opt_dropdown_value)
        overall_fig = stocks_traded_chart("Overall")


    elif main_category == 1:
        comment1 = html.Div([
            html.P("The currency exchange rate is the value of one currency relative to another. Exchange rates fluctuate due to factors such as interest rates, inflation, political stability, and economic performance.",
                   className='box_comment fs-5 text-center', 
                   style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
                   ),
            html.Br(),
            html.P("Exchange rates influence international trade competitiveness, affecting exports and imports. For example, a strong currency can make a country’s exports more expensive and imports cheaper, impacting its trade balance. Exchange rate fluctuations also impact multinational corporations, commodity prices (like oil and gold), inflation, and the attractiveness of investments in different countries. Sudden shifts can lead to financial instability or even currency crises, impacting global economic stability.",
                   className='box_comment fs-5 text-center', 
                   style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
                   ),
        ])

        comment2 = html.Div([
                
                html.Br(),

                html.Div([
                    html.Div([
                        html.P("The pandemic led to significant currency fluctuations due to investor uncertainty, shifting risk appetites, and central banks' interventions. Currencies of emerging markets depreciated sharply against the U.S. dollar, while the dollar initially strengthened as a safe haven before stabilizing."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-4"),

                html.Div([
                    html.Br(),
                    html.P("Trading Volume in U.S. (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("15.63 billion shares", className="fw-bold text-info display-5 text-center"),  
                    html.P("(Measured against the U.S. dollar)", className="fs-5 text-center"),  
                ], className="col-md-4"),

                html.Div([
                    html.Br(),
                    html.P("Brazilian Real (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("↓ 29% ", className="fw-bold text-info display-5 text-center"),  
                    html.P("(2019 average - 7 billion shares/day)", className="fs-5 text-center"),  
                ], className="col-md-4"),

                html.Div([
                    html.Div([
                        html.P("Brazil's drop was attributed to economic instability, political uncertainty, and a struggling healthcare system during the pandemic. Even the South African rand fell nearly 25% against the dollar in March 2020 as investors pulled funds from emerging markets. South Africa’s reliance on global demand for minerals compounded the problem as commodity prices plunged."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-6"),

                html.Div([
                    html.Div([
                        html.P("Emerging market currencies depreciated an average of 13-15% in the first half of 2020, according to the International Monetary Fund (IMF), while safe-haven currencies like the U.S. dollar and Swiss franc saw temporary strength. The Federal Reserve's rate cuts in March 2020 also helped ease the dollar's rise, stabilizing the global currency markets."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-6"),

        ], className='row mb-5')

        options = [{'label': country, 'value': country} for country in make_ctry_dropdown("Currency")]
        fig = currency_rates_chart(opt_dropdown_value)
        overall_fig = currency_rates_chart("Overall")


    else:
        comment1 = html.Div([
            html.Div([
                html.P("S&P 500: Tracks the performance of 500 large-cap U.S. companies and is seen as a barometer for the U.S. economy."),
                html.P("Russell 2000: Measures the performance of 2,000 small-cap U.S. companies and gives insights into the health of the smaller, often growth-oriented segment of the economy."),
                html.P("NYSE Composite: Includes all stocks listed on the New York Stock Exchange and reflects the overall performance of the NYSE."),
                html.P("OMX Nordic 40: Tracks the 40 most actively traded stocks on the Nordic stock exchanges (Denmark, Finland, Iceland, and Sweden)."),
            ],className='box_comment fs-5 text-center', 
            style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
            ),
            html.Br(),
            html.P("Stock indexes represent the economic health and investor confidence in a region or sector. For example, if the S&P 500 is doing well, it generally indicates that the U.S. economy is strong, which positively affects global markets as the U.S. is a major trading partner and financial hub. Conversely, downturns in these indexes can lead to a loss of investor confidence, reduced consumer spending, and lowered corporate earnings, which can all dampen global economic activity. Indexes like OMX Nordic 40 help gauge the economic stability of specific regions and can signal growth or risks in those markets, affecting investor sentiment and international investments in those areas.",
                   className='box_comment fs-5 text-center', 
                   style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
                   ),
        ])

        comment2 = html.Div([
                
                html.Br(),

                html.Div([
                    html.Br(),
                    html.P("Italy’s FTSE MIB (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("↓ 17%", className="fw-bold text-info display-5 text-center"),  
                    html.P("(The index ended 2020 down approximately 5.4%)", className="fs-5 text-center"),  
                ], className="col-md-3"),


                html.Div([
                    html.Br(),
                    html.P("BSE Sensex (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("↓ 38%", className="fw-bold text-info display-5 text-center"),  
                    html.P("(Economic toll of India’s strict lockdown and disruptions in the informal sector)", className="fs-5 text-center"),  
                ], className="col-md-3"),

                html.Div([
                    html.Br(),
                    html.P("China's CSI 300 (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("↑ 27% ", className="fw-bold text-info display-5 text-center"),  
                    html.P("(Rapid containment of the virus and government stimulus measures supported their economy)", className="fs-5 text-center"),  
                ], className="col-md-3"),

                html.Div([
                    html.Br(),
                    html.P("NASDAQ-100 Closing (2020)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("47%", className="fw-bold text-info display-5 text-center"),  
                    html.P("(Major MNCs saw increased demand due to remote work and e-commerce growth)", className="fs-5 text-center"),  
                ], className="col-md-3"),

                html.Div([
                    html.Div([
                        html.P("COVID-19 triggered massive volatility across stock indexes worldwide. Initial sharp declines in March 2020 were followed by recoveries, especially in technology-heavy and healthcare stocks that benefited from digitalization trends during the pandemic."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-6"),

                html.Div([
                    html.Div([
                        html.P("Global trading volumes rose by around 30% in the first quarter of 2020 compared to the same period in 2019, driven by sharp movements as investors reacted to COVID-19's evolving economic impact."),
                                ],className='box_comment fs-5 text-center'),
                ], className="col-md-6"),

        ], className='row mb-5')

        options = [{'label': stock, 'value': stock} for stock in make_ctry_dropdown("Stock")]
        fig = stock_indices_chart(opt_dropdown_value)
        overall_fig = stock_indices_chart("Overall")

    return options, comment1, fig, overall_fig, comment2
