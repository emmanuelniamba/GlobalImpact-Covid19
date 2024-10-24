# '''
# 4. Inflation and Prices
# Page Name: "Inflation & Prices"

# Purpose: Explore inflation rates during COVID-19, especially the effects of supply chain disruptions.
# Content:
# Comparison of inflation rates across countries.
# Impact of COVID-19 on essential commodities and services.
# Discussion of supply chain challenges and price fluctuations.
# Visualizations:
# Line chart: Inflation rate trends over time.
# Heatmap: Correlation between inflation and other variables (unemployment, trade).
# Bubble chart: Inflation vs. GDP growth vs. population.
# '''


import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go


dash.register_page(__name__, path='/inflation', name="Inflation and Prices", order=3)



################################### DATA #########################################

###### CONSUMER PRICES ######
def consumer_prices_data():
    data = pd.read_csv("data/consumer_prices.csv", sep=',')
    # link to the dataset: https://unctadstat.unctad.org/datacentre/dataviewer/US.Cpi_A

    '''
    1. Consumer Price Index (CPI):
    Definition: The CPI is an economic indicator that measures the average change over time in the prices paid by consumers for a basket of goods and services. It reflects the cost of living and is commonly used to gauge inflation.
    Base Year (2010 in this case): The base year is the reference point against which price changes are measured. In your case, the year 2010 has a CPI value of 100, meaning the index starts from that point. Prices in subsequent years are compared to this baseline.

    Example: A CPI of 110 in 2024 means that the average price of the goods and services in the basket has increased by 10% compared to their prices in 2010.

    Significance: CPI helps track how much prices have increased or decreased relative to the base year, allowing economists, policymakers, and businesses to understand inflationary trends and the purchasing power of consumers.
    '''

    data.rename(columns={"Economy_Label":"Country"}, inplace=True)

    years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]
    for year in years:
        data.rename(columns={f'{year}_Index_Base_2010_Value': f'{year}'}, inplace=True)

    selected_columns = ["Country","2017","2018","2019","2020","2021","2022"]
    filtered_data = data[selected_columns]

    melted_data = filtered_data.melt(id_vars = ['Country'], 
                            value_vars = ["2017","2018","2019","2020","2021","2022"], 
                            var_name = 'Year', 
                            value_name = 'Consumer Price'
                        )

    for i in range(0,len(melted_data["Country"])):
        n = melted_data["Country"][i].split(" ")
        if len(n) >= 3:
            melted_data.loc[i,"Country"] = f"{n[0]} {n[1]} {n[2]}"

    return melted_data



###### COMMODITY PRICES ######
def commodity_prices_data():
    data_commodity = pd.read_csv("data/CommodityPrices.csv", sep=',')
    # link: https://unctadstat.unctad.org/datacentre/dataviewer/US.CommodityPrice_A

    data_commodity.rename(columns={"Commodity_Label":"Commodity"}, inplace=True)

    years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]

    for year in years:
        data_commodity.rename(columns={f"{year}_Prices_Value": f'{year}'}, inplace=True)
    
    items = []
    for i in range(0, len(data_commodity["Commodity"])): 
        name = data_commodity["Commodity"][i].split(",")

        if name[0] in items:
            data_commodity.loc[i,"Commodity"] = f"{name[0]} ({name[1].strip()})"
        else:
            items.append(name[0])
            data_commodity.loc[i,"Commodity"] = f"{name[0]}"
    
    commodity_list = list(data_commodity["Commodity"])

    pre_covid_years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"]
    post_covid_years = ["2022","2023"]

    # data_commodity['Pre_Covid'] = data_commodity[pre_covid_years].apply(pd.to_numeric, errors = 'coerce').mean(axis=1)
    # data_commodity['Post_Covid'] = data_commodity[post_covid_years].apply(pd.to_numeric, errors = 'coerce').mean(axis=1)

    selected_columns_commodity = ["Commodity","2017","2018","2019","2020","2021","2022","2023"]
    filtered_data_commodity = data_commodity[selected_columns_commodity]

    melted_data_commodity = filtered_data_commodity.melt(id_vars = ['Commodity'], 
                            value_vars = ["2017","2018","2019","2020","2021","2022","2023"], 
                            var_name = 'Year', 
                            value_name = 'Commodity Price'
                        )
    
    return melted_data_commodity


