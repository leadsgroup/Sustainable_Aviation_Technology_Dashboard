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
from Flight_Operations.figures           import *
from Flight_Operations.knobs_and_buttons import * 
from Flight_Operations.control_panels    import * 
from Batteries.figures                   import * 
from Batteries.knobs_and_buttons         import * 
from Batteries.control_panels            import * 

# Deployment 
# https://www.youtube.com/watch?v=XWJBJoV5yww&t=0s&ab_channel=CharmingData 
# *** to remove ****  

filename = 'Data/LEADS_SAT_Dashboard_Data.xlsx'
SAT_data = pd.read_excel(filename,sheet_name=['Commercial_Batteries', 'Air_Travel','Global_Temperature']) 
Commercial_Batteries = SAT_data['Commercial_Batteries']
Air_Travel           = SAT_data['Air_Travel']
Global_Temperature   = SAT_data['Global_Temperature']
a                    = Commercial_Batteries['Brand']  
b                    = Commercial_Batteries['Chemistry']
c                    = Commercial_Batteries['Model']
d                    = a + ' ' + b + ' ' + c 
Commercial_Batteries["Battery Name"] = d        

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
# Airline Flight Operations  
# ---------------------------------------------------------------------------------------------------------------------------------------------------
flight_ops_aircraft_panel  = generate_flight_ops_aircraft_panel()  
flight_ops_map             = generate_flight_ops_map()
airport_bar_chart          = generate_flight_ops_airport_bar_chart()
global_temperature_map     = generate_global_temperature_map()
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery  
# --------------------------------------------------------------------------------------------------------------------------------------------------- 
battery_metrics_panel       = generate_battery_metrics_panel(Commercial_Batteries)
battery_comparison_panel    = generate_battery_comparison_panel(Commercial_Batteries)   
battery_development_panel   = generate_battery_development_panel(Commercial_Batteries)  
battery_map                 = generate_battery_dev_map(Commercial_Batteries)
 

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
        html.Div(["Sustainable Aviation Technology Dashboard"], className="bg-success text-center text-white h2 p-2"),
        
        dbc.Row([ 
             dbc.Col([ 
                 dbc.Card([  html.Plaintext(
                     children= ' text text text text text text text text text text' ,
                                            id= "header", 
                                            )
                     
                     ],body=True) 
                 
                 ],  width=8),  
             dbc.Col([ ],  width=4),  
            
            ]), 
        
        html.Div(["Commercial Battery Landscape"], className="bg-primary text-white h5 p-2"),
        color_mode_switch, 
        dbc.Row([ dbc.Col([battery_metrics_panel  ],  width=4),  
                  dbc.Col([ dcc.Graph(id       ="battery_metrics_figure", 
                                      className="border-0 bg-transparent")],  width=8),
                ]),    
        html.Div([    html.Br() ]),   
        html.Div(["Battery Cell Comparison"], className="bg-primary text-white h5 p-2"),   
        dbc.Row([   
                  dbc.Col([battery_comparison_panel],  width=6),    
                  dbc.Col([ dcc.Graph(id="battery_spider_plot", 
                                      className="border-0 bg-transparent")],  width=6),
                ]), 
        html.Div(["Worldwide Battery Development"], className="bg-primary text-white h5 p-2"),    
        dbc.Row([dbc.Col([battery_development_panel  ],  width=4),   
                dbc.Col([ dcc.Graph(id="battery_map",
                                    figure= battery_map,
                                    className="border-0 bg-transparent")],  width=8),
                ]), 
          
        html.Div(["Airline Flight Operations"], className="bg-primary  text-white h5 p-2"), 
        dbc.Row([  dbc.Col([flight_ops_aircraft_panel ],  width=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Ground Temperature"], className="text-sm-center h4"),
                       dcc.Graph(id="global_temperature_map",
                                               figure= global_temperature_map,
                                               className="border-0 bg-transparent"), 
                           
                       dcc.Graph(id="airport_bar_chart",
                                           figure= airport_bar_chart, )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=8),                
                
                ]), 
        html.Div(["Feasible Routes"], className="bg-primary  text-white h5 p-2"),  
        dbc.Row([     dbc.Col([
                      dbc.Card([
                      dbc.Row([
                      dbc.Col([    
                      html.Div(["Passengers: "], className="h6"), 
                      html.Div(["Max Takeoff Weight (kg): "], className="h6"),     
                      html.Div(["Lift-to-Drag Ratio "], className="h6"),        
                      html.Div(["Max Power (W): "], className="h6"),  
                      html.Div(["Max Voltage (V): "], className="h6"),     
                      html.Div(["Nominal Voltage (V): "], className="h6"),      
                      html.Div(["Capacity (mAh): "], className="h6"),     
                      html.Div(["Max Discharge Current (A): "], className="h6"),     
                      html.Div(["Max Discharge Power (W): "], className="h6"),       
                      html.Div(["Cell Mass (g): "], className="h6"),      
                      html.Div(["Energy Density (Wh/kg): "], className="h6"),      
                      html.Div(["Power Density (W/kg): "], className="h6"),  
                      html.Div(["Max Operating Temp. (deg. C): "], className="h6"),   
                      html.Div(["Min Operating Temp. (deg. C): "], className="h6"), 
                      ],  width=8),

                      dbc.Col([    
                      html.Div(["Value"], className="h6"), 
                      html.Div(["Value"], className="h6"),     
                      html.Div(["Value "], className="h6"),        
                      html.Div(["Value"], className="h6"),  
                      html.Div(["Value"], className="h6"),     
                      html.Div(["Value"], className="h6"),      
                      html.Div(["Value"], className="h6"),     
                      html.Div(["Value"], className="h6"),     
                      html.Div(["Value"], className="h6"),       
                      html.Div(["Value"], className="h6"),      
                      html.Div(["Value"], className="h6"),      
                      html.Div(["Value"], className="h6"),  
                      html.Div(["Value"], className="h6"),   
                      html.Div(["Value"], className="h6"), 
                      ],  width=4), 
                      ])
                      ],body=True, className="border-0 bg-transparent") 
                      ],  width=4), 

                    dbc.Col([ dcc.Graph(id="flight_ops_map",
                                    figure= flight_ops_map,
                                    className="border-0 bg-transparent")],  width=8),                  
                ]),   
        

        html.Div(["Contact Us"], className="bg-success text-white h2 p-2"),         
    ]

)
 
 
@callback(
    Output("battery_metrics_figure", "figure"),
    Input("battery_brand_metrics", "value"),
    Input("battery_chemistry_metrics", "value"),
    Input("battery_x_axis_metrics", "value"),
    Input("battery_y_axis_metrics", "value"),
    Input("color-mode-switch", "value"),
) 
def update_battery_metrics_figure(selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off):
    filename = 'Data/LEADS_SAT_Dashboard_Data.xlsx'
    SAT_data = pd.read_excel(filename,sheet_name=['Commercial_Batteries', 'Air_Travel','Global_Temperature']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries']    
    fig = generate_battery_scatter_plot(Commercial_Batteries,selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off)  
    return fig 
 
@callback(
    Output("battery_spider_plot", "figure"),
    Input("battery_1", "value"),
    Input("battery_2", "value"),
    Input("battery_3", "value"),
    Input("color-mode-switch", "value"),
)

def update_battery_comparison_figure(bat_1,bat_2,bat_3,switch_off):
    filename = 'Data/LEADS_SAT_Dashboard_Data.xlsx'
    SAT_data = pd.read_excel(filename,sheet_name=['Commercial_Batteries', 'Air_Travel','Global_Temperature']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ' ' + b + ' ' + c 
    Commercial_Batteries["Battery Name"] = d       
    fig_2 = generate_battery_spider_plot(Commercial_Batteries,bat_1,bat_2,bat_3,switch_off)  
    return fig_2  

@callback(
    Output("battery_map", "figure"),
    Input("color-mode-switch", "value"),
) 

@callback(
    Output("flight_ops_map", "figure"),
    Input("color-mode-switch", "value"),
)  

@callback(
    Output("airport_bar_chart", "figure"),
    Input("color-mode-switch", "value"),
)  

@callback(
    Output("global_temperature_map", "figure"),
    Input("color-mode-switch", "value"),
)  
 
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
    
    