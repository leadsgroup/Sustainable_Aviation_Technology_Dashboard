from dash import html, dcc  
import dash_bootstrap_components as dbc 


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Energy X Control Panel 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  


def select_flight_ops_BDL_aircraft_L_D():
    L_D  = html.Div(
        [
            dbc.Label("Lift-to-Drag Ratio"),
            dcc.Slider(12,20, 1,
                value= 16,
                id="EX_L_D", 
            ),
        ],
        className="mb-4",
    )
    return L_D

def select_flight_ops_BDL_aircraft_weight():
    
    W0  = html.Div(
        [
            dbc.Label("Takeoff Gross Weight (lbs)"),
            dcc.Slider(100000,200000, 20000,
                value= 160000,
                id="EX_TOGW", 
            ),
        ],
        className="mb-4",
    )
    return W0

def select_BDL_aircraft_max_power():
    
    P_max = html.Div(
        [
            dbc.Label("Max Power (MW)"),
            dcc.Slider(5, 35, 5,
                value= 15,
                id="EX_Max_Power", 
            ),
        ],
        className="mb-4",
    )
    return P_max 

def select_BDL_max_cell_voltage():
    
    voltage = html.Div(
        [
            dbc.Label("Nominal Voltage (V)"),
            dcc.Slider(2, 5, 0.5,
                value= 4,
                id="EX_voltage", 
            ),
        ],
        className="mb-4",
    )
    return voltage 

def select_BDL_max_cell_capacity():
    
    capacity = html.Div(
        [
            dbc.Label("Capacity (mAh)"),
            dcc.Slider(3000, 5000, 500,
                value= 4000,
                id="EX_capacity", 
            ),
        ],
        className="mb-4",
    )
    return capacity

def select_BDL_max_cell_max_C():
    
    C_max = html.Div(
        [
            dbc.Label("Max C-Rate"),
            dcc.Slider(3, 15, 1,
                value= 9,
                id="EX_C_max", 
            ),
        ],
        className="mb-4",
    )
    return C_max


def select_BDL_specific_energy(): 
    
    e_0 = html.Div(
        [
            dbc.Label("Specific Energy (Wh/kg)"),
            dcc.Slider(200, 1000, 100,
                value= 600,
                id="EX_e0", 
            ),
        ],
        className="mb-4",
    )
    return e_0


def select_BDL_temperature_range(): 
    Temp = html.Div(
        [
            dbc.Label("Operating Temperature (F)"),
            dcc.RangeSlider(0, 100, 10,
                            value=[10, 80],
                            id='EX_temperature_range'
                            ), 
        ],
        className="mb-4",
    )
    return Temp


def select_flight_ops_BDL_batt_mass_frac():
    
    battery_mass_fraction = html.Div(
        [
            dbc.Label("Battery Mass Fraction"),
            dcc.Slider(10, 100, 10,
                value= 50,
                id="EX_battery_mass_fraction", 
            ),
        ],
        className="mb-4",
    )
    return  battery_mass_fraction

def select_flight_ops_BDL_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Fleet Adoption"),
            dcc.Slider(0, 100, 10,
                value=100,
                id="EX_percent_adoption", 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption

def select_BDL_system_voltage():
    system_voltage = html.Div(
        [
            dbc.Label("System Voltage (V)"),
            dcc.Slider(400, 800, 50,
                value=600,
                id="EX_system_voltage", 
            ),
        ],
        className="mb-4",
    ) 
    return system_voltage

def select_BDL_propulsive_efficiency():
    propulsive_efficiency = html.Div(
        [
            dbc.Label("Propulsive Efficiency"),
            dcc.Slider(50, 100, 5,
                value=95,
                id="EX_aircraft_efficiency", 
            ),
        ],
        className="mb-4",
    )  
    return propulsive_efficiency

def select_flight_ops_month_BDL(US_Temperature_F):
    
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
                id="EX_aircraft_month",
            ),
        ],
        className="mb-4",
    )
    return  battery_dev_year
