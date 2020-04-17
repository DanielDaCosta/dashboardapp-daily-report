from dashboardapp import app

from flask import render_template
from wrangling_scripts.main import return_data
import json
import plotly


@app.route('/')
def index():
    data = return_data()
    figures = data['figures']

    # plot ids for the html id tag
    ids = [f'figure-{i}' for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', ids=ids, figuresJSON=figuresJSON,
                           high_aglom=data['high_aglom'],
                           low_variations=data['low_variations'],
                           high_variations=data['high_variations'],
                           date=data['date_string'])
