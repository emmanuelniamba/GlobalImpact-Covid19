from plotly.data import gapminder # For dataset
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash


# Needs to be updated please we need to find a better bootstrap template
external_css = ["https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/lux/bootstrap.min.css", ]
external_js = [
    "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js"
]

# Establishing the main server for our application/dashboard
app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css, external_scripts=external_js)
server = app.server

df = pd.read_csv("/Users/prachikansal/Desktop/centrale med/mock project/data/pmi_unemployment_data.csv")


img_tag = html.Img(src="assets/cc.png", width=27, className="m-1")
brand_link = dcc.Link([img_tag, "  Team3 "], href="#", className="navbar-brand")
pages_links = [dcc.Link(page['name'], href=page["relative_path"], className="nav-link")\
	         for page in dash.page_registry.values()]

app.layout = html.Div([
	### Navbar
    # html.Nav(children=[
	#     html.Div([
	# 		    html.Div([brand_link, ] + pages_links, className="navbar-nav")
    #     ], className="container-fluid"),
    # ], className="navbar navbar-expand-lg bg-dark", **{"data-bs-theme": "dark"}),
    html.Nav(children=[
		html.Div([
			html.Div([brand_link], className="navbar-brand"),  # Brand link remains as is
			html.Div([
				# Dropdown toggle button
				html.Div([
					html.Button(
						"Navigation",
						className="btn btn-dark dropdown-toggle",
						id="navbarDropdown",
						**{"data-bs-toggle": "dropdown"}, 
						**{"aria-expanded": "true"}
					),
					# Dropdown menu
					html.Ul([
						html.Li(dcc.Link(page['name'], href=page["relative_path"], className="dropdown-item"))
						for page in dash.page_registry.values()
					], className="dropdown-menu", **{"aria-labelledby": "navbarDropdown"})
				], className="dropdown"),
			], className="navbar-nav")
		], className="container-fluid"),
	], className="navbar navbar-expand-lg bg-dark", **{"data-bs-theme": "dark"}),

	#### Main Page
    html.Div([
	    html.Br(),
	    html.P('Impact of COVID-19 on Global Economy', className="text-dark text-center fw-bold fs-1"),
	    dash.page_container
	], className="col-11 mx-auto")
], style={"height": "100vw", "background-color": "#e3f2fd"})

if __name__ == '__main__':
	app.run(debug=True, port=5050)