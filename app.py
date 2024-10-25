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

# Navbar components
brand_link = dcc.Link("HOME", href="/", className="navbar-brand text-black")
pages_links = [
    # dcc.Link(page['name'], href=page["relative_path"], className="dropdown-item")
    dcc.Link(page['name'], href=page["relative_path"], className="nav-link text-black page-link")
    for page in dash.page_registry.values() if page['name'] != 'Homepage'  # Exclude homepage from side menu
]

# Layout of the Dash app
app.layout = html.Div(style={
    "height": "100vh",
    "background": "rgba(205, 225, 237, 0.1) url('/assets/background.jpg') no-repeat center center fixed",
    "background-size": "cover",
    "position": "relative"
}, children=[


    html.Nav([
        html.Div([
            
            html.A(brand_link, className="navbar-brand"),
           
            html.Button(
                "☰ Menu",
                className="btn menu-btn",
                # style={"border": "none", "font-size": "20px"},
                style={"border": "none"},
                **{"data-bs-toggle": "offcanvas"},
                **{"data-bs-target": "#offcanvasSidebar"},
                **{"aria-controls": "offcanvasSidebar"}
            )

        ], className="container-fluid d-flex justify-content-between")
    ], className="navbar navbar-expand-lg navbar-dark"), 

    # Off-canvas sidebar menu
    html.Div([
        html.Div([
            html.Br(),
            html.Button("", className="btn-close text-reset close-btn", style={"font-size": "24px"}, **{"data-bs-dismiss": "offcanvas"}, **{"aria-label": "Close"}),
            html.Div([
                html.Ul([html.Li(page_link, className="nav-item mb-4") for page_link in pages_links], className="navbar-nav mt-3")  
            ])
        ], className="offcanvas-body")
    ], className="offcanvas offcanvas-start", **{"tabIndex": "-1", "id": "offcanvasSidebar", "aria-labelledby": "offcanvasSidebarLabel"}),


    #### Main Page
    html.Div([
        html.Br(),
        dash.page_container
    ], className="col-11 mx-auto")

])


# Custom JavaScript to close the sidebar on link click
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%css%}
        <style>
            /* Custom styles */
            .offcanvas .nav-link {
                font-size: 16px;  
                text-shadow: none; 
            } 
            .offcanvas .close-btn {
                font-size: 24px; /* Larger close button */
            }
            .menu-btn {
                border: none;
                font-size: 20px;  /* Larger font size for menu button */
            }

        </style>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                // Close offcanvas sidebar after selecting an option
                document.querySelectorAll(".page-link").forEach(link => {
                    link.addEventListener("click", function() {
                        var offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById("offcanvasSidebar"));
                        offcanvas.hide();  // Hide the sidebar
                    });
                });
            });
        </script>
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

# ----------------------------------------------------------------

# from plotly.data import gapminder  # For dataset
# from dash import dcc, html, Dash
# import pandas as pd
# import dash

# # External Bootstrap CSS and JS
# external_css = ["https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/lux/bootstrap.min.css"]
# external_js = [
#     "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js",
#     "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js"
# ]

# # Establishing the main server for our application/dashboard
# app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css, external_scripts=external_js)
# server = app.server

# # Sample dataset (replace with your actual data path)
# df = pd.read_csv("data/pmi_unemployment_data.csv")

# # Navbar components
# img_tag = html.Img(src="assets/jj.png", width=27, className="m-1")
# brand_link = dcc.Link([img_tag, html.Span("Impact of COVID-19 on Global Economy ")], href="#", className="navbar-brand")
# pages_links = [
#     dcc.Link(page['name'], href=page["relative_path"], className="dropdown-item")
#     for page in dash.page_registry.values()
# ]

# # Layout of the Dash app
# app.layout = html.Div(style={
#     "height": "100vh",
#     "background": "rgba(205, 225, 237, 0.1) url('/assets/background.jpg') no-repeat center center fixed",
#     "background-size": "cover",
#     "position": "relative"
# }, children=[

#     ### Navbar
#     html.Nav([
#         html.Div([

#             # Navbar brand/logo
#             html.A(brand_link, className="navbar-brand"),

