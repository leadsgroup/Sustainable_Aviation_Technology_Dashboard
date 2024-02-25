

from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates import load_figure_template
 
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
 

primary_color     = '#78c2ad'
primary_color_2   = '#a9d8cb'
secondary_color   = '#f3969a' 
secondary_color_2 = '#f7bcbe'
backround         = '#212529'
success_color     = '#56cc9d'
info_color        = '#6cc3d5'
light_color       = '#f8f9fa'
warning_color     = '#fdce67'
dark_color        = '#828588'
font_size         =  '20px'
border            = '1px solid #828588'
tabs_styles       = {
    'height': '44px'
}
tab_style = {
    'borderTop': border, 
    'borderBottom': border, 
    'borderLeft': border,
    'borderRight': border,
    'padding': '6px', 
    'color': dark_color,
    'fontSize' : font_size,
    'backgroundColor': backround,
}

tab_selected_style_1 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': primary_color,
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '6px', 
    'fontSize' : font_size,
}
 

tab_selected_style_2 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': primary_color,
    'color': 'white',
    'fontWeight': 'bold',
    'fontSize' : font_size,
    'padding': '6px', 
}


tab_selected_style_3 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': primary_color,
    'color': 'white',
    'fontWeight': 'bold',
    'fontSize' : font_size,
    'padding': '6px', 
}


tab_selected_style_4 = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': primary_color,
    'color': 'white',
    'fontWeight': 'bold',
    'fontSize' : font_size,
    'padding': '6px', 
}

app.layout = html.Div([
    color_mode_switch,
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Energy-X', value='tab-1', style=tab_style, selected_style=tab_selected_style_4),
        dcc.Tab(label='Electrification', value='tab-2', style=tab_style, selected_style=tab_selected_style_1),
        dcc.Tab(label='Sustainable Aviation Fuel', value='tab-3', style=tab_style, selected_style=tab_selected_style_2),
        dcc.Tab(label='Hydrogen', value='tab-4', style=tab_style, selected_style=tab_selected_style_3),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

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


@callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'), 
              )

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])

if __name__ == '__main__':
    app.run(debug=True)