import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *
import numpy as np           
import pandas as pd
from scipy.io import netcdf 
from  mpl_toolkits.basemap import Basemap
from urllib.request import urlopen
import json
import plotly.io as pio
import plotly.figure_factory as ff
from RCAIDE.Core import Units
import RCAIDE 
 

def main():
    battery_map()
    #market_plot()
    
    return 

def market_plot():
    
    technology_filename  = '../Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d      
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d    
    route_temp_filename  = '../Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1']     
    

    battery_choice = Commercial_Batteries['Battery Name'][13]
    
    month_no              = 1 
    aircraft              = 'Boeing 737'
    percent_adoption      = 100
    weight_fraction       = 35
    propulsive_efficiency = 90
    switch_off            = False 
    system_voltage        = 400
        
    generate_flight_ops_map(Routes_and_Temp,Commercial_Batteries,battery_choice,aircraft,system_voltage,propulsive_efficiency,
                                weight_fraction,percent_adoption,month_no,switch_off)    
    return 
    
    

def generate_flight_ops_map(Routes_and_Temp,Commercial_Batteries,battery_choice,aircraft,system_voltage,propulsive_efficiency,
                            weight_fraction,percent_adoption,month_no,switch_off): 
    mapbox_access_token  = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    map_style            = None if switch_off else 'dark'  
    #template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]     
    
    if aircraft == "Boeing 737": 
        P_max           = 15000000 
        W_0             = 79015.8  
        L_div_D         = 15.452 
    elif aircraft == 'Airbus A320': 
        P_max           = 15000000 
        W_0             = 78000
        L_div_D         = 15.452         
        
    Wh_per_kg_to_J  = 3600.0
    Ah_to_C         = 3600.0  
    V_bat           = system_voltage
    eta_0           = propulsive_efficiency/100 

    # ----------------------------------------------------------------------------------     
    # Compute Range
    # ----------------------------------------------------------------------------------  
    
    month_names     = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']      
    month           =  month_names[month_no] 
    data            = Commercial_Batteries[Commercial_Batteries['Battery Name'] == battery_choice] 
    V_cell          = np.array(data['Nominal Voltage (V)'])[0]
    e_cell          = np.array(data['Gravimetric Energy Density (Wh/kg)'])[0] *Wh_per_kg_to_J
    q_cell          = np.array(data['Capacity (mAh)'])[0]/1000 * Ah_to_C  # conversion to coulombs
    i_max           = np.array(data['Maximum Discharge Current (A)'])[0]  # amps   
    Min_Temp        = np.array(data['Minimum Disharge Temperature (°C)'])[0] *9/5 + 32
    Max_Temp        = np.array(data['Maximum Discharge Temperature (°C)'])[0] *9/5 + 32
     
    #================================================================================================================================================
    
    I_bat           = P_max/ V_bat
    n_series        = V_bat/V_cell
    W_bat           = (weight_fraction/100 ) * W_0
    E_bat           = W_bat * e_cell  
    Q_bat           = E_bat /V_bat
    n_parallel      = Q_bat/q_cell 
    n_parallel_min  = I_bat/i_max 
    
    if n_parallel_min  <  n_parallel: 
        Range    = (e_cell/9.81) * L_div_D * (weight_fraction/100 ) * eta_0
    else:  
        Range = 0 
    
             
    # ----------------------------------------------------------------------------------     
    # Compute distance between departure and destimation points
    # ----------------------------------------------------------------------------------
    Routes_and_Temp_Mo           = Routes_and_Temp.loc[Routes_and_Temp['Month'] == month_no+1 ]  
    des_lon                      = np.array(Routes_and_Temp_Mo['Destination Longitude (Deg.)'])
    des_lat                      = np.array(Routes_and_Temp_Mo['Destination Latitude (Deg.)'])
    org_lon                      = np.array(Routes_and_Temp_Mo['Origin Longitude (Deg.)'])
    org_lat                      = np.array(Routes_and_Temp_Mo['Origin Latitude (Deg.)']) 
    origin_coordinates           = np.stack((des_lat,des_lon))
    destination_coordinates      = np.stack((org_lat, org_lon)) 
    R                            = 6371.0088*1000 
    coord0_rad                   = origin_coordinates*0.017453292519943295
    coord1_rad                   = destination_coordinates*0.017453292519943295
    angles                       = np.arccos(np.sin(coord0_rad[0,:])*np.sin(coord1_rad[0,:]) + 
                                            np.cos(coord0_rad[0,:])*np.cos(coord1_rad[0,:])*np.cos(coord0_rad[1,:] - coord1_rad[1,:]))
    distance                     = R*angles 
    Routes_and_Temp_Mo['Range']  = distance.tolist()
   
    # Filer List By Distance and Temperature   
    Infeasible_Routes_1          =Routes_and_Temp_Mo[Routes_and_Temp_Mo['Range'] > Range ]  
    Feasible_Routes_1            =Routes_and_Temp_Mo[Routes_and_Temp_Mo['Range'] < Range ] 
    Feasible_Routes_2            = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] > Min_Temp] 
    Infeasible_Routes_2          = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] < Min_Temp] 
    Feasible_Routes_3            = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] < Max_Temp] 
    Infeasible_Routes_3          = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] > Max_Temp]  
    Feasible_Routes_4            = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] > Min_Temp] 
    Infeasible_Routes_4          = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] < Min_Temp] 
    Feasible_Routes_5            = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] < Max_Temp] 
    Infeasible_Routes_5          = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] > Max_Temp]
    
    Infeasible_Routes_6          = Feasible_Routes_5.tail(int(len(Feasible_Routes_5)*(100 - percent_adoption)/100 ))
    Feasible_Routes              = Feasible_Routes_5.head(int(len(Feasible_Routes_5)*percent_adoption/100 ))
    
    # concatenate infeasible routes 
    Infeasible_Routes =  pd.concat([Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5,Infeasible_Routes_6])    
    
    # ####################################################################################################
    # Routes 
    # ####################################################################################################
    
    
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    fig = go.Figure()
    airport_marker_size  = 5
    airport_marker_color = "white"

    # ----------------------------------------------------------------------------------
    # Flight Paths
    # ----------------------------------------------------------------------------------  

    lons       = np.empty(3 * len(Infeasible_Routes))
    lons[::3]  = Infeasible_Routes['Origin Longitude (Deg.)']
    lons[1::3] = Infeasible_Routes['Destination Longitude (Deg.)']
    lons[2::3] = None
    lats       = np.empty(3 * len(Infeasible_Routes))
    lats[::3]  = Infeasible_Routes['Origin Latitude (Deg.)']
    lats[1::3] = Infeasible_Routes['Destination Latitude (Deg.)']
    lats[2::3] = None    
  
    fig.add_trace(
        go.Scattergeo( 
            lon = lons,
            lat = lats,
            mode = 'lines',
            line = dict(width = 0.1,color = 'grey'),  
        )
    )
    
    
    lons       = np.empty(3 * len(Feasible_Routes))
    lons[::3]  = Feasible_Routes['Origin Longitude (Deg.)']
    lons[1::3] = Feasible_Routes['Destination Longitude (Deg.)']
    lons[2::3] = None
    lats       = np.empty(3 * len(Feasible_Routes))
    lats[::3]  = Feasible_Routes['Origin Latitude (Deg.)']
    lats[1::3] = Feasible_Routes['Destination Latitude (Deg.)']
    lats[2::3] = None    
  
    fig.add_trace(
        go.Scattergeo( 
            lon = lons,
            lat = lats,
            mode = 'lines',
            line = dict(width = 2,color = "aquamarine"), 
        )
    )

    

    # ----------------------------------------------------------------------------------
    # Airports 
    # ----------------------------------------------------------------------------------
    fig.add_trace(go.Scattergeo( 
        lon = Routes_and_Temp['Destination Longitude (Deg.)'],
        lat = Routes_and_Temp['Destination Latitude (Deg.)'],
        #hoverinfo = 'text',
        text = Routes_and_Temp['Destination City'],
        mode = 'markers',
        marker = dict(
            size = airport_marker_size,
            color = airport_marker_color, 
        ))) 

    fig.add_trace(go.Scattergeo( 
        lon = Routes_and_Temp['Origin Longitude (Deg.)'],
        lat = Routes_and_Temp['Origin Latitude (Deg.)'], 
        text = Routes_and_Temp['Origin City'],
        mode = 'markers',
        marker = dict(
            size = airport_marker_size,
            color = airport_marker_color, 
        )))

    
    # ----------------------------------------------------------------------------------
    # Flight Paths
    # ----------------------------------------------------------------------------------   
    fig.update_layout(mapbox_style  = "open-street-map",      
                      showlegend    = False, 
                      height        = 400, 
                      geo_scope     ='usa',
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      mapbox        = dict( accesstoken=mapbox_access_token,style=map_style,
                                            center=go.layout.mapbox.Center( lat=30, lon= 230 ))  )   
     

    #fig["layout"]["template"] = template
    
    fig.show()
        
    return 


