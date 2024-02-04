import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

from financial_calculator.calculator import sip, emi

from Test.growth_calculator import * 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'text-align': 'center'}, children=[
    html.H1(children='Financial Calculator'),
    html.H2(children='Calculate your SIP Maturity Amount'),
    html.Label('Enter Monthly Investment'),
    dcc.Input(id="investment", type="number", placeholder="Monthly SIP Amount", value=5000),
    html.Label('Enter expected interest in p.a'),
    dcc.Input(id="interest", type="number", placeholder="Rate of Interest (p.a.)", value=12),
    html.Label('Enter investment duration in years'),
    dcc.Input(id="tenure", type="number", placeholder="Duration of investment (in years)", value=5),
    html.H3(id='maturity'),
    dcc.Graph(id='calculator'),
    #html.Hr(),
    #html.H2(children='Calculate your EMI Amount'),
    #html.Label('Enter Loan Amount'),
    #dcc.Input(id="amount", type="number", placeholder="Loan Amount", value=2500000),
    #html.Label('Enter ROI in p.a'),
    #dcc.Input(id="emiROI", type="number", placeholder="Rate of Interest (p.a.)", value=12),
    #html.Label('Enter investment duration in years'),
    #dcc.Input(id="emiTenure", type="number", placeholder="Duration of investment (in years)", value=20),
    #html.H4(id='emi')
])

@app.callback(
    dash.dependencies.Output('calculator', 'figure'),
    [dash.dependencies.Input('investment', 'value'),
     dash.dependencies.Input('interest', 'value'),
     dash.dependencies.Input('tenure', 'value')
    ]) 

def _growth_calculator(investment, interest, tenure):
    figure = growth_calculator(investment, interest, tenure) 
    return figure

@app.callback(
    dash.dependencies.Output('maturity', 'children'),
    [dash.dependencies.Input('investment', 'value'),
     dash.dependencies.Input('interest', 'value'),
     dash.dependencies.Input('tenure', 'value')
    ])
def maturity(investment, interest, tenure):
    maturity_amount = sip(investment, tenure, interest)
    return 'Maturity Amount is: ' + str(int(maturity_amount['Amount @ Maturity']))

#@app.callback(
    #dash.dependencies.Output('emi', 'children'),
    #[dash.dependencies.Input('amount', 'value'),
     #dash.dependencies.Input('emiROI', 'value'),
     #dash.dependencies.Input('emiTenure', 'value')
    #])
#def maturity(amount, emiROI, emiTenure):
    #EMI = emi(amount, emiTenure, emiROI)
    #return f"EMI: {int(EMI['EMI'])} | Total Repayment Amount: {int(EMI['Total Repayment Amount'])} | Interest Amount: {int(EMI['Interest Amount'])}"

if __name__ == "__main__":
    app.run_server(debug=True)