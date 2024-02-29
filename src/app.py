"""Sustainable Aviation Technology Dashboard
"""

from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates                  import load_figure_template 
import pandas as pd  
import os 
from Energy_X.figures                          import *
from Energy_X.knobs_and_buttons                import * 
from Energy_X.control_panels                   import *  
from Electrification.figures                   import * 
from Electrification.knobs_and_buttons         import * 
from Electrification.control_panels            import *  

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------------------------------------------------------------------------------
ospath                                = os.path.abspath(__file__)
separator                             = os.path.sep

technology_filename  = '..' + separator + 'Data' + separator + 'Technology_Data.xlsx'
SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries','Battery_Research']) 
Commercial_Batteries = SAT_data['Commercial_Batteries'] 
a                    = Commercial_Batteries['Brand']  
b                    = Commercial_Batteries['Chemistry']
c                    = Commercial_Batteries['Model']
d                    = a + ': ' + b + '-' + c 
Commercial_Batteries["Battery Name"] = d     
Battery_Research     = SAT_data['Battery_Research']

route_temp_filename  = '..' + separator + 'Data' + separator + 'American_Airlines_Monthly_Temp.xlsx'
Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
Routes_and_Temp      = Routes_and_Temp['Sheet1'] 


temperature_filename = '..' + separator + 'Data' + separator + 'Monthly_US_County_Temperature.xlsx'
Temeperature_data    = pd.read_excel(temperature_filename,sheet_name=['US_County_Temperature_F'])  
US_Temperature_F     = Temeperature_data['US_County_Temperature_F'] 
 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Control Panels 
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Energy X
Energy_X_aircraft_flight_ops_panel = generate_Energy_X_aircraft_flight_ops_panel(US_Temperature_F)
Energy_X_battery_panel             = generate_Energy_X_battery_panel()
  
# Battery   
battery_metrics_panel               = generate_battery_metrics_panel(Commercial_Batteries)
battery_comparison_panel            = generate_battery_comparison_panel(Commercial_Batteries)   
battery_development_panel           = generate_battery_development_panel(Battery_Research)    
battery_flight_ops_aircraft_panel   = generate_flight_ops_aircraft_panel(Commercial_Batteries,US_Temperature_F)   
 
# Sustainable Aviation Fuel  

# Hydrogen 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# App Layout 
# ---------------------------------------------------------------------------------------------------------------------------------------------------


# Template and theme
load_figure_template(["minty_dark", "minty"])  
app = Dash(__name__,external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME],suppress_callback_exceptions=True)
server = app.server

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)
 
# Template  colors 
primary_color     = '#78c2ad' # grey green
secondary_color   = '#f3969a' # red  # SAF 
backround         = '#212529'
success_color     = '#56cc9d' # green Bat 
info_color        = '#6cc3d5' # blue H2 
light_color       = '#f8f9fa'
warning_color     = '#fdce67' # yellow 
dark_color        = '#828588'
font_size         =  '28px'
border            = '1px solid #828588'
tabs_styles = {
    'height': '56px'
}
tab_style = {
    'borderTop': border, 
    'borderBottom': border, 
    'borderLeft': border,
    'borderRight': border,
    'padding': '6px', 
    'color': dark_color,
    'fontSize' : font_size,
    'backgroundColor': backround,
}

tab_selected_style_1 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': success_color,
    'color': 'white', 
    'padding': '6px', 
    'fontSize' : font_size,
}
 

tab_selected_style_2 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': primary_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


tab_selected_style_3 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': secondary_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


tab_selected_style_4 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': info_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


