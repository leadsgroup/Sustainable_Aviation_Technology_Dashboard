"""Sustainable Aviation Technology Dashboard
"""

from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates                  import load_figure_template 
import pandas as pd 
#from Energy_X.figures                          import *
#from Energy_X.knobs_and_buttons                import * 
#from Energy_X.control_panels                   import * 
from Flight_Operations.figures                 import *
from Flight_Operations.knobs_and_buttons       import * 
from Flight_Operations.control_panels          import * 
from Batteries.figures                   import * 
from Batteries.knobs_and_buttons         import * 
from Batteries.control_panels            import * 

# Deployment 
# https://www.youtube.com/watch?v=XWJBJoV5yww&t=0s&ab_channel=CharmingData 
# *** to remove ****  

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------------------------------------------------------------------------------

technology_filename  = 'Data/Technology_Data.xlsx'
SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries','Battery_Research']) 
Commercial_Batteries = SAT_data['Commercial_Batteries'] 
a                    = Commercial_Batteries['Brand']  
b                    = Commercial_Batteries['Chemistry']
c                    = Commercial_Batteries['Model']
d                    = a + ': ' + b + '-' + c 
Commercial_Batteries["Battery Name"] = d     
Battery_Research     = SAT_data['Battery_Research'] 
a                    = Commercial_Batteries['Brand']  
b                    = Commercial_Batteries['Chemistry']
c                    = Commercial_Batteries['Model']
d                    = a + ': ' + b + '-' + c 
Commercial_Batteries["Battery Name"] = d        



route_temp_filename  = 'Data/American_Airlines_Monthly_Temp.xlsx'
Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
Routes_and_Temp      = Routes_and_Temp['Sheet1'] 


temperature_filename = 'Data/Monthly_US_County_Temperature.xlsx'
Temeperature_data    = pd.read_excel(temperature_filename,sheet_name=['US_County_Temperature_F'])  
US_Temperature_F     = Temeperature_data['US_County_Temperature_F'] 
image_path           = 'Data/LEADS_logo_rectangle_nbg.png'
 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Control Panels 
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Energy X

  
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
app = Dash(__name__,external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)
 
# Template  colors 
primary_color     = '#78c2ad' 
secondary_color   = '#f3969a'  
backround         = '#212529'
success_color     = '#56cc9d'
info_color        = '#6cc3d5'
light_color       = '#f8f9fa'
warning_color     = '#fdce67'
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
    'backgroundColor': success_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


tab_selected_style_3 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': success_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


