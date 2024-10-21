from plotly.data import gapminder  # For dataset
from dash import dcc, html, Dash
import pandas as pd
import dash

# External Bootstrap CSS and JS
external_css = ["https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/lux/bootstrap.min.css"]
external_js = [
    "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js"
]

# Establishing the main server for our application/dashboard
app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css, external_scripts=external_js)
server = app.server

# Sample dataset (replace with your actual data path)
df = pd.read_csv(r"C:\Users\hp\OneDrive\Desktop\covidddd\GlobalImpact-Covid19\data\pmi_unemployment_data.csv")

# Navbar components
img_tag = html.Img(src="assets/cc.png", width=27, className="m-1")
brand_link = dcc.Link([img_tag, html.Span("Impact of COVID-19 on Global Economy ", className="glow-text")], href="#", className="navbar-brand")
pages_links = [
    dcc.Link(page['name'], href=page["relative_path"], className="dropdown-item")
    for page in dash.page_registry.values()
]

# Layout of the Dash app
app.layout = html.Div(style={
    "height": "100vh",
    "background": "rgba(0, 0, 0, 0.5) url('/assets/background.jpg') no-repeat center center fixed",
    "background-size": "cover",
    "position": "relative"
}, children=[

    ### Navbar
    html.Nav([
        html.Div([

            # Navbar brand/logo
            html.A(brand_link, className="navbar-brand"),

            # Navbar toggler for smaller screens
            html.Button(
                "Toggle navigation",
                className="navbar-toggler",
                **{"data-bs-toggle": "collapse"},
                **{"data-bs-target": "#navbarNav"},
                **{"aria-controls": "navbarNav"},
                **{"aria-expanded": "false"},
                **{"aria-label": "Toggle navigation"}
            ),

            # Collapsible navbar items
            html.Div([
                html.Ul([
                    # Dropdown menu
                    html.Li([
                        html.A("Navigation", className="nav-link dropdown-toggle", **{"data-bs-toggle": "dropdown"}, **{"aria-expanded": "false"}),
                        html.Ul([
                            html.Li(page_link) for page_link in pages_links
                        ], className="dropdown-menu")
                    ], className="nav-item dropdown"),
                ], className="navbar-nav ms-auto me-3")  # Shift to the right with a margin

            ], className="collapse navbar-collapse", id="navbarNav")

        ], className="container-fluid")
    ], className="navbar navbar-expand-lg navbar-dark bg-dark"),

    #### Main Page
    html.Div([
        html.Br(),
        html.P('Overview', className="text-white text-center fw-bold fs-1 glow-text"),
        dash.page_container
    ], className="col-11 mx-auto")

])

# Add custom CSS for glow effect
app.css.append_css({
    "external_url": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
})

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%css%}
        <style>
            /* Glow Text Effect */
            .glow-text {
                color: white;  /* Change text color to white */
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8),
                             0 0 20px rgba(255, 255, 255, 0.6),
                             0 0 30px rgba(255, 255, 255, 0.4),
                             0 0 40px rgba(0, 255, 255, 0.2); /* Adjust glow color here */
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=8050)
