from dash import html, dcc  
import dash_bootstrap_components as dbc 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_brand_panel_1():
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
                id="battery_brand_dropdown_p1",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_brand

def select_battery_chemistry_panel_1():
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
                id="battery_chemistry_dropdown_p1",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_chemistry

def select_battery_x_axis_panel_1():
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
                id="battery_x_axis_dropdown_p1",   
            ),
        ],
        className="mb-4",
    ) 
    
    return battery_x_axis 


def select_battery_y_axis_panel_1():
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
                id="battery_y_axis_dropdown_p1",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_y_axis

def select_battery_dev_year_panel_1():
    
    battery_dev_year = html.Div(
        [
            dbc.Label("Select Year Range"),
            dcc.RangeSlider(
                2000,
                2024, 
                1,
                id="battery_dev_year_slider_p1",
                marks={i: '{}'.format(i) for i in range(2000,2025,5)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[2000, 2024], 
            ),
        ],
        className="mb-4",
    )
    return  battery_dev_year


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_1_panel_2():
    battery  = html.Div(
        [
            dbc.Label("Select Battery"),
            dcc.Dropdown(
                ["gdpP2ercap", "li2feExp", "p3op"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="select_battery_1_dropdown_p2",   
            ),
        ],
        className="mb-4",
    ) 
    return battery    

def select_battery_2_panel_2():
    battery  = html.Div(
        [
            dbc.Label("Select Battery"),
            dcc.Dropdown(
                ["gdpP2ercap", "li2feExp", "p3op"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="select_battery_2_dropdown_p2",   
            ),
        ],
        className="mb-4",
    ) 
    return battery   

def select_battery_3_panel_2():
    battery  = html.Div(
        [
            dbc.Label("Select Battery"),
            dcc.Dropdown(
                ["gdpP2ercap", "li2feExp", "p3op"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="select_battery_3_dropdown_p2",   
            ),
        ],
        className="mb-4",
    ) 
    return battery   

def select_battery_4_panel_2():
    battery  = html.Div(
        [
            dbc.Label("Select Battery"),
            dcc.Dropdown(
                ["gdpP2ercap", "li2feExp", "p3op"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="select_battery_4_dropdown_p2",   
            ),
        ],
        className="mb-4",
    ) 
    return battery   

def select_battery_5_panel_2():
    battery  = html.Div(
        [
            dbc.Label("Select Battery"),
            dcc.Dropdown(
                ["gdpP2ercap", "li2feExp", "p3op"],
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="select_battery_5_dropdown_p2",   
            ),
        ],
        className="mb-4",
    ) 
    return battery   

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 3 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_brand_panel_3():
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
                id="battery_brand_dropdown_p3",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_brand

def select_battery_chemistry_panel_3():
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
                id="battery_chemistry_dropdown_p3",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_chemistry
 
def select_battery_dev_year_panel_3():
    
    battery_dev_year = html.Div(
        [
            dbc.Label("Select Year Range"),
            dcc.RangeSlider(
                2000,
                2024, 
                1,
                id="battery_dev_year_slider_p3",
                marks={i: '{}'.format(i) for i in range(2000,2025,5)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[2000, 2024], 
            ),
        ],
        className="mb-4",
    )
    return  battery_dev_year
