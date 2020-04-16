from dashboardapp import app

from flask import render_template
from wrangling_scripts.main import return_figures
import json
import plotly


@app.route('/')
def index():
    figures = return_figures()

    # plot ids for the html id tag
    ids = [f'figure-{i}' for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', ids=ids, figuresJSON=figuresJSON)
