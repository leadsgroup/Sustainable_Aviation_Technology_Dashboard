from dash import html, dcc  
import dash_bootstrap_components as dbc 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_flight_ops_battery(Commercial_Batteries):
    flight_ops_battery = html.Div(
        [ 
            dbc.Label("Battery"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value        = Commercial_Batteries['Battery Name'][13],
                placeholder  = Commercial_Batteries['Battery Name'][13], 
                disabled     = False,
                style        = {'display': True, 'color': 'black'},
                id           ="flight_ops_battery",   
            ),
        ],
        className="mb-4", 
    )  
    return flight_ops_battery 
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_flight_ops_aircraft():
    flight_ops_aircraft = html.Div(
        [
            dbc.Label("Aircraft"),
            dcc.Dropdown(
                ["Boeing 737",'Airbus A320'],
                value = 'Boeing 737',
                placeholder = 'Boeing 737', 
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="aircraft_type",   
            ),
        ],
        className="mb-4",
    ) 
    return flight_ops_aircraft


def select_flight_ops_aircraft_battery_mass_fraction():
    
    battery_mass_fraction = html.Div(
        [
            dbc.Label("Battery Mass Fraction"),
            dcc.Slider(20, 100, 5,
                value= 50,
                id="battery_mass_fraction", 
            ),
        ],
        className="mb-4",
    )
    return  battery_mass_fraction

def select_flight_ops_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Fleet Adoption"),
            dcc.Slider(0, 100, 10,
                value=100,
                id="percent_fleet_adoption", 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption

def select_aircraft_system_voltage():
    system_voltage = html.Div(
        [
            dbc.Label("System Voltage"),
            dcc.Slider(400, 800, 50,
                value=600,
                id="powertrain_voltage", 
            ),
        ],
        className="mb-4",
    ) 
    return system_voltage

def select_propulsive_efficiency():
    propulsive_efficiency = html.Div(
        [
            dbc.Label("Propulsive Efficiency"),
            dcc.Slider(50, 100, 5,
                value=95,
                id="efficiency", 
            ),
        ],
        className="mb-4",
    )  
    return propulsive_efficiency

def select_flight_ops_time_of_year(US_Temperature_F):
    
    battery_dev_year = html.Div(
        [
            dbc.Label("Month"), 
            dcc.Slider(0, 11, 1,
                value=4, 
                marks = {
                    0:{'label': "Jan"},
                    1:{'label': "Feb"}, 
                    2:{'label': "Mar"},  
                    3:{'label': "Apr"}, 
                    4:{'label': "May"},
                    5:{'label': "Jun"},
                    6:{'label': "Jul"},
                    7:{'label': "Aug"}, 
                    8:{'label': "Sep"},  
                    9:{'label': "Oct"}, 
                    10:{'label': "Nov"}, 
                    11:{'label': "Dec"},                    
                 },
                id="month",
            ),
        ],
        className="mb-4",
    )
    return  battery_dev_year
