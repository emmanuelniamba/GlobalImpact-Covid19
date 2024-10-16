import pandas as pd
import dash
from dash import Dash, dcc, html
import plotly.graph_objs as go
from plotly.subplots import make_subplots


# Register the page for multi-page Dash apps
dash.register_page(__name__, path='/consumerconfidence', name="Consumer Confidence Analysis", order=5)

df = pd.read_csv("data/pmi_unemployment_data.csv", index_col='date', parse_dates=True)
df['unemployment rate'] = df['unemployment rate'].str.replace('%', '').astype(float)

# Create subplot for consumer confidence over time for different countries
def create_consumer_confidence_plot(df):
    # Initialize subplots with 3 rows and 3 columns
    fig = make_subplots(rows=3, cols=3, subplot_titles=df['country'].unique())

    # Loop through the countries and plot the consumer confidence over time
    for i, country in enumerate(df['country'].unique()):
        # Filter the data for the current country
        filtered_df = df[df['country'] == country]

        # Use the index (which is the date) for the x-axis
        fig.add_trace(
            go.Scatter(x=filtered_df.index, y=filtered_df['consumer confidence'], mode='lines', name=country),
            row=(i // 3) + 1, col=(i % 3) + 1
        )

    # Update layout of the plot
    fig.update_layout(height=900, width=1200, title_text="Consumer Confidence Over Time for Different Countries")
    
    return fig


layout = html.Div(children=[
    html.Br(),
    html.H2("Unemployment Rates", className="fw-bold text-center"),
    html.Br(),
    dcc.Graph(id="consumerconfidence", figure=create_consumer_confidence_plot(df))
])