def make_dropdown(s):
    if (s == "Consumer"):
        df = consumer_prices_data()
        l = df["Country"].unique().tolist()
        l.append("Overall")
        return l
    
    elif (s == "Commodity"):
       df = commodity_prices_data()
       l = df["Commodity"].unique().tolist()
       l.append("Overall")
       return l
   




################################### GRAPHS AND CHARTS #########################################

def consumer_price_chart(ctry):
    df = consumer_prices_data()
    if ctry == "Overall":
        filtered_df = df
    else:
        filtered_df = df[df["Country"] == ctry]
        
    fig = px.line(filtered_df, 
                x = 'Year',
                y = 'Consumer Price',
                color = 'Country',
                title = f'Impact of Covid-19 on Consumer Price in {ctry}',
                labels = {'Year': 'Year', 'Consumer Price': 'Consumer Price (Index Base 10)'},
                markers = True)
    
    return fig


def commodity_price_chart(comm):
    df = commodity_prices_data()
    if comm == "Overall":
        filtered_data = df
    else:
        filtered_data = df[df["Commodity"] == comm]
    
    fig = px.line(filtered_data, 
                x = 'Year',
                y = 'Commodity Price',
                color = 'Commodity',
                title = f'Impact of Covid-19 on the Price of {comm}',
                labels = {'Year': 'Phase', 'Commodity Price': 'Price of Commodity'},
                markers = True)
    
    return fig




######################################### WIDGETS #########################################


dropdown_countries = dcc.Dropdown(id="ctry_cpi_name_col", options = make_dropdown("Consumer"), value = "France", clearable=False)
dropdown_commodities = dcc.Dropdown(id="commodity_name_col", options = make_dropdown("Commodity"), value = "Bananas", clearable=False)




################################### PAGE LAYOUT #########################################


