
from . import * 

def generate_flight_ops_aircraft_panel(): 
    flight_ops_aircraft                             = select_flight_ops_aircraft()   
    flight_ops_aircraft_battery_mass_fraction       = select_flight_ops_aircraft_battery_mass_fraction()   
    flight_ops_time_of_year                         = select_flight_ops_time_of_year()
    flight_ops_fleet_adoption                       = select_flight_ops_fleet_adoption() 
    flight_ops_battery_brand_panel_1               = select_flight_ops_battery_brand_panel_1()
    flight_ops_battery_chemistry_panel_1           = select_flight_ops_battery_chemistry_panel_1()
    flight_ops_battery_model_panel_1               = select_flight_ops_battery_model_panel_1()
    
    flight_ops_aircraft_panel = dbc.Card([flight_ops_aircraft,
                                        flight_ops_battery_brand_panel_1,
                                        flight_ops_battery_chemistry_panel_1,
                                        flight_ops_battery_model_panel_1,
                                        flight_ops_aircraft_battery_mass_fraction,
                                        flight_ops_fleet_adoption,
                                        flight_ops_time_of_year],body=True,)   
    return  flight_ops_aircraft_panel
 