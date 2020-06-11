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
    
    # Bar chart showcasing the total cases of COVID-19 by cities
    graph_three = []
    
    city_list = list(data.keys())[3:-1]
    total_cases = [city_status['totalCase'] for city_status in list(data.values())[3:-1]]
    
    graph_three.append(
        go.Bar(
            x = city_list,
            y = total_cases,
            text = total_cases,
            textposition = 'auto'
        )
    )
    
    layout_three = dict(title_text = 'COVID-19 total cases by cities as of TODAY')
    
    # Bar chart showcasing the new cases of COVID-19 by cities
    graph_four = []
    
    new_domestic_cases = [city_status['newCcase'] for city_status in list(data.values())[3:-1]]
    new_overseas_cases = [city_status['newFcase'] for city_status in list(data.values())[3:-1]]
    
    graph_four.append(
        go.Bar(
            name = 'Domestic',
            x = city_list,
            y = new_domestic_cases,
            text = new_domestic_cases,
            textposition = 'auto'
        )
    )
    graph_four.append(
        go.Bar(
            name = 'Overseas',
            x = city_list,
            y = new_overseas_cases,
            text = new_overseas_cases,
            textposition = 'auto'
        )
    )
    
    layout_four = dict(title_text = 'COVID-19 new cases by citis as of TODAY')
    
    # append all charts
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