# app layout 
app.layout = html.Div([
    html.Div(["Sustainable Aviation Technology Dashboard"], className="bg-success text-center text-white h2 p-2"),
    color_mode_switch,
    dbc.Row([ 
         dbc.Col([ ],  width=1),
         dbc.Col([ 
             dbc.Card([  
                 dbc.CardBody([
                              html.H5('Developed by the Lab for Electric Aircraft Design and Sustainablity (LEADS) at the University of Illinois Urbana-Champaign, the Sustainable Aviation Technology Dashboard is a platform to examine the integration of new batteries, sustainable aviation fuel (SAF) and hydrogen propulsion technologies into future aircraft systems and assess their broader impact on society.'),
                            ], className='text-sm-center h5'),   
                 ],body=True)  
             ],  width=10),  
         dbc.Col([ ],  width=1),  
         html.Div([ html.Br() ]),   
        ]),  
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-2', children=[
        dcc.Tab(label='Energy-eX(ploration)', value='tab-1', style=tab_style, selected_style=tab_selected_style_1),
        dcc.Tab(label='Electrification', value='tab-2', style=tab_style, selected_style=tab_selected_style_2),
        dcc.Tab(label='Sustainable Aviation Fuel', value='tab-3', style=tab_style, selected_style=tab_selected_style_3),
        dcc.Tab(label='Hydrogen', value='tab-4', style=tab_style, selected_style=tab_selected_style_4),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline'), 
    html.Div([    html.Br() ]),    
    html.Div(["Contact Us"], className="bg-success text-white h2 p-2"),
    dbc.Row([ 
         dbc.Col([ ],  width=1),
         dbc.Col([ 
             dbc.Card([   
                 dbc.CardBody([
                              html.H5('Kindly direct any questions to Dr. Matthew Clarke by sending an email to maclarke@illinois.edu. Contribute to the Dashboard by sending us information on new commercial batteries or batteries under development at high TRL levels (i.e. TRL > 8) using this link https://forms.gle/YPKqAuXwPZsoKcSdA.'),
                            ], className='text-sm-center h5'), 
                 ],body=True)  
             ],  width=10),  
         dbc.Col([ ],  width=1),  
         html.Div([ html.Br() ]),   
        ]),     
])


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
 

@callback(Output('tabs-content-inline', 'children'),
            Input('tabs-styled-with-inline', 'value'), 
              )

