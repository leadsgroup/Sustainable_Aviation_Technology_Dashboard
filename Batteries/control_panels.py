
from . import * 

def generate_battery_metrics_panel():  
    
    battery_brand_panel_1      = select_battery_brand_panel_1()
    battery_chemistry_panel_1  = select_battery_chemistry_panel_1()
    battery_x_axis_panel_1     = select_battery_x_axis_panel_1()   
    battery_y_axis_panel_1     = select_battery_y_axis_panel_1()   
    #battery_dev_year_panel_1   = select_battery_dev_year_panel_1()     

    battery_metrics_panel = dbc.Card([battery_brand_panel_1,
                                        battery_chemistry_panel_1,
                                        battery_x_axis_panel_1,
                                        battery_y_axis_panel_1,
                                        #battery_dev_year_panel_1
                                        ],body=True,)

    return battery_metrics_panel

 

def generate_battery_1_properties_panel():

    battery_1_brand      = select_battery_1_brand()
    battery_1_chemistry  = select_battery_1_chemistry()
    battery_1_model      = select_battery_1_model()  
    battery_1_control_panel = dbc.Card([battery_1_brand,battery_1_chemistry,battery_1_model], body=True,) 
    
    return battery_1_control_panel 
 
def generate_battery_2_properties_panel():

    battery_2_brand      = select_battery_2_brand()
    battery_2_chemistry  = select_battery_2_chemistry()
    battery_2_model      = select_battery_2_model()  
    battery_2_control_panel = dbc.Card([battery_2_brand,battery_2_chemistry,battery_2_model], body=True,) 
    
    return battery_2_control_panel 


def generate_battery_3_properties_panel():

    battery_3_brand      = select_battery_3_brand()
    battery_3_chemistry  = select_battery_3_chemistry()
    battery_3_model      = select_battery_3_model()  
    battery_3_control_panel = dbc.Card([battery_3_brand,battery_3_chemistry,battery_3_model], body=True,) 
    
    return battery_3_control_panel 


 
def generate_battery_control_panel_3():  
    
    battery_industry_panel_3  = select_battery_industry_panel_3()
    battery_type_panel_3      = select_battery_type_panel_3()      
    battery_control_panel_3   = dbc.Card([battery_industry_panel_3,
                                        battery_type_panel_3],body=True,)

    return battery_control_panel_3 