#             # Navbar toggler for smaller screens
#             html.Button(
#                 "Toggle navigation",
#                 className="navbar-toggler",
#                 **{"data-bs-toggle": "collapse"},
#                 **{"data-bs-target": "#navbarNav"},
#                 **{"aria-controls": "navbarNav"},
#                 **{"aria-expanded": "false"},
#                 **{"aria-label": "Toggle navigation"}
#             ),

#             # Collapsible navbar items
#             html.Div([
#                 html.Ul([
#                     # Dropdown menu
#                     html.Li([
#                         html.A("Navigation", className="nav-link dropdown-toggle", **{"data-bs-toggle": "dropdown"}, **{"aria-expanded": "false"}),
#                         html.Ul([
#                             html.Li(page_link) for page_link in pages_links
#                         ], className="dropdown-menu")
#                     ], className="nav-item dropdown"),
#                 ], className="navbar-nav ms-auto me-3")  # Shift to the right with a margin

#             ], className="collapse navbar-collapse", id="navbarNav")

#         ], className="container-fluid")
#     ], className="navbar navbar-expand-lg navbar-dark bg-dark"),

#     #### Main Page
#     html.Div([
#         html.Br(),
#         html.P('', className="text-white text-center fw-bold fs-1"),
#         dash.page_container
#     ], className="col-11 mx-auto")

# ])

# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%css%}
#         <style>
#         </style>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''

# if __name__ == '__main__':
#     app.run(debug=True, port=8050)


# ----------------------------------------------------------------


# from plotly.data import gapminder  
# from dash import dcc, html, Dash
# import pandas as pd
# import dash

# # External Bootstrap CSS and JS
# external_css = ["https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/lux/bootstrap.min.css"]
# external_js = [
#     "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js",
#     "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js"
# ]

# # Establishing the main server for our application/dashboard
# app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css, external_scripts=external_js)
# server = app.server

# # Sample dataset (replace with your actual data path)
# df = pd.read_csv("data/pmi_unemployment_data.csv")

# # Navbar components
# brand_link = dcc.Link("Impact of COVID-19 on Global Economy", href="/", className="navbar-brand text-black")
# pages_links = [
#     dcc.Link(page['name'], href=page["relative_path"], className="dropdown-item")
#     for page in dash.page_registry.values()
# ]

# # Layout of the Dash app
# app.layout = html.Div(style={
#     "height": "100vh",
#     "background": "rgba(205, 225, 237, 0.1) url('/assets/background.jpg') no-repeat center center fixed",
#     "background-size": "cover",
#     "position": "relative"
# }, children=[

#     ### Navbar
#     html.Nav([
#         html.Div([

#             # Navbar brand/logo
#             html.A(brand_link, className="navbar-brand"),

#             # Navbar toggler for smaller screens
#             html.Button(
#                 "Toggle navigation",
#                 className="navbar-toggler",
#                 **{"data-bs-toggle": "collapse"},
#                 **{"data-bs-target": "#navbarNav"},
#                 **{"aria-controls": "navbarNav"},
#                 **{"aria-expanded": "false"},
#                 **{"aria-label": "Toggle navigation"}
#             ),

#             # Collapsible navbar items
#             html.Div([
#                 html.Ul([
#                     # Dropdown menu
#                     html.Li([
#                         html.A("Navigation", className="nav-link dropdown-toggle", **{"data-bs-toggle": "dropdown"}, **{"aria-expanded": "false"}),
#                         html.Ul([
#                             html.Li(page_link) for page_link in pages_links
#                         ], className="dropdown-menu")
#                     ], className="nav-item dropdown"),
#                 ], className="navbar-nav ms-auto me-3")  # Shift to the right with a margin

#             ], className="collapse navbar-collapse", id="navbarNav")

#         ], className="container-fluid")
#     ], className="navbar navbar-expand-lg navbar-dark bg-dark"),

#     #### Main Page
#     html.Div([
#         html.Br(),
#         html.P('', className="text-white text-center fw-bold fs-1"),
#         dash.page_container
#     ], className="col-11 mx-auto")

# ])

# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%css%}
#         <style>
#         </style>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''

# if __name__ == '__main__':
#     app.run(debug=True, port=8050)