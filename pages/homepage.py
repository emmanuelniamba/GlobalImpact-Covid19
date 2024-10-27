import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/', name="Homepage", order=0)





####################### DATA #############################

df = pd.read_csv("data/hdi_data_map.csv")
df = df.rename(columns={'Entity':'Country','Human Development Index':'HDI'})
df = df[df["Year"].isin([2016, 2017, 2018, 2019, 2020, 2021, 2022])]





####################### PAGE LAYOUT #############################

layout = html.Div(children=[
    
    html.Br(),
    html.H1("COVID-19 Global Economic Impact Dashboard", className="fw-bold text-center",style={'fontSize': '3rem'}),
    html.Div(children=[
        html.P("Welcome to the COVID-19 Global Economic Impact Dashboard, an interactive platform designed to reveal the economic shifts during the pandemic. Explore data-driven insights into GDP, unemployment, inflation, and trade, discovering the lasting effects of COVID-19 on the global economy.", className='p-3 text-muted text-center'),
    ], style={'background-color': '#ffffff', 'border-radius': '10px', 'margin': '10px', 'padding': '15px', 'width': '100%'}),

    html.Div([
        html.Div([
            html.H3("Key Indicators at a Glance", style={'font-weight': 'bold'}),
            html.Br(),
            html.Div([
                html.P("GDP Decline: Visualize GDP trends and identify regions most affected, analyzing both immediate impacts and the journey toward recovery."),
                html.P("Unemployment Rates: Discover changes in employment across sectors, especially in areas like tourism and manufacturing."),
                html.P("Inflation Trends**: Understand how inflation fluctuated, affecting essential goods and services during the pandemic."),
            ],className='p-2 text-muted'),
        ], className='box', style={'background-color': '#f1f9ff', 'padding': '20px', 'border-radius': '10px', 'width': '50%'}),

        html.Div([
            html.H3("Explore data-driven stories and visuals", style={'font-weight': 'bold'}),
            html.Br(),
            html.Div([
                html.P("Global Heatmap: Identify the regions hardest hit by GDP declines and employment changes."),
                html.P("Economic Trends: Track global trends in GDP, stock markets, and unemployment to understand the resilience and recovery journey of the world economy."),
                html.P("Country-Wise Analysis: Understand how each country was affected in different sectors, which ones survived and which got crushed by the virus"),
            ],className='p-2 text-muted'),
        ], className='box', style={'background-color': '#f1f9ff', 'padding': '20px', 'border-radius': '10px', 'width': '50%'}),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px'}),


    html.Div([
        html.Div([
            html.Div([
                html.P("The COVID-19 pandemic, which began in late 2019, has had profound impacts on the world across various dimensions—health, economy, education, and social structures."),
                html.P("It reshaped the world in many ways, highlighting vulnerabilities in health systems, economies, and social structures. While recovery is underway, the long-term effects of the pandemic will likely continue to influence global policies and societal norms for years to come."),
                html.P("The numbers reflect not just a health crisis but also an economic and social transformation that demands comprehensive responses and recovery strategies."),

                html.Div([
                    html.Br(),
                    html.Div([
                        html.Br(),
                        html.P("Covid Cases (Oct-2020)", className="fw-bold text-primary fs-4 text-center"),
                        html.P("770 million", className="fw-bold text-info display-5 text-center"),  
                        html.P("(7 million reported deaths)", className="fs-5 text-center"),  
                    ], className="col-md-4"),

                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.P("But", className="fw-bold text-primary fs-5 text-center"),
                        html.P("alongside", className="fw-bold text-primary fs-5 text-center"),
                        html.P("that", className="fw-bold text-primary fs-5 text-center"),
                        html.Br(),
                    ], className="col-md-4"),

                    html.Div([
                        html.Br(),
                        html.P("Vaccine Doses Given", className="fw-bold text-primary fs-4 text-center"),
                        html.P("13 million", className="fw-bold text-info display-5 text-center"),  
                        html.P("(60% of the people received atleast one dose)", className="fs-5 text-center"),  
                    ], className="col-md-4"),

                    html.Div([
                        html.Div([
                            html.P("It also exacerbated mental health issues globally, with a reported 25% increase in anxiety and depression. More than 30% of adults experienced symptoms of anxiety or depression during the pandemic.")],className='box_comment fs-5 text-center'),
                    ], className="col-md-6"),

                    html.Div([
                        html.Div([
                            html.P("Marginalized groups were affected disproportionately, including low-income workers, women, and racial minorities, exacerbating existing inequalities. About 97 million people fell into extreme poverty as a result of this pandemic")],className='box_comment fs-5 text-center'),
                    ], className="col-md-6"),
                ], className='row mb-5'),
            ],className = 'box', style = {'width':'50%'}),

            html.Div([
                html.Img(src='assets/cases.jpeg', style={'width': '100%'}),
                html.Br(),
                html.Div(children=[
                    html.P("The rapid development of vaccines was unprecedented, with multiple vaccines receiving emergency use authorization within a year of the pandemic’s onset. Global scientific collaboration intensified, leading to significant advancements in virology, vaccine technology, and public health strategies.", className='p-3 text-muted text-center'),
                ], style={'background-color': '#ffffff', 'border-radius': '10px', 'margin': '10px', 'padding': '15px', 'width': '100%'}),
            ], style = {'width':'50%'}),
        ],style = {'display':'flex', 'justify-content': 'space-around', 'padding': '20px'}),
    ], style = {'width': '100%'}),


    html.Div([
        html.Br(),
        html.Div([
            html.Br(),
            html.H2("Human Development Index over the Years", className = "text-center"),
            html.Br(),
            html.P("The HDI measures development based on life expectancy, education, and income per capita, providing a snapshot of countries’ socio-economic progress. According to the United Nations Development Programme (UNDP), global HDI dropped for the first time since measurements began in 1990, marking a historical decline due to COVID-19."),
            html.P("Education systems were heavily impacted, with over 1.6 billion students out of school at one point, leading to significant learning loss. This transition to online learning revealed stark inequalities in access to technology, particularly in low-income regions, further exacerbating educational disparities. Mental health issues also surged during this period, with a reported 25% increase in anxiety and depression globally, affecting millions as isolation and uncertainty took their toll."),
            html.P("Economically, the pandemic triggered a severe global recession, causing the global economy to contract by about 3.5% in 2020. Governments responded with extensive fiscal measures, totaling over $12 trillion, to support businesses and individuals affected by lockdowns and restrictions. This financial support was crucial, as millions faced unemployment, with estimates indicating that about 220 million people lost their jobs at the pandemic's peak. Despite a rebound in 2021 with a growth rate of around 6%, the long-term economic ramifications are still being felt."),
            html.Br(),
        ],className='box', style={'background-color': '#f1f9ff', 'padding': '20px', 'border-radius': '10px', 'width': '100%'}),
        html.Br(),
        dcc.Graph(id='hdi-world-map', style={'height': '100%', 'width': '100%'}),
        html.Br(),
    ], style={'margin': '20px'}),


    html.Div([
        html.P("Despite the challenges, the pandemic fostered unprecedented levels of scientific collaboration, resulting in the rapid development of vaccines and public health strategies that continue to shape responses to health crises. Overall, the pandemic has reshaped the world, highlighting vulnerabilities in health systems and economic structures, and prompting discussions about resilience and equity in recovery efforts. Discover more sections for an in-depth analysis of specific areas, from trade to government responses, as we explore the legacy of COVID-19 on the global economy."),
    ], className="box_comment fs-4 text-center", style={'margin': '20px', 'padding': '20px', 'background-color': '#e9f5ff', 'border-radius': '10px'}),

    html.Br(),
    html.Br(),
    html.Br(),
])






####################### CALLBACKS #############################

@dash.callback(
    Output('hdi-world-map', 'figure'),
    Input('hdi-world-map', 'id')  
)

def update_hdi_map(_):
    fig = px.choropleth(
        df,
        locations='Country',
        locationmode='country names',  
        color='HDI',
        hover_name='Country',
        animation_frame="Year",
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'HDI': 'HDI'},
        # title='Human Development Index (HDI) by Country',
        range_color=(0, 1)  
    )
    fig.update_geos(projection_type="mercator")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    return fig

