
from . import * 

def generate_battery_metrics_panel(Commercial_Batteries):  
    
    battery_brand_metrics      = select_battery_brand_metrics(Commercial_Batteries)
    battery_chemistry_metrics  = select_battery_chemistry_metrics(Commercial_Batteries)
    battery_x_axis_metrics     = select_battery_x_axis_metrics(Commercial_Batteries)   
    battery_y_axis_metrics     = select_battery_y_axis_metrics(Commercial_Batteries)     

    battery_metrics_panel = dbc.Card([battery_brand_metrics,
                                        battery_chemistry_metrics,
                                        battery_x_axis_metrics,
                                        battery_y_axis_metrics, 
                                        ],body=True,)

    return battery_metrics_panel

def generate_battery_comparison_panel(Commercial_Batteries):

    battery_1_option         = select_battery_1(Commercial_Batteries) 
    battery_2_option         = select_battery_2(Commercial_Batteries) 
    battery_3_option         = select_battery_3(Commercial_Batteries) 
    battery_comparison_panel = dbc.Card([battery_1_option,battery_2_option,battery_3_option], body=True,) 
    
    return battery_comparison_panel   

 
def generate_battery_development_panel(Battery_Research):   
    battery_industry_dev_panel  = select_battery_industry_dev_panel(Battery_Research)
    battery_type_dev_panel      = select_battery_type_dev_panel(Battery_Research)      
    battery_development_panel   = dbc.Card([battery_industry_dev_panel,
                                        battery_type_dev_panel],body=True,)

    return battery_development_panel 