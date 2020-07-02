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
    api_key = 'e3e95a65b2c8fd2dc471fb6f40aa85c68'
    try:
        data = requests.get(f'http://api.corona-19.kr/korea/country/new/?serviceKey={api_key}').json()
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
    
    layout_one = dict(title='COVID Fatality Ratio')

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
    
    layout_two = dict(title='New Cases Ratio')
    
    # Bar chart showcasing the total cases of COVID-19 by cities
    graph_three = []
    
    city_list = list(data.keys())[3:]
    total_cases = [city_status['totalCase'] for city_status in list(data.values())[3:]]
    
    graph_three.append(
        go.Bar(
            x = city_list,
            y = total_cases,
            text = total_cases,
            textposition = 'auto'
        )
    )
    
    layout_three = dict(title = 'COVID-19 total cases by cities as of TODAY',
                        xaxis = dict(title = 'City'),
                        yaxis = dict(title = 'Number of the Confirmed'))
    
    # Bar chart showcasing the new cases of COVID-19 by cities
    graph_four = []
    
    new_domestic_cases = [city_status['newCcase'] for city_status in list(data.values())[3:]]
    new_overseas_cases = [city_status['newFcase'] for city_status in list(data.values())[3:]]
    
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
    
    layout_four = dict(title = 'COVID-19 new cases by citis as of TODAY',
                       xaxis = dict(title = 'City'),
                       yaxis = dict(title = 'Number of the New Confirmed'))
    
    # Line chart with bar chart showcasing daily total and new cases
    url = 'https://api.covid19api.com/total/dayone/country/south-korea'
    daily_cases = requests.get(url).json()
    
    graph_five = []
    
    date = [day['Date'][:10] for day in daily_cases]
    total_confirmed = [day['Confirmed'] for day in daily_cases]
    
    confirmed = 0
    new_cases = []
    for case in total_confirmed:
        if case != 0:
            new_case = case - confirmed
            new_cases.append(new_case)
            confirmed += new_case
            
    graph_five.append(
        go.Scatter(
            name = 'total confirmed',
            x = date,
            y = total_confirmed,
        )
    )
    
    graph_five.append(
        go.Bar(
            name = 'new confirmed',
            x = date,
            y = new_cases
        )
    )
    
    layout_five = dict(title='The current confirmed cases on daily basis',
                       autosize=False,
                       width=1200,
                       xaxis = dict(title = 'Date'),
                       yaxis = dict(title = 'Number of the Confirmed in Total'))
            
    # append all charts
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))
    
    return figures