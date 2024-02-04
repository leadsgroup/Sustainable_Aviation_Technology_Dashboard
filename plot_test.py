import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


import plotly.figure_factory as ff
from numpy import sin, cos,  pi
import numpy as np
def main():
    filename = 'Data/LEADS_SAT_Dashboard_Data.xlsx'
    SAT_data = pd.read_excel(filename,sheet_name=['Commercial_Batteries', 'Air_Travel','Global_Temperature'])
    Commercial_Batteries = SAT_data['Commercial_Batteries']
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Chemistry']
    c                    = Commercial_Batteries['Model']
    d                    = a + ' ' + b + ' ' + c 
    Commercial_Batteries["Battery Name"] = d     
    
    Air_Travel           = SAT_data['Air_Travel']
    Global_Temperature   = SAT_data['Global_Temperature'] 
      
    battery_plot(Global_Temperature,month)


    return 

def battery_plot(Commercial_Batteries,month,map_style = "dark"):
    # https://chart-studio.plotly.com/~Dreamshot/9158/import-plotly-plotly-version-/?_ga=2.170686953.817117617.1706992706-2105816253.1700495821#/
    
    
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
     
    fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Magnitude', radius=10,
                            center=dict(lat=0, lon=180), zoom=0,
                            mapbox_style="open-street-map")
    fig.show()
    
    
    
    x, y = np.mgrid[0:1:16j,0:1:16j]    
    z = 0.0*np.ones(x.shape)
    
    u = sin(x*pi) * cos(y*pi) * cos(z*pi)
    v = cos(x*pi) * sin(y*pi) * cos(z*pi)
    
    fig = FF.create_quiver(x, y, u, v,
                           scale=0.065,
                           arrow_scale=.3,
                           angle=pi/18,
                           name='quiver',
                           line=dict(width=1, color='#8f180b'))
    fig.show()
    
    
    
    
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  
    battery_map = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                                    color_discrete_sequence=["aquamarine"], zoom=1 ,)
    battery_map.update_layout(mapbox_style="open-street-map",      
                              showlegend=False, 
                              height    = 300,
                              margin={'t':0,'l':0,'b':0,'r':0},
                              mapbox=dict(
                                  accesstoken=mapbox_access_token, 
                                          style=map_style,
                                          center=go.layout.mapbox.Center(
                                              lat=20,
                                                      lon=10
                                                      ),                                          
                              )                              
                              ) 

     
    return 
 
 



if __name__ == '__main__': 
    main()     