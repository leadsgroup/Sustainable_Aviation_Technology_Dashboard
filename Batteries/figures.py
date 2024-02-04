import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np 


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def generate_battery_scatter_plot(Commercial_Batteries,selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off): 
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    unique_brands        = list(Commercial_Batteries['Brand'][1:].unique())
    unique_chemsitrys    = list(Commercial_Batteries['Chemistry'][1:].unique())
    marker_size          = 15
    opacity_ratio        = 0.8 if switch_off else 1.0
    font_size            = 16 

    # Brand Colors: greenyellow, aquamarine, paleturquoise, lightcoral, yellow, lavender ,thistle ,orangered   
    Brand_Colors      = px.colors.qualitative.Pastel 
    Chemistry_Markers = ['square','x','circle','cross','diamond','triangle-up','triangle-down'] 
    fig = go.Figure()
    if selected_brand == 'All' and  selected_chemistry == 'All':
        # for each Brand 
        for i in range(len(unique_brands)): 
            # for each chemsitry 
            for j in range(len(unique_chemsitrys)):
                data_1 = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == unique_brands[i]] 
                data_2 = data_1.loc[Commercial_Batteries['Chemistry'] == unique_chemsitrys[j]]  
                models = data_2["Model"]
                fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                                     y             = np.array(data_2[selected_y_axis]),  
                                     mode          = 'markers', 
                                     name          ="",                                    
                                     marker        = dict(size=marker_size,color=Brand_Colors[i],opacity=opacity_ratio,symbol = Chemistry_Markers[j]),
                                     hovertemplate = 'Brand: ' + unique_brands[i] + '<br>' + 'Chemistry: ' + unique_chemsitrys[j] + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                     )) 
    elif selected_brand != 'All' and  selected_chemistry == 'All':
        # for each Brand  
        for j in range(len(unique_chemsitrys)):
            data_1 = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == selected_brand] 
            data_2 = data_1.loc[Commercial_Batteries['Chemistry'] == unique_chemsitrys[j]]  
            i_index  = unique_brands.index(selected_brand)
            models = data_2["Model"]
            fig.add_trace(go.Scatter( x             = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers',
                                 name          = "",            
                                 marker        = dict(size=marker_size,color=Brand_Colors[i_index ],opacity=opacity_ratio,symbol = Chemistry_Markers[j]),
                                 hovertemplate = 'Brand: ' + selected_brand + '<br>' + 'Chemistry: ' + unique_chemsitrys[j] + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))
    elif selected_brand == 'All' and selected_chemistry != 'All':
        # for each Brand 
        for i in range(len(unique_brands)):  
            data_1   = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == unique_brands[i]] 
            data_2   = data_1.loc[Commercial_Batteries['Chemistry'] == selected_chemistry] 
            j_index  = unique_chemsitrys.index(selected_chemistry)
            models = data_2["Model"]
            fig.add_trace(go.Scatter( x             = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers',
                                 name          = "",      
                                 marker        = dict(size=marker_size,color=Brand_Colors[i],opacity=opacity_ratio,symbol = Chemistry_Markers[j_index]),
                                 hovertemplate = 'Brand: ' + unique_brands[i] + '<br>' + 'Chemistry: ' + selected_chemistry + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))
    else:
        data_1   = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == selected_brand ] 
        data_2   = data_1.loc[Commercial_Batteries['Chemistry'] == selected_chemistry] 
        i_index  = unique_brands.index(selected_brand)
        j_index  = unique_chemsitrys.index(selected_chemistry)
        models = data_2["Model"]
        fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                             y             = np.array(data_2[selected_y_axis]),  
                             mode          = 'markers', 
                             name          = "",       
                             marker        = dict(size=marker_size,color=Brand_Colors[i_index],opacity=opacity_ratio,symbol = Chemistry_Markers[j_index]),
                             hovertemplate = 'Brand: ' + selected_brand  + '<br>' + 'Chemistry: ' + selected_chemistry + '<br>' + 'Model: ' + models  + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                             ))
 
    fig.update_layout(xaxis_title = selected_x_axis,
                       yaxis_title = selected_y_axis,
                       showlegend  = False, 
                       height      = 400,
                       margin      ={'t':0,'l':0,'b':0,'r':0},
                       font=dict(  size=font_size ),  
                       )     
    fig["layout"]["template"] = template 
    return fig 