def battery_map():
    
    technology_filename  = '../Data/Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries','Battery_Research']) 
    route_temp_filename  = '../Data/American_Airlines_Monthly_Temp.xlsx'
    Routes_and_Temp      = pd.read_excel(route_temp_filename,sheet_name=['Sheet1']) 
    Routes_and_Temp      = Routes_and_Temp['Sheet1'] 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d        
    map_style       = 'dark'
    
    
    battery_choice = Commercial_Batteries['Battery Name'][13]
    month_no       = 4
    month_names    = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']      
    month          =  month_names[month_no]
    percent_adoption = 100
    
    font_size       = 16
    Wh_per_kg_to_J  = 3600.0
    Ah_to_C         = 3600.0
    data            = Commercial_Batteries.loc[Commercial_Batteries['Battery Name'] == battery_choice] 
    V_cell          = np.array(data['Nominal Voltage (V)'])
    e_cell          = 1000 *Wh_per_kg_to_J # np.array(data['Gravimetric Energy Density (Wh/kg)'])[0] *Wh_per_kg_to_J
    q_cell          = np.array(data['Capacity (mAh)'])[0]/1000 * Ah_to_C  # conversion to coulombs
    i_max           = np.array(data['Maximum Discharge Current (A)']) # amps   
    Min_Temp        = np.array(data['Minimum Disharge Temperature (°C)'])[0] 
    Max_Temp        = 100 # np.array(data['Maximum Discharge Temperature (°C)'])[0] 
    
    
    P_max           = 15000000 # W 
    W_bat_div_W_0   = 0.45      
    V_bat           = 600 # V  
    W_0             = 79015.8  # 737  
    L_div_D         = 15.452
    eta_0           = 0.9 
    
    #================================================================================================================================================
    
    I_bat           = P_max/ V_bat
    n_series        = V_bat/V_cell
    W_bat           = W_bat_div_W_0 * W_0
    E_bat           = W_bat * e_cell  
    Q_bat           = E_bat /V_bat
    n_parallel      = Q_bat/q_cell 
    n_parallel_min  = I_bat/i_max  
    
    if n_parallel_min  <  n_parallel: 
        Range    = (e_cell/9.81) * L_div_D * W_bat_div_W_0  * eta_0  
    else:  
        Range = 0 
    
             
    # ----------------------------------------------------------------------------------     
    # Compute distance between departure and destimation points
    # ----------------------------------------------------------------------------------
    Routes_and_Temp_Mo           = Routes_and_Temp[Routes_and_Temp['Month'] == month_no+1 ]  
    des_lon                      = np.array(Routes_and_Temp_Mo['Destination Longitude (Deg.)'])
    des_lat                      = np.array(Routes_and_Temp_Mo['Destination Latitude (Deg.)'])
    org_lon                      = np.array(Routes_and_Temp_Mo['Origin Longitude (Deg.)'])
    org_lat                      = np.array(Routes_and_Temp_Mo['Origin Latitude (Deg.)']) 
    origin_coordinates           = np.stack((des_lat,des_lon))
    destination_coordinates      = np.stack((org_lat, org_lon)) 
    R                            = 6371.0088*1000 # meters 
    coord0_rad                   = origin_coordinates*0.017453292519943295
    coord1_rad                   = destination_coordinates*0.017453292519943295
    angles                       = np.arccos(np.sin(coord0_rad[0,:])*np.sin(coord1_rad[0,:]) + 
                                            np.cos(coord0_rad[0,:])*np.cos(coord1_rad[0,:])*np.cos(coord0_rad[1,:] - coord1_rad[1,:]))
    distance                     = R*angles 
    Routes_and_Temp_Mo['Range']  = distance.tolist()
   
    # Filer List By Distance and Temperature    
    Infeasible_Routes_1  = Routes_and_Temp_Mo[Routes_and_Temp_Mo['Range'] > Range ]  
    Feasible_Routes_1    = Routes_and_Temp_Mo[Routes_and_Temp_Mo['Range'] < Range ] 
    Feasible_Routes_2    = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] > Min_Temp] 
    Infeasible_Routes_2  = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] < Min_Temp] 
    Feasible_Routes_3    = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] < Max_Temp] 
    Infeasible_Routes_3  = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] > Max_Temp]  
    Feasible_Routes_4    = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] > Min_Temp] 
    Infeasible_Routes_4  = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] < Min_Temp] 
    Feasible_Routes_5    = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] < Max_Temp] 
    Infeasible_Routes_5  = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] > Max_Temp] 
    Infeasible_Routes_6  = Feasible_Routes_5.tail(int(len(Feasible_Routes_5)*(100 - percent_adoption)/100 ))
    Feasible_Routes      = Feasible_Routes_5.head(int(len(Feasible_Routes_5)*percent_adoption/100 ))
    
    # concatenate infeasible routes 
    Infeasible_Routes    =  pd.concat([Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5,Infeasible_Routes_6])  
    
     
    ## ####################################################################################################
    ## Routes 
    ## ####################################################################################################
    
    
    #mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    #fig = go.Figure()
    #airport_marker_size  = 5
    #airport_marker_color = "white"

    ## ----------------------------------------------------------------------------------
    ## Flight Paths
    ## ----------------------------------------------------------------------------------  

    #lons       = np.empty(3 * len(Infeasible_Routes))
    #lons[::3]  = Infeasible_Routes['Origin Longitude (Deg.)']
    #lons[1::3] = Infeasible_Routes['Destination Longitude (Deg.)']
    #lons[2::3] = None
    #lats       = np.empty(3 * len(Infeasible_Routes))
    #lats[::3]  = Infeasible_Routes['Origin Latitude (Deg.)']
    #lats[1::3] = Infeasible_Routes['Destination Latitude (Deg.)']
    #lats[2::3] = None    
  
    #fig.add_trace(
        #go.Scattergeo( 
            #lon = lons,
            #lat = lats,
            #mode = 'lines',
            #line = dict(width = 0.1,color = 'grey'),  
        #)
    #)
    
    
    #lons       = np.empty(3 * len(Feasible_Routes))
    #lons[::3]  = Feasible_Routes['Origin Longitude (Deg.)']
    #lons[1::3] = Feasible_Routes['Destination Longitude (Deg.)']
    #lons[2::3] = None
    #lats       = np.empty(3 * len(Feasible_Routes))
    #lats[::3]  = Feasible_Routes['Origin Latitude (Deg.)']
    #lats[1::3] = Feasible_Routes['Destination Latitude (Deg.)']
    #lats[2::3] = None    
  
    #fig.add_trace(
        #go.Scattergeo( 
            #lon = lons,
            #lat = lats,
            #mode = 'lines',
            #line = dict(width = 2,color = "aquamarine"), 
        #)
    #)

    

    ## ----------------------------------------------------------------------------------
    ## Airports 
    ## ----------------------------------------------------------------------------------
    #fig.add_trace(go.Scattergeo( 
        #lon = Routes_and_Temp['Destination Longitude (Deg.)'],
        #lat = Routes_and_Temp['Destination Latitude (Deg.)'],
        ##hoverinfo = 'text',
        #text = Routes_and_Temp['Destination City'],
        #mode = 'markers',
        #marker = dict(
            #size = airport_marker_size,
            #color = airport_marker_color, 
        #)))
    

    #fig.add_trace(go.Scattergeo( 
        #lon = Routes_and_Temp['Origin Longitude (Deg.)'],
        #lat = Routes_and_Temp['Origin Latitude (Deg.)'],
        ##hoverinfo = 'text',
        #text = Routes_and_Temp['Origin City'],
        #mode = 'markers',
        #marker = dict(
            #size = airport_marker_size,
            #color = airport_marker_color, 
        #)))

    
    ## ----------------------------------------------------------------------------------
    ## Flight Paths
    ## ----------------------------------------------------------------------------------   
    #map_style = "dark"
    #fig.update_layout(mapbox_style  = "open-street-map",      
                      #showlegend    = False, 
                      #height        = 300, 
                      #margin        = {'t':0,'l':0,'b':0,'r':0},  
                      #mapbox        = dict( accesstoken=mapbox_access_token,style=map_style,
                                          #center=go.layout.mapbox.Center( lat=20, lon= 170 ))  )   
     
     
    
    
    
    
    # ####################################################################################################
    # Routes and Range 
    # #################################################################################################### 
    fig = go.Figure()

    sector_colors    = px.colors.qualitative.Pastel 
    
    
    #fig.add_trace(go.Histogram(histfunc="sum", y=Feasible_Routes['Passengers'], x=Feasible_Routes['Distance (miles)'], name="count"))
    #fig.add_trace(go.Histogram(histfunc="sum", y= Infeasible_Routes['Passengers'], x=Infeasible_Routes['Distance (miles)'], name="sum")) 
    #fig = px.histogram(Feasible_Routes, x="Distance (miles)", y="Passengers", nbins=8)
    #fig.add_trace(px.histogram(Infeasible_Routes, x="Distance (miles)", y="Passengers", nbins=8))
    #fig = px.histogram(Feasible_Routes, x="total_bill", nbins=20)
    #fig = px.scatter(x=x_vals, y=y_vals)
    #fig.show()
    
    sector_colors       = px.colors.qualitative.Pastel 
    fig.add_trace(go.Histogram(histfunc="sum",
                               x = Feasible_Routes['Distance (miles)'],
                               y = Feasible_Routes['Passengers'],
                               name='All Electric', 
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=sector_colors[0],
                               )
                  )
    fig.add_trace(go.Histogram(histfunc="sum",
                               x= Infeasible_Routes['Distance (miles)'],
                               y = Infeasible_Routes['Passengers'],
                               name='Fossil Fuel',
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=sector_colors[2],

                               )
                  )
    
    # The two histograms are drawn on top of another
    fig.update_layout(barmode='stack', 
                      xaxis_title_text='Distance (miles)', # xaxis label
                      yaxis_title_text='Passengers', # yaxis label 
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size )) 
    
    
    # ####################################################################################################
    # Busiest Airports 
    # #################################################################################################### 
    #fig = go.Figure()
    #sector_colors       = px.colors.qualitative.Pastel 
    #Airport_Routes     = Feasible_Routes[['Passengers','Origin Airport','Destination City']]
    #Cumulative_Flights = Airport_Routes.groupby(['Origin Airport']).sum()
    #Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(10) 
    #Alphabetical_List  = Busiest_Airports.sort_values(by=['Origin Airport'])
    
    
    #fig.add_trace(go.Bar( x=list(Alphabetical_List['Passengers'].index),
                       #y=np.array(Alphabetical_List['Passengers']),
                       #marker_color=sector_colors[0]))
    

    #fig.update_layout(xaxis_title_text='Airport', # xaxis label
                      #yaxis_title_text='Passengers', # yaxis label 
                      #height        = 300, 
                      #width         = 600, 
                      #margin        = {'t':0,'l':0,'b':0,'r':0},  
                      #bargap        = 0.1,
                      #font=dict(  size=font_size )) 
     

    
    ## ####################################################################################################
    ## Busiest Airports 
    ## ####################################################################################################
    #fig = go.Figure()
    #sector_colors       = px.colors.qualitative.Pastel 
    #Feasible_Passenger_Miles    = np.sum(np.array(Feasible_Routes['Passengers'])* np.array(Feasible_Routes['Distance (miles)']))
    #Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Passengers']])* np.array(Infeasible_Routes[['Distance (miles)']]))
    #Total_Passenger_Miles       = np.sum(np.array(Routes_and_Temp[['Passengers']])* np.array(Routes_and_Temp[['Distance (miles)']]))
    
    ## cost per seat mile for American is 13.6
    
    #cost_per_seat_mile = 13.6
    #Market = Total_Passenger_Miles*cost_per_seat_mile 
   
    #labels = ["All Electric", "Fossil Fuel"]
    
    ## Create subplots: use 'domain' type for Pie subplot 
    #fig.add_trace(go.Pie(labels=labels,
                         #values=[Feasible_Passenger_Miles, Infeasible_Passenger_Miles],
                         #marker_colors=sector_colors))
    
    ## Use `hole` to create a donut-like pie chart
    #fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    
    #fig.update_layout( title_text="Major US. Airline: " + str(round(Market/1000000000))+  'Billion USD.',
                      #height        = 400, 
                      #width         = 600, 
                      #margin        = {'t':50,'l':0,'b':0,'r':0},  
                      #font=dict(  size=font_size ))
    #fig.show()
    
     
    ## ####################################################################################################
    ## Annual Emissions 
    ## ####################################################################################################
    ## https://www.airmilescalculator.com/distance/jfk-to-sfo/#co2-emissions
    
    #no_battery = np.zeros(12)
    #battery    = np.zeros(12)
    #month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             #'August', 'September', 'October', 'November', 'December']  
    #for m_i in range(12): 
        #Routes_and_Temp_Mo           = Routes_and_Temp.loc[Routes_and_Temp['Month'] == m_i+1 ]  
        #des_lon                      = np.array(Routes_and_Temp_Mo['Destination Longitude (Deg.)'])
        #des_lat                      = np.array(Routes_and_Temp_Mo['Destination Latitude (Deg.)'])
        #org_lon                      = np.array(Routes_and_Temp_Mo['Origin Longitude (Deg.)'])
        #org_lat                      = np.array(Routes_and_Temp_Mo['Origin Latitude (Deg.)']) 
        #origin_coordinates           = np.stack((des_lat,des_lon))
        #destination_coordinates      = np.stack((org_lat, org_lon)) 
        #R                            = 6371.0088*1000 
        #coord0_rad                   = origin_coordinates*0.017453292519943295
        #coord1_rad                   = destination_coordinates*0.017453292519943295
        #angles                       = np.arccos(np.sin(coord0_rad[0,:])*np.sin(coord1_rad[0,:]) + 
                                                #np.cos(coord0_rad[0,:])*np.cos(coord1_rad[0,:])*np.cos(coord0_rad[1,:] - coord1_rad[1,:]))
        #distance                     = R*angles 
        #Routes_and_Temp_Mo['Range']  = distance.tolist()
        
        ## Filer List By Distance and Temperature   
        #Infeasible_Routes_1          = Routes_and_Temp_Mo.loc[Routes_and_Temp_Mo['Range'] > Range ]  
        #Feasible_Routes              = Routes_and_Temp_Mo.loc[Routes_and_Temp_Mo['Range'] < Range ]  
        #Feasible_Routes              = Feasible_Routes.loc[Feasible_Routes['Origin ' + month[m_i]] > Min_Temp] 
        #Infeasible_Routes_2          = Feasible_Routes.loc[Feasible_Routes['Origin ' + month[m_i]] < Min_Temp] 
        #Feasible_Routes              = Feasible_Routes.loc[Feasible_Routes['Origin ' + month[m_i]] < Max_Temp] 
        #Infeasible_Routes_3          = Feasible_Routes.loc[Feasible_Routes['Origin ' + month[m_i]] > Max_Temp] 
        #Feasible_Routes              = Feasible_Routes.loc[Feasible_Routes['Destination ' + month[m_i]] > Min_Temp] 
        #Infeasible_Routes_4          = Feasible_Routes.loc[Feasible_Routes['Destination ' + month[m_i]] < Min_Temp] 
        #Feasible_Routes              = Feasible_Routes.loc[Feasible_Routes['Destination ' + month[m_i]] < Max_Temp] 
        #Infeasible_Routes_5          = Feasible_Routes.loc[Feasible_Routes['Destination ' + month[m_i]] > Max_Temp]    
        
        ## concatenate infeasible routes 
        #Infeasible_Routes =  pd.concat([Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5])
     
        #Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Distance (miles)']]))
        #Total_Passenger_Miles       = np.sum( np.array(Routes_and_Temp_Mo[['Distance (miles)']]))

        #CO2e_per_mile = 9.0736
        
        #no_battery[m_i] = Total_Passenger_Miles * CO2e_per_mile
        #battery[m_i]    = Infeasible_Passenger_Miles * CO2e_per_mile
      
              
      
    ## Add data
    #sector_colors       = px.colors.qualitative.Pastel 

    #month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
             #'Aug', 'Sep', 'Oct', 'Nov', 'Dec']      
    #fig = go.Figure()
    ## Create and style traces
    #fig.add_trace(go.Scatter(x=month_names, y=battery, name = 'With Electrication',
                             #line=dict(color=sector_colors[0], width=4)))  
    #fig.add_trace(go.Scatter(x=month_names, y=no_battery, name='Without Electrication',
                             #line=dict(color=sector_colors[1], width=4))) 
     
    #fig.update_layout( 
                      #height           = 400, 
                      #width            = 800, 
                      #margin           = {'t':50,'l':0,'b':0,'r':0},
                      #yaxis_title_text ='CO2 Emissions (kg)', # yaxis label
                      #yaxis_range      = [0,10000000],
                      #font=dict(  size=font_size )) 
    

    fig.show()
        
    return 
     
if __name__ == '__main__':
    main()