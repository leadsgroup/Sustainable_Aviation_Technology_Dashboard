from dash import html, dcc  
import dash_bootstrap_components as dbc 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_brand_metrics(Commercial_Batteries):
    All = ['All']
    brand_list = All + list(Commercial_Batteries['Brand'][1:].unique())
    battery_brand = html.Div(
        [
            dbc.Label("Select Battery Brand"),
            dcc.Dropdown(brand_list,
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="battery_brand_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_brand

def select_battery_chemistry_metrics(Commercial_Batteries): 
    All = ['All']
    chemistry_list = All + list(Commercial_Batteries['Chemistry'][1:].unique())
    battery_chemistry = html.Div(
        [
            dbc.Label("Select Battery Chemistry"),
            dcc.Dropdown(chemistry_list,
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="battery_chemistry_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_chemistry

def select_battery_x_axis_metrics(Commercial_Batteries): 
    battery_x_axis = html.Div(
        [
            dbc.Label("X-Axis"),
            dcc.Dropdown(list(Commercial_Batteries.columns.values)[4:18],
                value = list(Commercial_Batteries.columns.values)[4:18][7],
                placeholder = 'Select Indicator',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="battery_x_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    
    return battery_x_axis 


def select_battery_y_axis_metrics(Commercial_Batteries):
    battery_y_axis = html.Div(
        [
            dbc.Label("Y-Axis"),
            dcc.Dropdown(list(Commercial_Batteries.columns.values)[4:18],
                value = list(Commercial_Batteries.columns.values)[4:18][9],
                placeholder = 'Select Indicator',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="battery_y_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_y_axis
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_1(Commercial_Batteries): 
    battery_1_selection  = html.Div(
        [  
            dbc.Label("Select Battery Cell 1"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value       = list(Commercial_Batteries['Battery Name'][1:].unique())[17],
                placeholder = 'Select Battery',
                clearable   = True,
                disabled    = False,
                style       = {'display': True, 'color': 'black'},
                id          = "battery_1",   
            ),
        ],
        className="mb-4", 
    ) 
    return battery_1_selection 

def select_battery_2(Commercial_Batteries):
    battery_2_selection   = html.Div(
        [ 
            dbc.Label("Select Battery Cell 2"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value        = list(Commercial_Batteries['Battery Name'][1:].unique())[8],
                placeholder  = 'Select Battery',
                clearable    = True,
                disabled     = False,
                style        = {'display': True, 'color': 'black'},
                id           ="battery_2",   
            ),
        ],
        className="mb-4", 
    ) 
    return battery_2_selection 

def select_battery_3(Commercial_Batteries):
    battery_3_selection   = html.Div(
        [ 
            dbc.Label("Select Battery Cell 3"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value        = list(Commercial_Batteries['Battery Name'][1:].unique())[0],
                placeholder  = 'Select Battery',
                clearable    = True,
                disabled     = False,
                style        = {'display': True, 'color': 'black'},
                id           ="battery_3",   
            ),
        ],
        className="mb-4", 
    ) 
    return battery_3_selection 
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 3 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_industry_dev_panel(Battery_Research):
    All = ['All']
    sector_list = All + list(Battery_Research['Sector'][1:].unique())
    battery_industry = html.Div(
        [
            dbc.Label("Select Sector"), 
            dcc.Dropdown(sector_list,
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="battery_sector",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_industry

def select_battery_type_dev_panel(Battery_Research): 
    type_list =  ['All','Li-Ion','Li-Sulphur','Metal-Air','Li-Silicon']
    battery_type = html.Div(
        [
            dbc.Label("Select Battery Type"),
            dcc.Dropdown(type_list,
                value = 'All',
                placeholder = 'All',
                clearable = True,
                disabled = False,
                style = {'display': True, 'color': 'black'},
                id="battery_type",
            ),
        ],
        className="mb-4",
    ) 
    return battery_type