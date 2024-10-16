import dash
from dash import html

dash.register_page(__name__, path='/', name="Name of Tab=Global", order=0)
# Order = order of the page in nav bar. Start from 0


####################### PAGE LAYOUT #############################

layout = html.Div(children=[

    html.Div(children=[
        html.H2("Covid 19 Combined Dataset Overview"),
        "<Put a brief description>",
        html.Br(),html.Br(),
        "Put links of all the datasets. Citations are important.",
        ]),

    html.Div(children=[
        html.Br(),
        html.H2("Data Variables"),
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