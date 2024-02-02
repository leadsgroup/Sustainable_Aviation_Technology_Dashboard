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
            dbc.Label("Select Battery Mass Fraction"),
            dcc.RangeSlider(
                2000,
                2024, 
                1,
                id="battery_mass_fraction",
                marks={i: '{}'.format(i) for i in range(2000,2025,5)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[2000, 2024], 
            ),
        ],
        className="mb-4",
    )
    return  battery_mass_fraction

def select_flight_ops_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Select % Fleet Adoption"),
            dcc.RangeSlider(
                2000,
                2024, 
                1,
                id="fleet_adoption",
                marks={i: '{}'.format(i) for i in range(2000,2025,5)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[2000, 2024], 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption


def select_flight_ops_time_of_year():
    
    battery_dev_year = html.Div(
        [
            dbc.Label("Select Month Range"),
            dcc.RangeSlider(
                2000,
                2024, 
                1,
                id="time_of_year_slider",
                marks={i: '{}'.format(i) for i in range(2000,2025,5)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[2000, 2024], 
            ),
        ],
        className="mb-4",
    )
    return  battery_dev_year
