import plotly.express as px
import pandas as pd


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def generate_battery_scatter_plot():
    df = px.data.gapminder()
    battery_fig = px.scatter(
            df.query("year==2007"),
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            log_x=True,
            size_max=60,
            template="minty",
        )

    return battery_fig

def generate_battery_spider_plot():  
    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
               'thermal stability', 'device integration']))
    battery_radar = px.line_polar(df, r='r', theta='theta', line_close=True) 
    battery_radar.update_traces(fill='toself')
    
    # https://www.youtube.com/watch?v=amRFPjSgEnk&ab_channel=CharmingData 
    # https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash%20Components/Checklist/checkbox.py 
    return battery_radar


def generate_battery_dev_map(map_style = "dark"): 
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  
    battery_map = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                            color_discrete_sequence=["aquamarine"], zoom=1 ,)
    battery_map.update_layout(mapbox_style="open-street-map",      
                              showlegend=False,
                              mapbox=dict(
                                          accesstoken=mapbox_access_token, 
                                          style=map_style, 
                                      )                              
                              ) 
    
    return battery_map