def render_content(tab):
    if tab == 'tab-1':
        return dbc.Container([    
            html.Div([    html.Br() ]),              
            html.Div(["Future Electrochemical Cell (Battery) Impact Predictor"], className="bg-success text-white h4 p-2"), 
            dbc.Row([  dbc.Col([ 
                html.Div(["Aircraft Parameterization"], className="text-sm-center h5"),
                Energy_X_aircraft_flight_ops_panel,  
                html.Div([    html.Br() ]),                  
                html.Div(["Battery Cell Parameterization"], className="text-sm-center h5"),                
                Energy_X_battery_panel,
                ],  width=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),                  
                       html.Div(["Feasible Routes"], className="text-sm-center h5"),
                       dcc.Graph(id="EX_flight_ops_map", className="border-0 bg-transparent"), 
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),
                       html.Div(["Average Monthly Temperature (deg. F)"], className="text-sm-center h5"),
                       dcc.Graph(id="EX_us_temperature_map", className="border-0 bg-transparent")                       
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=8),                
                
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Air Travel Techno-economics and Emissions Impact"], className="bg-success text-white h4 p-2"),    
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Travel Distances"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_passenger_range", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Airports"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_airports", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                
                
                ]), 
            html.Div([    html.Br() ]),  
            html.Div([    html.Br() ]),        
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Market Size"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_market_size", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Monthly Emissions"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_yearly_emissions", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                
                
                ]),  
        ]) 
    
    
    elif tab == 'tab-2':
        return  dbc.Container([    
            html.Div([ html.Br() ]),    
            html.Div(["Commercial Battery Assessment"], className="bg-primary text-white h4 p-2"),
            dbc.Row([ dbc.Col([battery_metrics_panel  ],  width=4),  
                      dbc.Col([ dcc.Graph(id ="battery_metrics_figure", className="border-0 bg-transparent")],  width=8),
                    ]),
            html.Div([    html.Br() ]),
            html.Div(["Commercial Battery Cell Comparison"], className="bg-primary text-white h4 p-2"),   
            dbc.Row([   
                      dbc.Col([battery_comparison_panel],  width=4),    
                      dbc.Col([ dcc.Graph(id="battery_spider_plot", className="border-0 bg-transparent")],  width=8),
                    ]),           
        
            html.Div(["Worldwide Battery Cell Development"], className="bg-primary text-white h4 p-2"),    
            dbc.Row([dbc.Col([battery_development_panel  ],  width=4),   
                dbc.Col([ dcc.Graph(id="battery_map", className="border-0 bg-transparent")],  width=8),
                ]),  
            html.Div([    html.Br() ]),             
            html.Div(["Airline Electric Aircraft Flight Operations"], className="bg-primary text-white h4 p-2"), 
            dbc.Row([  dbc.Col([battery_flight_ops_aircraft_panel ],  width=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Feasible Routes"], className="text-sm-center h5"),
                       dcc.Graph(id="flight_ops_map", className="border-0 bg-transparent"), 
                       html.Div([    html.Br() ]),
                       html.Div(["Average Monthly Temperature (deg. F)"], className="text-sm-center h5"),
                       dcc.Graph(id="US_bat_temperature_map", className="border-0 bg-transparent")                       
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=8),                
                
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Air Travel Techno-economics and Emissions Impact"], className="bg-primary text-white h4 p-2"),    
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Travel Distances"], className="text-sm-center h5"),  
                       dcc.Graph(id="electric_aircraft_passenger_range", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Airports"], className="text-sm-center h5"),  
                       dcc.Graph(id="electric_aircraft_airports", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                
                
                ]), 
            html.Div([    html.Br() ]),  
            html.Div([    html.Br() ]),        
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Market Size"], className="text-sm-center h5"),  
                       dcc.Graph(id="electric_aircraft_market_size", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Monthly Emissions"], className="text-sm-center h5"),  
                       dcc.Graph(id="electric_aircraft_yearly_emissions", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                
                
                ]),    
        ])
    
    elif tab == 'tab-3':
        return dbc.Container([    
            html.Div([ html.Br() ]),
            html.H3('Coming Soon!')
        ])
    elif tab == 'tab-4':
        return dbc.Container([    
            html.Div([ html.Br() ]),
            html.H3('Coming Soon!')
        ]) 

@callback(
    Output("battery_metrics_figure", "figure"),
    Input("battery_brand_metrics", "value"),
    Input("battery_chemistry_metrics", "value"),
    Input("battery_x_axis_metrics", "value"),
    Input("battery_y_axis_metrics", "value"),
    Input("color-mode-switch", "value"), 
)  
def update_battery_metrics_figure(selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off):   
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
    fig_2 = generate_battery_spider_plot(Commercial_Batteries,bat_1,bat_2,bat_3,switch_off)  
    return fig_2  

@callback(
    Output("battery_map", "figure"),
    Input("battery_sector", "value"),
    Input("battery_type", "value"),
    Input("color-mode-switch", "value"), 
) 
def update_sector_map(sector,bat_type,switch_off): 
    technology_filename  = '..' + separator + 'Data' + separator + 'Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries','Battery_Research']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d     
    Battery_Research     = SAT_data['Battery_Research']    
    fig_3 = generate_battery_dev_map(Battery_Research,sector,bat_type,switch_off)  
    return fig_3 

@callback(
    Output("flight_ops_map", "figure"),
    Input("electric_aircraft_type", "value"),
    Input("electric_aircraft_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("electric_aircraft_system_voltage", "value"),
    Input("electric_aircraft_efficiency", "value"),
    Input("electric_aircraft_percent_adoption", "value"),
    Input("electric_aircraft_month", "value"),
    Input("color-mode-switch", "value"), 
)   
def update_flight_ops_map(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off): 
    fig_4 = generate_flight_ops_map(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off) 
    return fig_4 


@callback(
    Output("EX_flight_ops_map", "figure"),   
    Input("EX_TOGW", "value"),
    Input("EX_L_D", "value"),
    Input("EX_Max_Power", "value"),
    Input("EX_system_voltage", "value"), 
    Input("EX_battery_mass_fraction", "value"),
    Input("EX_aircraft_efficiency", "value"), 
    Input("EX_voltage", "value"),
    Input("EX_capacity", "value"),
    Input("EX_C_max", "value"),
    Input("EX_e0", "value"),
    Input("EX_temperature_range", "value"),     
    Input("EX_percent_adoption", "value"), 
    Input("EX_aircraft_month", "value"), 
    Input("color-mode-switch", "value"), 
)   
def update_flight_ops_map(EX_TOGW,EX_L_D,EX_Max_P,EX_system_V,EX_bat_frac,EX_eta,EX_cell_V,EX_capacity,EX_C_max,EX_e0,EX_Temp,EX_adoption,EX_month,switch_off):  
    fig_ex_4 = generate_EX_flight_ops_map(Routes_and_Temp,EX_TOGW,EX_L_D,EX_Max_P,EX_system_V,EX_bat_frac,EX_eta,EX_cell_V,EX_capacity,EX_C_max,EX_e0,EX_Temp,EX_adoption,EX_month,switch_off) 
    return fig_ex_4 
@callback(
    Output("US_bat_temperature_map", "figure"),
    Input("electric_aircraft_month", "value"),
    Input("color-mode-switch", "value"),
)
def update_US_bat_temperature_map(month_no,switch_off):
    filename           = '..' + separator + 'Data' + separator + 'Monthly_US_County_Temperature.xlsx'
    Temeperature_data  = pd.read_excel(filename,sheet_name=['US_County_Temperature_F'])  
    US_Temperature_F   = Temeperature_data['US_County_Temperature_F'] 
    fig_6              = generate_US_bat_temperature_map(US_Temperature_F,month_no,switch_off)  
    return fig_6  


@callback(
    Output("EX_us_temperature_map", "figure"),
    Input("EX_aircraft_month", "value"),
    Input("color-mode-switch", "value"),
)
def update_EX_bat_temperature_map(month_no,switch_off):
    filename           = '..' + separator + 'Data' + separator + 'Monthly_US_County_Temperature.xlsx'
    Temeperature_data  = pd.read_excel(filename,sheet_name=['US_County_Temperature_F'])  
    US_Temperature_F   = Temeperature_data['US_County_Temperature_F'] 
    fig_ex_6           = generate_US_EX_temperature_map(US_Temperature_F,month_no,switch_off)  
    return fig_ex_6   

@callback(
    Output("electric_aircraft_passenger_range", "figure"),
    Output("electric_aircraft_airports", "figure"),
    Output("electric_aircraft_market_size", "figure"),
    Output("electric_aircraft_yearly_emissions", "figure"),
    Input("electric_aircraft_type", "value"),
    Input("electric_aircraft_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("electric_aircraft_system_voltage", "value"),
    Input("electric_aircraft_efficiency", "value"),
    Input("electric_aircraft_percent_adoption", "value"),
    Input("electric_aircraft_month", "value"),
    Input("color-mode-switch", "value"), 
)   
def update_flight_ops_passenger_range_plot(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off): 
    fig_5, fig_6 ,fig_7,fig_8 = generate_electric_aircraft_flight_ops_meta_data(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off)     
    return fig_5, fig_6 ,fig_7,fig_8  
  
@callback(
    Output("EX_aircraft_passenger_range", "figure"),
    Output("EX_aircraft_airports", "figure"),
    Output("EX_aircraft_market_size", "figure"),
    Output("EX_aircraft_yearly_emissions", "figure"),  
    Input("EX_TOGW", "value"),
    Input("EX_L_D", "value"),
    Input("EX_Max_Power", "value"),
    Input("EX_system_voltage", "value"), 
    Input("EX_battery_mass_fraction", "value"),
    Input("EX_aircraft_efficiency", "value"), 
    Input("EX_voltage", "value"),
    Input("EX_capacity", "value"),
    Input("EX_C_max", "value"),
    Input("EX_e0", "value"),
    Input("EX_temperature_range", "value"),     
    Input("EX_percent_adoption", "value"), 
    Input("EX_aircraft_month", "value"), 
    Input("color-mode-switch", "value"), 
)   
def update_flight_ops_passenger_range_plot(EX_TOGW,EX_L_D,EX_Max_P,EX_system_V,EX_bat_frac,EX_eta,EX_cell_V,EX_capacity,EX_C_max,EX_e0,EX_Temp,EX_adoption,EX_month,switch_off):  
    fig_ex_5, fig_ex_6 ,fig_ex_7,fig_ex_8 = generate_EX_aircraft_flight_ops_meta_data(Routes_and_Temp,EX_TOGW,EX_L_D,EX_Max_P,EX_system_V,EX_bat_frac,EX_eta,EX_cell_V, EX_capacity,EX_C_max,EX_e0,EX_Temp,EX_adoption,EX_month,switch_off)  
    return fig_ex_5, fig_ex_6 ,fig_ex_7,fig_ex_8
  
    
if __name__ == "__main__":
    app.run_server(debug=True)
    
    