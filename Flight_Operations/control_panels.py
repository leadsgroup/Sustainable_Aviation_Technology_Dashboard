
from . import * 

def generate_flight_ops_aircraft_panel(Commercial_Batteries,US_Temperature_F): 
    flight_ops_aircraft                             = select_flight_ops_aircraft()   
    flight_ops_aircraft_battery_mass_fraction       = select_flight_ops_aircraft_battery_mass_fraction()   
    flight_ops_time_of_year                         = select_flight_ops_time_of_year(US_Temperature_F)
    flight_ops_fleet_adoption                       = select_flight_ops_fleet_adoption() 
    aircraft_system_voltage                         = select_aircraft_system_voltage() 
    propulsive_efficiency                           = select_propulsive_efficiency() 
    flight_ops_battery                              = select_flight_ops_battery(Commercial_Batteries) 
    
    flight_ops_aircraft_panel = dbc.Card([flight_ops_aircraft,
                                        flight_ops_battery, 
                                        flight_ops_aircraft_battery_mass_fraction,
                                        aircraft_system_voltage,
                                        propulsive_efficiency,
                                        flight_ops_fleet_adoption,
                                        flight_ops_time_of_year],body=True,)   
    return  flight_ops_aircraft_panel
 