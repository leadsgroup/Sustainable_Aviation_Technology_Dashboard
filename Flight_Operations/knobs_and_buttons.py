from dash import html, dcc  
import dash_bootstrap_components as dbc 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_flight_ops_battery_brand_panel_1():
    flight_ops_battery_brand = html.Div(
        [
            dbc.Label("Select Battery Brand"),
            dcc.Dropdown(
                ["gdpPercap", "lifeExp", "pop"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="flight_ops_battery_brand_dropdown",   
            ),
        ],
        className="mb-4",
    ) 
    return flight_ops_battery_brand

def select_flight_ops_battery_chemistry_panel_1():
    flight_ops_battery_chemistry = html.Div(
        [
            dbc.Label("Select Battery Chemistry"),
            dcc.Dropdown(
                ["gdpPefrcap", "lifreExp", "pfop"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="flight_ops_battery_chemistry_dropdown",   
            ),
        ],
        className="mb-4",
    ) 
    return flight_ops_battery_chemistry


def select_flight_ops_battery_model_panel_1():
    flight_ops_battery_model = html.Div(
        [
            dbc.Label("Select Battery Model"),
            dcc.Dropdown(
                ["gdpPefrcap", "lifreExp", "pfop"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="flight_ops_battery_model_dropdown",   
            ),
        ],
        className="mb-4",
    ) 
    return flight_ops_battery_model
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_flight_ops_aircraft():
    flight_ops_aircraft = html.Div(
        [
            dbc.Label("Select Aircraft"),
            dcc.Dropdown(
                ["gdpPercap", "lifeExp", "pop"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="flight_ops_aircraft_dropdown",   
            ),
        ],
        className="mb-4",
    ) 
    return flight_ops_aircraft


def select_flight_ops_aircraft_battery_mass_fraction():
    
    battery_mass_fraction = html.Div(
        [
            dbc.Label("Select % Battery Mass Fraction"),
            dcc.Slider(0, 100, 10,
                value=20,
                id="battery_mass_fraction", 
            ),
        ],
        className="mb-4",
    )
    return  battery_mass_fraction

def select_flight_ops_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Select % Fleet Adoption"),
            dcc.Slider(0, 100, 10,
                value=50,
                id="battery_fleet", 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption


def select_flight_ops_time_of_year():
    
    battery_dev_year = html.Div(
        [
            dbc.Label("Select Month"), 
            dcc.Slider(0, 11, 1,
                value=6, 
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
