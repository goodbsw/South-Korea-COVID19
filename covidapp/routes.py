from covidapp import app

import json, plotly
from flask import render_template, request, jsonify
from data.data import return_figures

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    # GET request returns current status of COVID-19 in South Korea
    figures = return_figures()
    
    # Plot ids for the html id tags
    ids = [f"figure-{i}" for i, _ in enumerate(figures)]
    
    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
 
    return render_template('index.html', ids=ids, figuresJSON=figuresJSON)