"""
Example of light and dark color modes available in
  dash-bootstrap-component >= 1.5.0
  dash-bootstrap-templates >= 1.1.0
"""

from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# adds  templates to plotly.io
load_figure_template(["minty_dark", "minty"])


df = px.data.gapminder()

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------

battery_brand = html.Div(
    [
        dbc.Label("Select Battery Brand"),
        dcc.Dropdown(
            ["gdpPercap", "lifeExp", "pop"],
            value = 'All',
            placeholder = 'All',
            clearable = True,
            disabled = False,
            style = {'display': True, 'color': 'black'},
            id="indicator",   
        ),
    ],
    className="mb-4",
)


battery_chemistry = html.Div(
    [
        dbc.Label("Select Battery Chemistry"),
        dcc.Dropdown(
            ["gdpPefrcap", "lifreExp", "pfop"],
            value = 'All',
            placeholder = 'All',
            clearable = True,
            disabled = False,
            style = {'display': True, 'color': 'black'},
            id="indicator2",   
        ),
    ],
    className="mb-4",
) 
  

battery_x_axis = html.Div(
    [
        dbc.Label("X-Axis"),
        dcc.Dropdown(
            ["gdpPefrcfsap", "lifreEfsxp", "pfopfs"],
            value = 'Specific_Power',
            placeholder = 'Select Indicator',
            clearable = True,
            disabled = False,
            style = {'display': True, 'color': 'black'},
            id="indicator3",   
        ),
    ],
    className="mb-4",
) 

battery_y_axis = html.Div(
    [
        dbc.Label("Y-Axis"),
        dcc.Dropdown(
            ["gdpPfefrcap", "lifrfeExp", "pffop"],
            value = 'Specific_Energy',
            placeholder = 'Select Indicator',
            clearable = True,
            disabled = False,
            style = {'display': True, 'color': 'black'},
            id="indicator4",   
        ),
    ],
    className="mb-4",
) 
   

battery_dev_year = html.Div(
    [
        dbc.Label("Select Year Range"),
        dcc.RangeSlider(
            2000,
            2024, 
            1,
            id="years",
            marks={i: '{}'.format(i) for i in range(2000,2025,5)},
            tooltip={"placement": "bottom", "always_visible": True},
            value=[2000, 2024], 
        ),
    ],
    className="mb-4",
)

battery_controls_1 = dbc.Card(
    [battery_brand,battery_chemistry,battery_x_axis,battery_y_axis,battery_dev_year],
    body=True,
)

battery_fig = px.scatter(
        df.query("year==2007"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
        template="minty",
    )
 
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  
battery_map = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=1 )
battery_map.update_layout(mapbox_style="open-street-map") 



app.layout = dbc.Container(
    [
        html.Div(["State of Battery Development"], className="bg-primary text-white h3 p-2"),
        color_mode_switch, 
        dbc.Row([ dbc.Col([battery_controls_1  ],  width=4),  
                  dbc.Col([ dcc.Graph(id="battery_fig", figure= battery_fig, className="border")],  width=8),
                ]),         
         dcc.Graph(id="battery_map", figure= battery_map, className="border"),        
    ]

)
 
@callback(
    Output("battery_fig", "figure"),
    Input("color-mode-switch", "value"),
)

@callback(
    Output("battery_map", "figure"),
    Input("color-mode-switch", "value"),
)
 
 
def update_figure_template(switch_off):
    template = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    patched_figure = Patch()
    patched_figure["layout"]["template"] = template
    return patched_figure



clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)


if __name__ == "__main__":
    app.run_server(debug=True)