def generate_battery_spider_plot(Commercial_Batteries,bat_1,bat_2,bat_3,switch_off): 
    template     = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]   
    font_size     = 16     
    data_1        = Commercial_Batteries.loc[ Commercial_Batteries['Battery Name'] == bat_1] 
    vals_1        = np.zeros((1,7))
    vals_1[:,:6]  = np.array(data_1[['Gravimetric Power Density (W/kg)' ,'Maximum Voltage (V)','Capacity (mAh)','Maximum Discharge Current (A)','Maximum Discharge Power (W)', 'Gravimetric Energy Density (Wh/kg)']])
    vals_1[0,6]   = vals_1[0,0]    
        
    data_2       = Commercial_Batteries.loc[ Commercial_Batteries['Battery Name'] == bat_2]  
    vals_2       = np.zeros((1,7))
    vals_2[:,:6] = np.array(data_2[['Gravimetric Power Density (W/kg)' ,'Maximum Voltage (V)','Capacity (mAh)','Maximum Discharge Current (A)','Maximum Discharge Power (W)', 'Gravimetric Energy Density (Wh/kg)']]) 
    vals_2[0,6]  = vals_2[0,0]   

    data_3       = Commercial_Batteries.loc[ Commercial_Batteries['Battery Name'] == bat_3]  
    vals_3       = np.zeros((1,7))
    vals_3[:,:6] = np.array(data_3[['Gravimetric Power Density (W/kg)' ,'Maximum Voltage (V)','Capacity (mAh)','Maximum Discharge Current (A)','Maximum Discharge Power (W)', 'Gravimetric Energy Density (Wh/kg)']]) 
    vals_3[0,6]  = vals_3[0,0] 
    
    # Stack data
    battery_data = np.vstack((vals_1,vals_2 ))    
    battery_data = np.vstack((battery_data,vals_3))   
     
    ranges = np.array([[1000,5,5000,20,50,500,1000], [1000,5,5000,20,50,500,1000], [1000,5,5000,20,50,500,1000]])
     
    fig_2 = go.Figure()  
    
    scales_data = np.zeros((2,len(ranges))) 
    scales_data = battery_data/ranges 
    fig_2.add_trace(
                go.Scatterpolar(
                                r    = scales_data[0],
                                theta=['Power Density <br>  (W/kg)' ,'Max Voltage <br>   (V)','Capacity <br>  (mAh)',
                                       'Max. Discharge<br> Current (A)','Max. Discharge <br> Power (W)',
                                       'Energy Density <br>  (Wh/kg)','Power Density <br>  (W/kg)' ],  
                                fill      ='toself', 
                                name      = 'Battery 1', 
                                marker    = None,
                                line=dict(color=px.colors.qualitative.Pastel[0],width = 4),  # px.colors.qualitative.Light24[6]
                                showlegend=True, 
                                )
                )
    

    fig_2.add_trace(
                go.Scatterpolar(
                                r    = scales_data[1],
                                theta=['Power Density <br>  (W/kg)' ,'Max Voltage <br>   (V)','Capacity <br>  (mAh)',
                                       'Max. Discharge<br> Current (A)','Max. Discharge <br> Power (W)',
                                       'Energy Density <br>  (Wh/kg)','Power Density <br>  (W/kg)' ],  
                                fill      ='toself', 
                                name      = 'Battery 2', 
                                marker    = None,
                                line=dict(color=px.colors.qualitative.Pastel[1],width = 4), # px.colors.qualitative.Light24[13]
                                showlegend=True, 
                                )
                )        


    fig_2.add_trace(
                go.Scatterpolar(
                                r    = scales_data[2],
                                theta=['Power Density <br>  (W/kg)' ,'Max Voltage <br>   (V)','Capacity <br>  (mAh)',
                                       'Max. Discharge<br> Current (A)','Max. Discharge <br> Power (W)',
                                       'Energy Density <br>  (Wh/kg)','Power Density <br>  (W/kg)' ],  
                                fill      ='toself', 
                                name      = 'Battery 3', 
                                marker    = None,
                                line=dict(color=px.colors.qualitative.Pastel[4],width = 4),  # px.colors.qualitative.Light24[19]
                                showlegend=True, 
                                )
                )        

    fig_2.update_layout(height      = 400, 
                       margin={'t':50},
                       font=dict(  size=font_size ),  
                           )            
    fig_2.update_polars(radialaxis=dict(visible=False,range=[0, 1]))  
    fig_2["layout"]["template"] = template 
    return fig_2 


def generate_battery_dev_map(Commercial_Batteries,map_style = "dark"): 
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

    return battery_map