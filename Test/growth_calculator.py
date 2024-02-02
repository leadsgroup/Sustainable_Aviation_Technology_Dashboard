
from financial_calculator.calculator import sip, emi


def growth_calculator(investment, interest, tenure):
    sip_dict = sip(investment, tenure, interest, show_amount_list=True)
    maturity_amount = sip_dict['Amount @ Maturity']
    monthly_amount = sip_dict['Amount every month']
    
    x_axis = list(monthly_amount.keys())
    growth = list(monthly_amount.values())
    total_investment = [investment*(month) for month in monthly_amount.keys()]
      
    figure = {
        'data': [
            {'x': x_axis, 'y': growth, 'type': 'line', 'name': 'Total Growth'},
            {'x': x_axis, 'y': total_investment, 'type': 'line', 'name': 'Total Investment'}],
        'layout': {'title': 'SIP Calculator'}
    }
    return figure