layout = html.Div(children=[
   
    html.Div([
       html.H2("Impact of Covid-19 on Inflation and Prices", className="fw-bold text-center"),
       html.Br(),
       html.P(["Overall, these metrics are interconnected and significantly impact the global economy. The COVID-19 pandemic has reshaped market dynamics, investor behavior, and economic policies, leading to shifts in how these metrics are perceived and evaluated. As the world moves towards recovery, understanding these metrics will be crucial for navigating the post-pandemic economic landscape."]),
    ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
         

    html.Div([
        
        # Text box - Row 1 Left

        html.Div([

            html.Div([
                html.Br(),
                html.Div([
                    html.P("Before the pandemic, consumer prices globally remained relatively stable, with annual inflation hovering around 2-3% in most developed economies.", className='box_comment fs-5'),
                ], className="col-md-4"),

                html.Div([
                    html.P("Global Inflation (2019)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("2.5%", className="fw-bold text-info display-4 text-center"),  # Large key figure
                ], className="col-md-4"),

                html.Div([
                    html.P("Regions like the EU and U.S. had consistent inflation rates below 2%.", className='box_comment fs-5'),
                ], className="col-md-4"),

            ], className='row mb-5'),

            
            html.Div([
                html.Br(),

                html.Div([
                    html.P("U.S. Inflation Peak in 2022", className="fw-bold text-primary fs-4 text-center"),
                    html.P("9.1%", className="fw-bold text-danger display-4 text-center"),  
                ], className="col-md-4"),

                html.Div([
                    # html.H4("Pandemic-Induced Price Surge", className="fw-bold text-primary"),
                    html.P("As the pandemic unfolded, countries faced disruptions in production, labor, and supply chains. Consumer prices began to rise sharply across the globe, particularly for essentials like food, healthcare, and energy.", className='box_comment fs-5'),
                ], className="col-md-4"),

                html.Div([
                    html.P("U.K. Inflation", className="fw-bold text-primary fs-4 text-center"),
                    html.P("10.1%", className="fw-bold text-info display-4 text-center"), 
                ], className="col-md-4"),
                
            ], className='row mb-5'),


            html.Div([
                html.Div([
                    html.Div([
                        html.H4("Food Prices", className="fw-bold text-center"),
                        html.P("Global food prices saw a sharp increase, especially in countries relying on imports.")
                    ], className="box_comment fs-6 text-center"),
                    html.P("Food price rise in Africa: '30%'", className="fw-bold text-info fs-4 text-center"),
                ], className="col-md-4"),

                html.Div([
                    html.Div([
                        html.H4("Energy Prices", className="fw-bold text-center"),
                        html.P("Energy prices skyrocketed, with oil prices rebounding sharply after an initial drop.")
                    ], className="box_comment fs-6 text-center"),
                    html.P("Gas prices up '45%' in Europe", className="fw-bold text-danger fs-4 text-center"),
                ], className="col-md-4"),

                html.Div([
                    html.Div([
                        html.H4("Healthcare Costs", className="fw-bold text-center"),
                        html.P("Healthcare costs surged as demand for medical supplies increased during the pandemic.")
                    ], className="box_comment fs-6 text-center"),
                    html.P("Healthcare inflation in the U.S.: **5.6%**", className="fw-bold text-warning fs-4 text-center"),
                ], className="col-md-4"),
            ], className="row mb-5"),


            html.Div([
                html.P("By 2023, global consumer prices began to stabilize as supply chains recovered. However, in many regions, inflation persisted due to lingering energy crises, geopolitical tensions, and wage increases. Countries like Argentina continued to experience high inflation rates (above 80%), while developed economies started seeing a slow moderation in inflation.", 
                    className='box_comment fs-5 text-center'),
                ], className="col-md-12 p-4 mb-5"),
            
            ], className='box', style={'width': '50%'}),

        # Graph box - Row 1 Right
        html.Div([
            html.H3("Consumer Prices"),
            html.P("Tracks change in prices (relative to the base year) to understand inflationary trends and the purchasing power of consumers"),
            html.Br(),
            html.Label("Select Country"), 
            dropdown_countries, 
            html.Br(), 
            dcc.Graph(id="consumer_graph"),

            html.Br(),
            html.Br(),
            html.Br(),

            html.Div([
                html.Br(),
                html.Div([
                    html.P("U.S. Inflation (mid-2023)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("4.9%", className="fw-bold text-info display-4 text-center"), 
                    html.P("Moderated", className="fw-bold text-primary fs-4 text-center"),
                ], className="col-md-4"),

                html.Div([
                    html.P("Argentina inflation in 2023", className="fw-bold text-primary fs-4 text-center"),
                    html.P("82.4%", className="fw-bold text-danger display-4 text-center"),  
                ], className="col-md-4"),

                html.Div([
                    html.P("EU Inflation (end-2023)", className="fw-bold text-primary fs-4 text-center"),
                    html.P("5.5%", className="fw-bold text-info display-4 text-center"), 
                    html.P("Stabilised", className="fw-bold text-primary fs-4 text-center"),
                ], className="col-md-4"),
            
            ], className='row'),

        ],className='box', style={'width': '50%'}),

    ], style={'display': 'flex', 'width': '100%'}),


    # Flexbox for the two graphs in the second row
    html.Div([
        html.Div([
            html.H3("Commodity Prices"),
            html.P("Shows the fluctuating values of major commodities over the years"),
            html.Br(),
            html.Label("Select Commodity"), 
            dropdown_commodities, 
            html.Br(), 
            dcc.Graph(id="commodity_graph")
            ],className='box', style={'width': '50%'}),

    #     html.Div([
    #         html.P("At the onset of the pandemic, there was a sharp drop in consumer demand as lockdowns and social distancing measures were imposed. This led to a deflationary environment in some sectors (e.g., travel, hospitality). Oil prices dropped significantly, reducing inflationary pressure in energy-dependent sectors.", 
    #                className='box_comment', 
    #                style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
    #                ),
    #         html.P("As the pandemic progressed, global supply chains were severely disrupted due to factory closures, transportation bottlenecks, and labor shortages. This led to scarcity of goods, pushing prices upward. Governments worldwide implemented large fiscal stimulus packages to prevent economic collapse. Central banks cut interest rates and engaged in quantitative easing, increasing money supply, which started driving inflation upwards.",
    #                className='box_comment', 
    #                style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
    #                ),
    #         html.P("As economies reopened, there was a surge in demand for goods and services, especially as consumers released pent-up savings. However, supply chains had not fully recovered, leading to a significant mismatch between supply and demand. Energy prices, particularly oil and gas, soared due to supply constraints, further contributing to inflation. Central banks initially viewed the inflation as 'transitory', expecting it to ease once supply chains normalized. However, it persisted longer than expected.",
    #                className='box_comment', 
    #                style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
    #                ),
    #         html.P("Many countries, especially in the U.S., Europe, and some emerging markets, experienced inflation reaching multi-decade highs. Key drivers included labor shortages, rising energy prices, and continued supply chain disruptions. Central banks began tightening monetary policies by raising interest rates to curb inflation. For example, the Federal Reserve and European Central Bank increased rates, which eventually started slowing inflation.",
    #                className='box_comment', 
    #                style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
    #                ),
    #         html.P("By late 2023 and into 2024, inflation rates began to moderate in many countries as supply chains improved, energy prices stabilized, and the effects of higher interest rates curtailed demand. However, inflation levels in some regions remained elevated due to structural issues like wage increases or geopolitical tensions (e.g., energy supply disruptions from conflicts).", 
    #                className='box_comment', 
    #                style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}
    #                ),
    #         html.P(id="comment_commodity", className='box_comment', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    #    ],className='box', style={'width': '50%'}),
    html.Div([
        html.H3("COVID-19's Economic Impact: Inflation and Supply Chain", className="fw-bold text-center mb-4"),

        # First Section: Key Figures and Stats (in 1 column)
        html.Div([
            html.Div([
                html.P("Global Inflation Rate Surge:", className="fw-bold text-primary fs-4 text-center"),
                html.P("12%", className="fw-bold text-danger display-4 text-center"),  # Large key figure
            ], className="col"),

            html.Div([
                html.P("Fiscal Stimulus by Countries (2020-2022):", className="fw-bold text-primary fs-4 text-center"),
                html.P("$16 Trillion", className="fw-bold text-success display-4 text-center"),  # Large key figure
            ], className="col"),

            html.Div([
                html.P("Oil Price Drop in 2020:", className="fw-bold text-primary fs-4 text-center"),
                html.P("↓ 65%", className="fw-bold text-info display-4 text-center"),  # Large key figure
            ], className="col"),
        ], className='row mb-5'),

        html.Hr(),  # Section separator

        # Second Section: Two Columns with Text
        html.Div([

            # Column 1 (Left)
            html.Div([
                html.H4("Initial Impact on Prices", className="fw-bold text-primary"),
                html.P("At the onset of the pandemic, sectors like travel and hospitality saw a deflationary trend. Oil prices dropped significantly, reducing inflation in energy-dependent sectors.",
                    className='box_comment fs-5'),  # Smaller text
                html.P("↓ Oil prices dropped by **65%** in 2020", className='fw-bold text-danger fs-6'),  # Bold and colored
                html.P("This provided temporary relief to the inflationary pressure.",
                    className='box_comment fs-5'),  # Slightly smaller text for details
            ], className="col-md-6"),

            # Column 2 (Right)
            html.Div([
                html.H4("Global Supply Chain Disruptions", className="fw-bold text-primary"),
                html.P("Disruptions due to factory closures and labor shortages led to **scarcity** of goods, pushing prices up. Transportation bottlenecks further aggravated the situation.",
                    className='box_comment fs-5'),
                html.P("Governments responded with fiscal stimulus of **$16 trillion** to avoid economic collapse.", 
                    className='fw-bold text-success fs-5'),
                html.P("Meanwhile, central banks engaged in **quantitative easing**.", 
                    className='box_comment fs-6 text-warning'),  # Highlighting with color
            ], className="col-md-6")
        ], className='row mb-5'),

        html.Hr(),  # Section separator

        # Third Section: Three Columns with Key Highlights
        html.Div([
            html.Div([
                html.H4("Labor Shortages", className="fw-bold text-center"),
                html.P("Severe labor shortages due to pandemic-induced lockdowns contributed to supply chain issues.",
                    className="box_comment fs-6 text-center"),
                html.P("Wages rose by **10%**", className="fw-bold text-info fs-4 text-center"),
            ], className="col-md-4"),

            html.Div([
                html.H4("Energy Prices", className="fw-bold text-center"),
                html.P("Energy prices soared, particularly oil and gas, contributing heavily to inflation.",
                    className="box_comment fs-6 text-center"),
                html.P("Gas prices up **45%**", className="fw-bold text-danger fs-4 text-center"),
            ], className="col-md-4"),

            html.Div([
                html.H4("Monetary Policies", className="fw-bold text-center"),
                html.P("Central banks began tightening policies. Interest rates increased by the Federal Reserve, slowing inflation growth.",
                    className="box_comment fs-6 text-center"),
                html.P("Interest rate hikes **3x**", className="fw-bold text-warning fs-4 text-center"),
            ], className="col-md-4"),
        ], className="row mb-5"),

        html.Hr(),  # Section separator

        # Fourth Section: Full-width text block with important narrative
        html.Div([
            html.H4("Moderation of Inflation (2023-2024)", className="fw-bold text-primary text-center"),
            html.P("By late 2023 and into 2024, inflation rates began to moderate in many countries as supply chains improved and energy prices stabilized. However, some regions experienced elevated inflation due to structural issues like wage increases or geopolitical tensions (e.g., conflicts affecting energy supply).", 
                className='box_comment fs-5 text-center'),
        ], className="col-md-12 p-4 mb-5"),

        # Final Section: Three-column layout with smaller detailed insights
        html.Div([
            html.Div([
                html.P("Energy prices stabilized.", className="box_comment fs-6 text-center"),
            ], className="col-md-4"),

            html.Div([
                html.P("Supply chains started recovering.", className="box_comment fs-6 text-center"),
            ], className="col-md-4"),

            html.Div([
                html.P("Monetary policy adjustments helped curb inflation.", className="box_comment fs-6 text-center"),
            ], className="col-md-4"),
        ], className="row")
    ], className='container-fluid'),


    ], style={'display': 'flex', 'width': '100%'}),
    

    # # Full-width graphs below
    # html.Div([
    #    html.Div([html.Label("Overall Currency Graph")]),
    #    html.Br(),
    #    dcc.Graph(id="currency_graph_overall", figure=currency_rates_chart_overall()),
    # ], className='box', style={'width': '100%'}),

    # html.Div([
    #    html.Div([html.Label("Stock Indices Graph")]),
    #    html.Br(),
    #    dcc.Graph(id="stock_indices_graph", figure=stock_indices_chart()),
    # ], className='box', style={'width': '100%'}),
])





################################### CALLBACKS #########################################


@callback(Output("consumer_graph", "figure"),
        Input('ctry_cpi_name_col', 'value'))

def update_graph_consumer(ctry_cpi_name_col):
    return consumer_price_chart(ctry_cpi_name_col)


@callback(Output("ommodity_graph", "figure"),
        Input('commodity_name_col', 'value'))

def update_graph_commodity(commodity_name_col):
    return commodity_price_chart(commodity_name_col)
