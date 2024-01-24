
from . import * 

def generate_battery_control_panel_1():  
    
    battery_brand_panel_1      = select_battery_brand_panel_1()
    battery_chemistry_panel_1  = select_battery_chemistry_panel_1()
    battery_x_axis_panel_1     = select_battery_x_axis_panel_1()   
    battery_y_axis_panel_1     = select_battery_y_axis_panel_1()   
    battery_dev_year_panel_1   = select_battery_dev_year_panel_1()     

    battery_control_panel_1 = dbc.Card([battery_brand_panel_1,battery_chemistry_panel_1,battery_x_axis_panel_1,battery_y_axis_panel_1,battery_dev_year_panel_1],body=True,)

    return battery_control_panel_1


def generate_battery_control_panel_2():

    cell_1  = select_battery_1_panel_2()
    cell_2  = select_battery_2_panel_2()
    cell_3  = select_battery_3_panel_2()
    cell_4  = select_battery_4_panel_2()
    cell_5  = select_battery_5_panel_2()    

    battery_control_panel_2 = dbc.Card([cell_1,cell_2,cell_3,cell_4,cell_5], body=True,) 
    
    return battery_control_panel_2

 
def generate_battery_control_panel_3():  
    
    battery_brand_panel_3      = select_battery_brand_panel_3()
    battery_chemistry_panel_3  = select_battery_chemistry_panel_3() 
    battery_dev_year_panel_3   = select_battery_dev_year_panel_3()     

    battery_control_panel_3 = dbc.Card([battery_brand_panel_3,battery_chemistry_panel_3,battery_dev_year_panel_3],body=True,)

    return battery_control_panel_3 