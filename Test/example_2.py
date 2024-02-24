# Video:    [Checklist - Python Dash Plotly](https://youtu.be/amRFPjSgEnk )
# Docs:     [dcc.Checklist](https://dash.plotly.com/dash-core-components/checklist)
#


from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates import load_figure_template

#app = dash.Dash(__name__) 


# adds  templates to plotly.io
load_figure_template(["minty_dark", "minty"]) 
 
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME]) 

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)
 
 

app.layout = html.Div([
    color_mode_switch,
    dcc.Tabs([
        
        
        dcc.Tab(label='Tab one', className="bg-primary text-white h2 p-2", children=[
            
            
            
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        
        
        ]
                
                ),
        dcc.Tab(label='Tab two',className="bg-primary text-white h2 p-2", children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Tab three',className="bg-primary text-white h2 p-2",  children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        ]),
    ])
])




#app.layout = html.Div([
    #dcc.Tabs(id = 'tabs', value = 'tab-1', children = [
    #dcc.Tab(label = 'Battery ', value = 'tab-1',className="bg-primary text-white h2 p-2"),
    #dcc.Tab(label = 'Energy Exploration', value = 'tab-2', className="bg-primary text-white h2 p-2"),
    #]),
    #html.Div(id = 'tab-content')
#])

#@callback(
    #Output('tab-content', 'children'),
    #Input('tabs', 'value')
#)

#def render_content(tab):
    #if tab == 'tab-1':
        #return html.Div([
        #color_mode_switch,
        #html.H3('Tab 1 Content'),
        #])
    #elif tab == 'tab-2':
        #return html.Div([ 
        #color_mode_switch,        
        #html.H3('Tab 2 Content'),
        #]) 
    
    
def update_figure_template(switch_off):
    template = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    patched_figure = Patch()
    patched_figure["layout"]["template"] = template 
    return patched_figure 

clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

     
if __name__ == '__main__':
    app.run_server(debug=True)