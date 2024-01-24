"""
Example of light and dark color modes available in
  dash-bootstrap-component >= 1.5.0
  dash-bootstrap-templates >= 1.1.0
"""

from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates import load_figure_template


# local imports 
from Batteries.figures           import * 
from Batteries.knobs_and_buttons import * 
from Batteries.control_panels    import * 

# adds  templates to plotly.io
load_figure_template(["minty_dark", "minty"]) 
 
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME]) 
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery  
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# batter buttons and knobs 
battery_control_panel_1 = generate_battery_control_panel_1()
battery_control_panel_2 = generate_battery_control_panel_2() 
battery_control_panel_3 = generate_battery_control_panel_3() 
 
# Battery Plots  
battery_fig         = generate_battery_scatter_plot()
battery_spider_plot = generate_battery_spider_plot()
battery_map         = generate_battery_dev_map()
 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Motors 
# ---------------------------------------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Inverters 
# ---------------------------------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Cables 
# ---------------------------------------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Motors 
# ---------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Layout  
# ---------------------------------------------------------------------------------------------------------------------------------------------------

app.layout = dbc.Container(
    [
        html.Div(["State of Battery Development"], className="bg-primary text-white h2 p-2"),
        html.Div(["Battery Metric Indicator"], className="bg-primary text-white h5 p-2"),
        color_mode_switch, 
        dbc.Row([ dbc.Col([battery_control_panel_1  ],  width=3),  
                  dbc.Col([ dcc.Graph(id="battery_fig", figure= battery_fig, className="border")],  width=9),
                ]),     
        html.Hr(),  
        html.Div(["Battery Cell Comparison"], className="bg-primary text-white h5 p-2"),        
        dbc.Row([ dbc.Col([battery_control_panel_2  ],  width=3),  
                  dbc.Col([dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item') ],  width=3), 
                  dbc.Col([ dcc.Graph(id="battery_spider_plot", figure= battery_spider_plot , className="border")],  width=6),
                ]),          
        html.Hr(),
        html.Div(["Worldwide Battery Development"], className="bg-primary text-white h5 p-2"),    
        dbc.Row([ dbc.Col([battery_control_panel_3  ],  width=3),   
                  dbc.Col([ dcc.Graph(id="battery_map", figure= battery_map, className="border")],  width=9),
                ]), 
        
    ]

)
 
@callback(
    Output("battery_fig", "figure"),
    Input("color-mode-switch", "value"),
)

@callback(
    Output("battery_spider_plot", "figure"),
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


# https://www.researchgate.net/figure/Distance-distribution-of-daily-flights-worldwide-Data-from-ref-5_fig2_351583250

if __name__ == "__main__":
    app.run_server(debug=True)
    
    