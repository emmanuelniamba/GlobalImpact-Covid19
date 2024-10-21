import dash
from dash import html

dash.register_page(__name__, path='/', name="Name of Tab=Global", order=0)
# Order = order of the page in nav bar. Start from 0


####################### PAGE LAYOUT #############################

content = '''

THE PLAN
1. Home / Overview Page\n
Page Name: "Global Economic Overview"\n
Purpose: Introduce the dashboard and provide a high-level summary of COVID-19's impact on the global economy.\n
\n
Content:\n
Key economic indicators (e.g., GDP, unemployment, inflation) at a glance (using summary cards or small visual snippets).
A world map highlighting the worst-hit regions (based on GDP decline, unemployment rates, etc.).
A line graph showing the global trend of GDP, stock markets, and unemployment over time.
\n
Visualizations:\n
Map: Global heatmap of GDP change during COVID-19.
Line chart: Overall trends in economic growth, unemployment, and inflation.
\n\n

2. GDP and Economic Growth
Page Name: "GDP & Economic Growth"
Purpose: Analyze the impact of COVID-19 on the GDP of different countries and regions.

Content:
Time-series analysis of GDP growth pre- and post-COVID.
Comparative analysis of GDP contraction and recovery across regions.
Highlight top countries with the biggest growth and decline.

Visualizations:
Line chart: Global GDP growth trends over time.
Bar chart: GDP change comparison between countries.
Scatter plot: GDP growth vs. unemployment rate.

\n\n
3. Employment and Labor Market
Page Name: "Employment & Labor Market"

Purpose: Focus on how COVID-19 affected global employment, labor force participation, and unemployment rates.
Content:
Comparative analysis of unemployment rates across countries.
Relationship between GDP and unemployment rate (Phillips Curve).
Impact on different sectors (e.g., tourism, healthcare).
Visualizations:
Bar chart: Country-wise unemployment rates during and after COVID.
Scatter plot: GDP vs. unemployment rate.
Time-series plot: Unemployment trends across countries or regions.
4. Inflation and Prices
Page Name: "Inflation & Prices"

Purpose: Explore inflation rates during COVID-19, especially the effects of supply chain disruptions.
Content:
Comparison of inflation rates across countries.
Impact of COVID-19 on essential commodities and services.
Discussion of supply chain challenges and price fluctuations.
Visualizations:
Line chart: Inflation rate trends over time.
Heatmap: Correlation between inflation and other variables (unemployment, trade).
Bubble chart: Inflation vs. GDP growth vs. population.
5. Trade and Supply Chains
Page Name: "Global Trade & Supply Chains"

Purpose: Analyze how COVID-19 impacted international trade, exports, imports, and supply chains.
Content:
Overview of how global trade volume decreased due to the pandemic.
Comparative analysis of export/import volumes across countries.
Analysis of specific industries affected (e.g., manufacturing, energy).
Visualizations:
Bar chart: Trade volume changes for key countries.
Line chart: Time-series showing export/import trends.
Scatter plot: Trade volume vs. stock market performance.
6. Government Response and Debt
Page Name: "Government Response & Debt"

Purpose: Examine how governments responded to the economic crisis through fiscal measures (stimulus packages, debt levels).
Content:
Comparison of stimulus packages across countries.
Impact of increased government borrowing and debt on long-term economic stability.
Correlation between government debt and GDP recovery.
Visualizations:
Dual-axis line chart: GDP growth vs. government debt.
Pie chart: Share of government expenditure on COVID-19 relief.
Time-series: Debt growth over time.
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
8. Sector-Specific Impact
Page Name: "Sectoral Impact"

Purpose: Dive deeper into the impact of COVID-19 on specific economic sectors such as healthcare, tourism, retail, and manufacturing.
Content:
Breakdown of the most impacted sectors.
Analysis of sector-specific unemployment and recovery rates.
Impact on essential and non-essential industries.
Visualizations:
Bar chart: Sector-wise GDP contribution pre- and post-pandemic.
Scatter plot: Sectoral employment trends.
Pie chart: Share of economic output by sector.
9. Comparative Analysis
Page Name: "Comparative Insights"

Purpose: A deep-dive comparative analysis of multiple parameters together to understand their relationships.
Content:
Correlation matrix of key economic indicators (GDP, inflation, unemployment).
Comparative analysis of regions/countries that recovered quickly vs. those that didn’t.
Visualizations:
Heatmap: Correlation matrix for different economic indicators.
Bubble chart: Comparing GDP growth, unemployment, and inflation across countries.
Scatter plot: Multi-variable comparison (e.g., debt, GDP, stock markets).
'''

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Covid 19 Combined Dataset Overview"),
        "<Put a brief description>",
        html.Br(),html.Br(),
        "Put links of all the datasets. Citations are important.",
        ]),

    html.Div(children=[
        html.Br(), 
        content,
        "Number of Instances: 178",html.Br(),
        "Number of Attributes: 13 numeric, predictive attributes and the class",
        html.Br(),html.Br(),
        html.B("We can add names of metrics here"),
        html.Br(),
        html.B("- Metric 1"),
        html.Br(),
        html.B("- Metric 2"),
        html.Br(),
        html.B("- Metric 3"),
    ])
    
], className="p-4 m-2", style={"background-color": "#e3f2fd"})