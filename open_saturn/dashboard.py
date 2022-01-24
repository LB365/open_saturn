import os
import json

from flask import Blueprint, render_template, redirect, url_for, g, request

from datawrapper import Datawrapper

from inireader import reader
from tshistory.api import timeseries

from open_saturn.helper import generate_okta_secret
from dw_squared.client import PlotConfig, create_single_plot, update_single_plot, get_data

PLOTS = PlotConfig('plots.yaml')
REFINERY = reader('refinery.ini')
TSA = timeseries(REFINERY['db']['uri'])
TOKEN = os.environ['DW_TOKEN']

bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@bp.route('/dashboard')
def index():
    return render_template(
        'dashboard.html',
        has_write_permission=True
    )

def _single_graph(tsa:timeseries, title:str, token:str, plots:PlotConfig):
    dw = Datawrapper(token)
    program = PLOTS.series_bounds([title])
    data = get_data(TSA, program)
    data = saturn_to_frame(data, plots, title)
    charts = dw.get_charts(search=title)
    args = data, PLOTS, title, token
    create_single_plot(*args) if not charts else update_single_plot(*args)
    chart = dw.get_iframe_code(title)
    print(chart) 
    return chart
    

@bp.route('/single_graph/<graph_title>')
def single_graph(graph_title):
    return _single_graph(TSA, graph_title, TOKEN, PLOTS)