import plotly.express as px
import pandas as pd
import plotly.io as pio 
import numpy as np  
from urllib.request import urlopen
import plotly.graph_objects as go
import json 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Flight Operations Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
 
def generate_us_temperature_map(US_Temperature_F,month_no,switch_off):  
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    font_size            = 16  
    
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)     
    
    month = list(US_Temperature_F.columns.values)[3:][month_no] 
    fips  = list(US_Temperature_F['FIPS'])  
    US_Temperature_F['FIPS'] = ["%05d" % i for i in fips] 
    us_temperature_map= px.choropleth(US_Temperature_F, geojson=counties, locations='FIPS', color = month,
                           color_continuous_scale="RdYlBu_r", 
                           hover_data=["Name","State", month],
                           scope='usa',
                           range_color=(0, 90),  
                          )   
    us_temperature_map.update_layout(coloraxis_colorbar=dict(title=" "),
                                     coloraxis_colorbar_x=0.85, 
                                     height    = 400, 
                                     margin={'t':0,'l':0,'b':0,'r':0},                              
                              )  
    us_temperature_map.update_coloraxes( colorbar_tickvals= np.linspace(0,90,11),
                                        colorbar_tickfont_size=font_size) 

    us_temperature_map["layout"]["template"] = template     
    return us_temperature_map


