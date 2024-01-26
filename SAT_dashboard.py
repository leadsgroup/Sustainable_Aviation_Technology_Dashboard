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

# Deployment 
# https://www.youtube.com/watch?v=XWJBJoV5yww&t=0s&ab_channel=CharmingData 
# *** to remove **** 

import datetime as dt
df = pd.read_csv("Urban_Park_Ranger_Animal_Condition_Response.csv")  # https://drive.google.com/file/d/1m63TNoZdDUtH5XhK-mc4kDFzO9j97eWW/view?usp=sharing

#------------------------------------------------------------------------------
# Drop rows w/ no animals found or calls w/ varied age groups
df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Create column for month from time call made to Ranger
df['Month Call Made'] = pd.to_datetime(df['Date and Time of initial call'])
df['Month Call Made'] = df['Month Call Made'].dt.strftime('%m')
df.sort_values('Month Call Made', inplace=True)
df['Month Call Made'] = df['Month Call Made'].replace({"01":"January","02":"February","03":"March",
                                                       "04":"April","05":"May","06":"June",
                                                       "07":"July","08":"August","09":"September",
                                                       "10":"October","11":"November","12":"December",})
# Copy columns to new columns with clearer names
df['Amount of Animals'] = df['# of Animals']

# *** to remove **** 

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
                  dbc.Col([ dcc.Graph(id       ="battery_fig",
                                      figure   = battery_fig,
                                      className="border")],  width=9),
                ]),     
        html.Hr(),  
        html.Div(["Battery Cell Comparison"], className="bg-primary text-white h5 p-2"),        
        dbc.Row([ dbc.Col([battery_control_panel_2  ],  width=3),  
                  dbc.Col([html.Div(["Metric"], className="h6"),     
                      dcc.Checklist(id             = 'battery_metric_checklist',                  
                                    options        = [ {'label': x, 'value': x, 'disabled':False} for x in df['Month Call Made'].unique() ],
                                    value          = ['January','July','December'], 
                                    inline         =False,
                                    className      = 'my_box_container',    
                                    inputClassName = 'my_box_input',        
                                    labelClassName = 'my_box_label', )],  width=3),  
                  dbc.Col([ dcc.Graph(id="battery_spider_plot",
                                      figure= battery_spider_plot ,
                                      className="border")],  width=6),
                ]),          
        html.Hr(),
        html.Div(["Worldwide Battery Development"], className="bg-primary text-white h5 p-2"),    
        dbc.Row([dbc.Col([battery_control_panel_3  ],  width=3),   
                dbc.Col([ dcc.Graph(id="battery_map",
                                    figure= battery_map,
                                    className="border")],  width=9),
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

#@app.callback(
    #Output("battery_spider_plot","figure"),
    #Input("battery_metric_checklist","value"),
#) 

# 
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
#https://www.youtube.com/watch?v=amRFPjSgEnk&ab_channel=CharmingData
if __name__ == "__main__":
    app.run_server(debug=True)
    
    