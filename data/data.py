import requests
import pandas as pd
import numpy as np
# import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.colors

def calculate_cases(total, recovered, death):
    """Calculate the number of patients with certain status
    
    Args:
        total(string): total number of COVID patients
        recovered(string): total number of recovered patients
        death(string): total number of the death
        
    Returns:
        list(int): list containing recovered, under treatement, death in order
    """
    
    total = int(total.replace(',', ''))
    recovered = int(recovered.replace(',', ''))
    death = int(death.replace(',', ''))
    under_treatement = total - recovered - death
    
    return [recovered, under_treatement, death]
    

def return_figures():
    """Creates four visualizations that show current status of corona virus in South Korea
    
    Args:
        None
    
    Returns:
        list(dict): list containing the four plotly visualizations
    """
    
    # Pulling data from COVID-19 api
    try:
        data = requests.get('http://api.corona-19.kr/korea/country/new/').json()
    except:
        print('failed to load data')
        
    patients_status = data['korea']
    
    # pie chart by COVID fatality
    graph_one = []
    
    labels = ['Recovered', 'Under Treatement', 'Death']
    values = calculate_cases(patients_status['totalCase'],
                             patients_status['recovered'],
                             patients_status['death'])
    
    graph_one.append(go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        insidetextorientation='radial'
    ))
    
    layout_one = dict(title_text='COVID Fatality Rate')
    
    go.Figure(data=graph_one[0], layout=layout_one).show()

    # Pie chart by new COVID cases as of TODAY
    graph_two = []
    
    labels = ['Domestic', 'Overseas']
    values = [patients_status['newCcase'], patients_status['newFcase']]
    
    graph_two.append(go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        insidetextorientation='radial'
    ))
    
    layout_two = dict(title_text='New Cases Ratio')
    
    go.Figure(data=graph_two[0], layout=layout_two).show()

return_figures()
