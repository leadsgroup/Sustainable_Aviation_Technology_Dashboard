import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np 
import plotly.figure_factory as ff
from numpy import sin, cos,  pi
import numpy as np
def main():
    filename = 'Data/LEADS_SAT_Dashboard_Data.xlsx'
    SAT_data = pd.read_excel(filename,sheet_name=['Commercial_Batteries','Battery_Research', 'Air_Travel','US_Temperature_F'])
    Commercial_Batteries = SAT_data['Commercial_Batteries']
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ' ' + b + ' ' + c 
    Commercial_Batteries["Battery Name"] = d     
    
    Air_Travel           = SAT_data['Air_Travel']
    US_Temperature_F   = SAT_data['US_Temperature_F'] 
    period_of_year       = 0
      
    battery_plot(US_Temperature_F,period_of_year)

    # https://plotly.com/python/lines-on-mapbox/
    return 

def battery_plot(US_Temperature_F,period_of_year,map_style = "dark"):
    points        = 105
    start         = points*period_of_year
    end           = points*(1+period_of_year)
    Date          = US_Temperature_F['Date'][start:end] 
    latitude      = np.array(US_Temperature_F['Latitude'][start:end])  
    longitude     = np.array(US_Temperature_F['Longitude'][start:end])
    east_wind     = np.array(US_Temperature_F['Eastward Wind Velocity (m/s)'][start:end])  
    north_wind    = np.array(US_Temperature_F['Northward Wind Velocity (m/s)'][start:end])
    ground        = np.zeros_like(latitude)
    temp   = np.array(US_Temperature_F['Surface Temperature (°C)'][start:end])
      
    colormap                 = 'jet'  
    min_noise_level          = 35 
    max_noise_level          = 90
    noise_scale_label        = None
    save_figure              = False
    show_figure              = True
    save_filename            = "Noise_Contour"
    use_lat_long_coordinates = True
    show_trajectory          = False
    show_microphones         = False
    colormap                 = 'jet'
    background_color         = 'rgb(17,54,71)'
    grid_color               = 'gray'
    width                    = 1400
    height                   = 800
      
                        
    fig  = go.Figure()
    
    plot_data  = []   
    
    # ---------------------------------------------------------------------------     
    # geo
    # --------------------------------------------------------------------------- 
    fig.add_trace(go.Scattergeo( )) 
    fig.update_traces(opacity=0.1)
    
    # ---------------------------------------------------------------------------     
    # temperature 
    # --------------------------------------------------------------------------- 
    
    fig.add_trace(go.Contour(
        z  = temp,
        x  = longitude,
        y  = latitude, 
        colorscale = 'jet',
        opacity= 0.5, 
        colorbar = dict(title = 'Temperature', titleside = "right", orientation = "v"),
        contours=dict(
            start=-40,
            end=40,
            size=5,
        ),
    ))   
    
    # ---------------------------------------------------------------------------     
    # wind
    # ---------------------------------------------------------------------------    
    width_dim  = 7 
    lenth_dim  = 15 
    scaleratio = 0.8
    scale      = 0.4    
    x          = np.reshape(longitude,(width_dim,lenth_dim))
    y          = np.reshape(latitude,(width_dim,lenth_dim))
    u          = np.reshape(east_wind,(width_dim,lenth_dim))
    v          = np.reshape(north_wind,(width_dim,lenth_dim))
    fig.add_trace(ff.create_quiver(x, y, u, v,
                           scale=.25,
                           line=dict(width=1.15, color='white'),
                           arrow_scale=.3,       
                           name='quiver1', 
                           line_width=1.15).data[0],) 

    # ---------------------------------------------------------------------------     
    # world map 
    # ---------------------------------------------------------------------------       
         
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  
    fig2 = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                                    color_discrete_sequence=["aquamarine"], zoom=1)  
        
    fig2.update_layout(mapbox_style="open-street-map",      
                    showlegend=False, 
                    margin={'t':0,'l':0,'b':0,'r':0},
                    mapbox=dict( accesstoken=mapbox_access_token,  style=map_style, center=go.layout.mapbox.Center( lat=20, lon=10 ))                              
                              )     
 
    # ----------------------------------------------------------------------------------------------------------------------  
    
    # AIRCRAFT TRAJECTORY - routes 
    #if show_trajectory:
        #aircraft_trajectory = go.Scatter3d(x   =  ,
                                           #y   =  ,
                                           #z   =  ,
                                           #mode= 'markers',
                                           #marker=dict(size=6,
                                                       #color='black',
                                                       #opacity=0.8),
                                    #line=dict(color='black',width=2))
        #plot_data.append(aircraft_trajectory)
        
     
    # ----------------------------------------------------------------------------------------------------------------------  
         
    # GROUND MICROPHONES can be used for airpots  
    #microphones = go.Scatter3d(x        = Y.flatten(),
                               #y        = X.flatten(),
                               #z        = Z.flatten(),
                               #mode     = 'markers',
                               #marker   = dict(size=6,color='white',opacity=0.8),
                               #line     = dict(color='white',width=2))
    #plot_data.append(microphones)
    
    # ----------------------------------------------------------------------------------------------------------------------  
    
    fig.show()
     

    return fig       
 
def colorax(vmin, vmax):
    return dict(cmin=vmin, cmax=vmax)
 
def contour_surface_slice(x,y,z,values,color_scale, showscale = False , colorbar_title = None, colorbar_location = 'right', colorbar_orientation = 'v'):
    return go.Surface(x=x,y=y,z=z,surfacecolor=values,colorscale=color_scale, showscale=showscale,
                      colorbar = dict(title = colorbar_title, titleside = "right", orientation = "v")) 

   


if __name__ == '__main__': 
    main()     