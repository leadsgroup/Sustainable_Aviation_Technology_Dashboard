import plotly.express as px
import pandas as pd


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Flight Operations Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
 
def generate_global_temperature_map(map_style = "dark"): 
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  
    global_temperature_map = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                            color_discrete_sequence=["aquamarine"], zoom=3 ,)
    global_temperature_map.update_layout(mapbox_style="open-street-map",      
                              showlegend=False, 
                              height    = 400,
                              margin={'t':0,'l':0,'b':0,'r':0},                              
                              mapbox=dict(
                                          accesstoken=mapbox_access_token, 
                                          style=map_style, 
                                      )                              
                              ) 
    
    return global_temperature_map

def generate_flight_ops_airport_bar_chart():
    data_canada = px.data.gapminder().query("country == 'Canada'")
    flight_ops_bar_chart = px.bar(data_canada, x='year', y='pop') 
    flight_ops_bar_chart.update_layout(height    = 300)     
    return flight_ops_bar_chart



def generate_flight_ops_map(map_style = "dark"): 
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  
    flight_ops_map = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                            color_discrete_sequence=["aquamarine"], zoom=3 ,)
    flight_ops_map.update_layout(mapbox_style="open-street-map",      
                              showlegend=False, 
                              height    = 400,
                              margin={'t':0,'l':0,'b':0,'r':0},                              
                              mapbox=dict(
                                          accesstoken=mapbox_access_token, 
                                          style=map_style, 
                                      )                              
                              )  
    return flight_ops_map

def generate_flight_ops_pie_chart(day):
    df = px.data.tips()
    flight_ops_pie_chart = px.pie(df, values='tip', names='day')
    return flight_ops_pie_chart


# environmental_technoeconomics_chart
def generate_flight_ops_ETC_chart(day):
    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
               'thermal stability', 'device integration']))
    flight_ops_ETC_radar = px.line_polar(df, r='r', theta='theta', line_close=True) 
    flight_ops_ETC_radar.update_traces(fill='toself')
    return flight_ops_ETC_radar