def generate_flight_ops_map(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off): 
    mapbox_access_token  = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    map_style            = None if switch_off else 'dark'  
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    
    if aircraft == "Boeing 737": 
        P_max           = 15000000 
        W_0             = 79015.8  
        L_div_D         = 15.452 
    elif aircraft == 'Airbus A320': 
        P_max           = 15000000 
        W_0             = 78000
        L_div_D         = 15.452         
        
    Wh_per_kg_to_J     = 3600.0
    Ah_to_C            = 3600.0  
    V_bat              = system_voltage
    eta_0              = propulsive_efficiency/100 

    # ---------------------------------------------------------------------------------------------------------------------------------------------- 
    # Compute Range
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    
    month_names     = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']      
    month           =  month_names[month_no] 
    data            = Commercial_Batteries[Commercial_Batteries['Battery Name'] == battery_choice] 
    V_cell          = np.array(data['Nominal Voltage (V)'])[0]
    e_cell          = np.array(data['Gravimetric Energy Density (Wh/kg)'])[0] *Wh_per_kg_to_J
    q_cell          = np.array(data['Capacity (mAh)'])[0]/1000 * Ah_to_C  # conversion to coulombs
    i_max           = np.array(data['Maximum Discharge Current (A)'])[0] # amps   
    Min_Temp        = np.array(data['Minimum Disharge Temperature (°C)'])[0]*9/5 + 32
    Max_Temp        = np.array(data['Maximum Discharge Temperature (°C)'])[0]*9/5 + 32  
    I_bat           = P_max/ V_bat
    n_series        = V_bat/V_cell
    W_bat           = (weight_fraction/100) * W_0
    E_bat           = W_bat * e_cell  
    Q_bat           = E_bat /V_bat
    n_parallel      = Q_bat/q_cell 
    n_parallel_min  = I_bat/i_max 
    
    if n_parallel_min  <  n_parallel: 
        Range    = (e_cell/9.81) * L_div_D * (weight_fraction/100)* eta_0
    else:  
        Range = 0 
    
             
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    # Compute distance between departure and destimation points
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    Routes_and_Temp_Mo           = Routes_and_Temp[Routes_and_Temp['Month'] == month_no+1 ]  
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
     
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    # Routes 
    # ---------------------------------------------------------------------------------------------------------------------------------------------- 
    mapbox_access_token  = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    fig                  = go.Figure()
    airport_marker_size  = 5
    airport_marker_color = "white"

    # ----------------------------------------------------------------------------------------------------------------------------------------------
    # Flight Paths
    # ----------------------------------------------------------------------------------------------------------------------------------------------
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
 

    # ----------------------------------------------------------------------------------------------------------------------------------------------
    # Airports 
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scattergeo( 
        lon = Routes_and_Temp['Destination Longitude (Deg.)'],
        lat = Routes_and_Temp['Destination Latitude (Deg.)'], 
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
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    # Flight Paths
    # ---------------------------------------------------------------------------------------------------------------------------------------------- 
    fig.update_layout(mapbox_style  = "open-street-map",      
                      showlegend    = False, 
                      height        = 400, 
                      geo_scope     ='usa',
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      mapbox        = dict( accesstoken=mapbox_access_token,style=map_style,
                                            center=go.layout.mapbox.Center( lat=30, lon= 230 ))  )   
     

    fig["layout"]["template"] = template
        
    return fig

def generate_electric_aircraft_flight_ops_meta_data(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,switch_off): 
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]     
    font_size            = 16 

    # ---------------------------------------------------------------- ---------------------------------------------------------------------
    # Compute Aircraft Properties 
    # ---------------------------------------------------------------- ---------------------------------------------------------------------    
    if aircraft == "Boeing 737": 
        P_max           = 15000000 
        W_0             = 79015.8  
        L_div_D         = 15.452 
    elif aircraft == 'Airbus A320': 
        P_max           = 15000000 
        W_0             = 78000
        L_div_D         = 15.452     
            
    cost_per_seat_mile = 13.6 # cost per seat mile for American is 13.6 
    CO2e_per_mile      = 9.0736                 
    Wh_per_kg_to_J     = 3600.0
    Ah_to_C            = 3600.0  
    V_bat              = system_voltage
    eta_0              = propulsive_efficiency/100  
    
    months          = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']      
    month           =  months[month_no] 
    data            = Commercial_Batteries[Commercial_Batteries['Battery Name'] == battery_choice] 
    V_cell          = np.array(data['Nominal Voltage (V)'])[0]
    e_cell          = np.array(data['Gravimetric Energy Density (Wh/kg)'])[0] *Wh_per_kg_to_J
    q_cell          = np.array(data['Capacity (mAh)'])[0]/1000 * Ah_to_C  # conversion to coulombs
    i_max           = np.array(data['Maximum Discharge Current (A)'])[0] # amps   
    Min_Temp        = np.array(data['Minimum Disharge Temperature (°C)'])[0]*9/5 + 32
    Max_Temp        = np.array(data['Maximum Discharge Temperature (°C)'])[0]*9/5 + 32   
    I_bat           = P_max/ V_bat
    n_series        = V_bat/V_cell
    W_bat           = (weight_fraction/100) * W_0
    E_bat           = W_bat * e_cell  
    Q_bat           = E_bat /V_bat
    n_parallel      = Q_bat/q_cell 
    n_parallel_min  = I_bat/i_max 
    
    if n_parallel_min  <  n_parallel: 
        Range    = (e_cell/9.81) * L_div_D * (weight_fraction/100)* eta_0
    else:  
        Range = 0  
             
    # ---------------------------------------------------------------- ---------------------------------------------------------------------
    # Compute distance between departure and destimation points
    # ---------------------------------------------------------------- ---------------------------------------------------------------------
    Routes_and_Temp_Mo           = Routes_and_Temp[Routes_and_Temp['Month'] == month_no+1 ]  
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

    #================================================================================================================================================  
    # 
    #================================================================================================================================================    

    fig_5               = go.Figure()
    sector_colors       = px.colors.qualitative.Pastel 
    fig_5.add_trace(go.Histogram(histfunc="sum",
                               x= Feasible_Routes['Distance (miles)'],
                               y = Feasible_Routes['Passengers'],
                               name='All Electric', 
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=sector_colors[0],
                               )
                  )
    fig_5.add_trace(go.Histogram(histfunc="sum",
                               x= Infeasible_Routes['Distance (miles)'],
                               y = Infeasible_Routes['Passengers'],
                               name='Fossil Fuel',
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=sector_colors[2],

                               )
                  )
    
    # The two histograms are drawn on top of another
    fig_5.update_layout(barmode='stack', 
                      xaxis_title_text='Distance (miles)', # xaxis label
                      yaxis_title_text='Passengers', # yaxis label 
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size ))     

    fig_5["layout"]["template"] = template     

    #================================================================================================================================================      

    #================================================================================================================================================    

    fig_6 = go.Figure()
    sector_colors      = px.colors.qualitative.Pastel 
    Airport_Routes     = Feasible_Routes[['Passengers','Origin Airport','Destination City']]
    Cumulative_Flights = Airport_Routes.groupby(['Origin Airport']).sum()
    Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(10) 
    Alphabetical_List  = Busiest_Airports.sort_values(by=['Origin Airport'])  
    fig_6.add_trace(go.Bar( x=list(Alphabetical_List['Passengers'].index),
                       y=np.array(Alphabetical_List['Passengers']),
                       marker_color=sector_colors[0])) 
    fig_6.update_layout(xaxis_title_text='Airport', # xaxis label
                      yaxis_title_text='Passengers', # yaxis label 
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size ))      
    fig_6["layout"]["template"] = template    

    #================================================================================================================================================      
    # 
    #================================================================================================================================================    
    fig_7                       = go.Figure()
    colors                      = px.colors.qualitative.Pastel 
    sector_colors               = [colors[0],colors[2]]
    Feasible_Passenger_Miles    = np.sum(np.array(Feasible_Routes['Passengers'])* np.array(Feasible_Routes['Distance (miles)']))
    Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Passengers']])* np.array(Infeasible_Routes[['Distance (miles)']]))
    Total_Passenger_Miles       = np.sum(np.array(Routes_and_Temp[['Passengers']])* np.array(Routes_and_Temp[['Distance (miles)']])) 
    Market                      = Total_Passenger_Miles*cost_per_seat_mile  
    labels                      = ["All Electric", "Fossil Fuel"] 
    fig_7.add_trace(go.Pie(labels=labels,
                         values=[Feasible_Passenger_Miles, Infeasible_Passenger_Miles],
                         marker_colors=sector_colors)) 
    fig_7.update_traces(hole=.4, hoverinfo="label+percent+name") 
    fig_7.update_layout( title_text="Major US. Airline Marker Size: " + str(round(Market/1000000000))+  ' Billion USD.',
                      height        = 400, 
                      width         = 600, 
                      margin        = {'t':50,'l':0,'b':0,'r':0},  
                      font=dict(  size=font_size ))      

    fig_7["layout"]["template"] = template     
     
    #================================================================================================================================================      
    # 
    #================================================================================================================================================   
    no_battery = np.zeros(12)
    battery    = np.zeros(12) 
    for m_i in range(12): 
        Routes_and_Temp_Mo           = Routes_and_Temp.loc[Routes_and_Temp['Month'] == m_i+1 ]  
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
        Infeasible_Routes_1  = Routes_and_Temp_Mo[Routes_and_Temp_Mo['Range'] > Range ]  
        Feasible_Routes_1    = Routes_and_Temp_Mo[Routes_and_Temp_Mo['Range'] < Range ] 
        Feasible_Routes_2    = Feasible_Routes_1[Feasible_Routes_1['Origin ' + months[m_i]] > Min_Temp] 
        Infeasible_Routes_2  = Feasible_Routes_1[Feasible_Routes_1['Origin ' + months[m_i]] < Min_Temp] 
        Feasible_Routes_3    = Feasible_Routes_2[Feasible_Routes_2['Origin ' + months[m_i]] < Max_Temp] 
        Infeasible_Routes_3  = Feasible_Routes_2[Feasible_Routes_2['Origin ' + months[m_i]] > Max_Temp]  
        Feasible_Routes_4    = Feasible_Routes_3[Feasible_Routes_3['Destination ' + months[m_i]] > Min_Temp] 
        Infeasible_Routes_4  = Feasible_Routes_3[Feasible_Routes_3['Destination ' + months[m_i]] < Min_Temp] 
        Feasible_Routes_5    = Feasible_Routes_4[Feasible_Routes_4['Destination ' + months[m_i]] < Max_Temp] 
        Infeasible_Routes_5  = Feasible_Routes_4[Feasible_Routes_4['Destination ' + months[m_i]] > Max_Temp] 
        Infeasible_Routes_6  = Feasible_Routes_5.tail(int(len(Feasible_Routes_5)*(100 - percent_adoption)/100 ))
        Feasible_Routes      = Feasible_Routes_5.head(int(len(Feasible_Routes_5)*percent_adoption/100 ))
        
        # concatenate feasible and infeasible routes 
        Infeasible_Routes           = pd.concat([Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5,Infeasible_Routes_6])   
        Infeasible_Routes           = pd.concat([Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5]) 
        Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Distance (miles)']]))
        Total_Passenger_Miles       = np.sum( np.array(Routes_and_Temp_Mo[['Distance (miles)']]))  
        no_battery[m_i]             = Total_Passenger_Miles * CO2e_per_mile
        battery[m_i]                = Infeasible_Passenger_Miles * CO2e_per_mile
      
               
    colors              = px.colors.qualitative.Pastel 
    sector_colors       = [colors[0],colors[2]] 
    month_names         = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']      
    fig_8               = go.Figure()
    # Create and style traces
    fig_8.add_trace(go.Scatter(x=month_names, y=battery, name = 'With Electrication',
                             line=dict(color=sector_colors[0], width=4)))  
    fig_8.add_trace(go.Scatter(x=month_names, y=no_battery, name='Without Electrication',
                             line=dict(color=sector_colors[1], width=4)))  
    fig_8.update_layout( 
                      height           = 400, 
                      width            = 800, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='CO2 Emissions (kg)', # yaxis label
                      yaxis_range      = [0,10000000],
                      font=dict(  size=font_size )) 
        

    fig_8["layout"]["template"] = template         
    
    return fig_5, fig_6, fig_7,fig_8 
 