tab_selected_style_4 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': success_color,
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
                 html.Plaintext( children= 'Developed by the Lab for Electric Aircraft Design and Sustainablity (LEADS) at the University of Illinois,', id= "header_part_1",), 
                 html.Plaintext( children= 'Urbana-Champaign, the Sustainable Aviation Technology Dashboard is a place to evaluate and examine the ', id= "header_part_2",), 
                 html.Plaintext( children= 'integration of existing technologies onto future aircraft platforms.', id= "header_part_3",), 
                 ],body=True)  
             ],  width=10),  
         dbc.Col([ ],  width=1),  
         html.Div([ html.Br() ]),   
        ]),  
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Energy-X', value='tab-1', style=tab_style, selected_style=tab_selected_style_4),
        dcc.Tab(label='Electrification', value='tab-2', style=tab_style, selected_style=tab_selected_style_1),
        dcc.Tab(label='Sustainable Aviation Fuel', value='tab-3', style=tab_style, selected_style=tab_selected_style_2),
        dcc.Tab(label='Hydrogen', value='tab-4', style=tab_style, selected_style=tab_selected_style_3),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline'), 
    html.Div([    html.Br() ]),    
    html.Div(["Contact Us"], className="bg-success text-white h2 p-2"),
    dbc.Row([ 
         dbc.Col([ ],  width=1),
         dbc.Col([ 
             dbc.Card([   
                 html.Plaintext( children= 'Kindly direct any questions to Prof. Matthew Clarke by sending an email to maclarke@illinois.edu.', id= "tail_part_1",), 
                 html.Plaintext( children= 'Contribute to the Dashboard by sending us information on new commercial batteries or batteries ', id= "tail_part_2",), 
                 html.Plaintext( children= 'under development at high TRL levels (i.e. TRL > 8).', id= "tail_part_3",), 
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
            html.Div([ html.Br() ]),
            html.H3('Test 2')
        ])
    elif tab == 'tab-2':
        return  dbc.Container([    
            html.Div([ html.Br() ]),      
            html.Div(["Commercial Battery Metric Analysis"], className="bg-primary text-white h5 p-2"),
            dbc.Row([ dbc.Col([battery_metrics_panel  ],  width=4),  
                      dbc.Col([ dcc.Graph(id ="battery_metrics_figure", className="border-0 bg-transparent")],  width=8),
                    ]),
            html.Div([    html.Br() ]),
            html.Div(["Commercial Battery Cell Comparison"], className="bg-primary text-white h5 p-2"),   
            dbc.Row([   
                      dbc.Col([battery_comparison_panel],  width=4),    
                      dbc.Col([ dcc.Graph(id="battery_spider_plot", className="border-0 bg-transparent")],  width=8),
                    ]),           
        
            html.Div(["Worldwide Battery Cell Development"], className="bg-primary text-white h5 p-2"),    
            dbc.Row([dbc.Col([battery_development_panel  ],  width=4),   
                dbc.Col([ dcc.Graph(id="battery_map", className="border-0 bg-transparent")],  width=8),
                ]),  
            html.Div([    html.Br() ]),             
            html.Div(["Airline Flight Operations"], className="bg-primary text-white h5 p-2"), 
            dbc.Row([  dbc.Col([battery_flight_ops_aircraft_panel ],  width=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Feasible Routes"], className="text-sm-center h4"),
                       dcc.Graph(id="flight_ops_map", className="border-0 bg-transparent"), 
                       html.Div([    html.Br() ]),
                       html.Div(["Average Monthly Temperature (deg. F)"], className="text-sm-center h4"),
                       dcc.Graph(id="us_temperature_map", className="border-0 bg-transparent")                       
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=8),                
                
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Airline Meta Data"], className="bg-primary text-white h5 p-2"),    
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Travel Distances"], className="text-sm-center h4"),  
                       dcc.Graph(id="passenger_range_plot", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Electrified Airports"], className="text-sm-center h4"),  
                       dcc.Graph(id="airport_electrification", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                
                
                ]), 
            html.Div([    html.Br() ]),  
            html.Div(["Airline and Airport Techno-economics"], className="bg-primary text-white h5 p-2"),        
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Electric Aircraft Market Analysis"], className="text-sm-center h4"),  
                       dcc.Graph(id="market_analysis_plot", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Monthly Emissions"], className="text-sm-center h4"),  
                       dcc.Graph(id="monthly_emissions", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  width=6),                
                
                ]),    
        ])
    
    elif tab == 'tab-3':
        return dbc.Container([    
            html.Div([ html.Br() ]),
            html.H3('Comming Soon!')
        ])
    elif tab == 'tab-4':
        return dbc.Container([    
            html.Div([ html.Br() ]),
            html.H3('Comming Soon!')
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
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries'])      
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
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries'])  
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d       
    fig_2 = generate_battery_spider_plot(Commercial_Batteries,bat_1,bat_2,bat_3,switch_off)  
    return fig_2  

@callback(
    Output("battery_map", "figure"),
    Input("battery_sector", "value"),
    Input("battery_type", "value"),
    Input("color-mode-switch", "value"),
) 
def update_sector_map(sector,bat_type,switch_off):
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Battery_Research'])  
    Battery_Research = SAT_data['Battery_Research'] 
    fig_3 = generate_battery_dev_map(Battery_Research,sector,bat_type,switch_off)  
    return fig_3 

@callback(
    Output("flight_ops_map", "figure"),
    Input("aircraft_type", "value"),
    Input("flight_ops_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("powertrain_voltage", "value"),
    Input("efficiency", "value"),
    Input("percent_fleet_adoption", "value"),
    Input("month", "value"),
    Input("color-mode-switch", "value"),
)   
def update_flight_ops_map(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off):
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d      
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d    
    route_temp_filename  = 'Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1']     
    fig_4 = generate_flight_ops_map(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off) 
    return fig_4

@callback(
    Output("passenger_range_plot", "figure"),
    Input("aircraft_type", "value"),
    Input("flight_ops_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("powertrain_voltage", "value"),
    Input("efficiency", "value"),
    Input("percent_fleet_adoption", "value"),
    Input("month", "value"),
    Input("color-mode-switch", "value"),
)   
def update_flight_ops_passenger_range_plot(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off):
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d      
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d    
    route_temp_filename  = 'Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1']     
    fig_5 = generate_flight_ops_passenger_range_plot(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off) 
    return fig_5 


@callback(
    Output("airport_electrification", "figure"),
    Input("aircraft_type", "value"),
    Input("flight_ops_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("powertrain_voltage", "value"),
    Input("efficiency", "value"),
    Input("percent_fleet_adoption", "value"),
    Input("month", "value"),
    Input("color-mode-switch", "value"),
)   
def update_flight_ops_passenger_range_plot(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off):
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d      
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d    
    route_temp_filename  = 'Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1']     
    fig_6 = generate_flight_ops_airport_electrification(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off) 
    return fig_6  


@callback(
    Output("market_analysis_plot", "figure"),
    Input("aircraft_type", "value"),
    Input("flight_ops_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("powertrain_voltage", "value"),
    Input("efficiency", "value"),
    Input("percent_fleet_adoption", "value"),
    Input("month", "value"),
    Input("color-mode-switch", "value"),
)   
def update_flight_ops_market_analysis_plot(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off):
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d      
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d    
    route_temp_filename  = 'Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1']     
    fig_7 = generate_flight_ops_market_analysis(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off) 
    return fig_7 


@callback(
    Output("monthly_emissions", "figure"),
    Input("aircraft_type", "value"),
    Input("flight_ops_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("powertrain_voltage", "value"),
    Input("efficiency", "value"),
    Input("percent_fleet_adoption", "value"),
    Input("month", "value"),
    Input("color-mode-switch", "value"),
)   
def update_battery_flight_ops_monthly_emissions_plot(aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off):
    technology_filename  = 'Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d      
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d    
    route_temp_filename  = 'Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1']     
    fig_8 = generate_flight_ops_monthly_emissions(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off) 
    return fig_8  

@callback(
    Output("us_temperature_map", "figure"),
    Input("month", "value"),
    Input("color-mode-switch", "value"),
)
def update_us_temperature_map(month_no,switch_off):
    filename           = 'Data/Monthly_US_County_Temperature.xlsx'
    Temeperature_data  = pd.read_excel(filename,sheet_name=['US_County_Temperature_F'])  
    US_Temperature_F   = Temeperature_data['US_County_Temperature_F'] 
    fig_6              = generate_us_temperature_map(US_Temperature_F,month_no,switch_off)  
    return fig_6 
 
 
if __name__ == "__main__":
    app.run_server(debug=True)
    
    