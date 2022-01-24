import os
import json

from flask import Blueprint, render_template, redirect, url_for, g, request

from datawrapper import Datawrapper

from inireader import reader
from tshistory.api import timeseries

from open_saturn.helper import generate_okta_secret
from dw_squared.client import PlotConfig, create_single_plot, update_single_plot

PLOTS = PlotConfig('plots.yaml')
REFINERY = reader('refinery.ini')
TSA = timeseries(REFINERY['db']['uri'])
TOKEN = os.environ['DW_TOKEN']
DW = Datawrapper(TOKEN)

bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@bp.route('/dashboard')
def index():
    return render_template(
        'summary.html',
        has_write_permission=True
    )

def _single_graph(graph_title):
    program = PLOTS.series_bounds([graph_title])
    data = get_data(TSA, program)
    data = saturn_to_frame(data, PLOTS, graph_title)
    charts = DW.get_charts(search=graph_title)
    if not charts:
        create_single_plot(data, PLOTS, graph_title, TOKEN)
    else:
        update_single_plot(data, PLOTS, graph_title, TOKEN)
    

@bp.route('single_graph/<graph_title>')
def single_graph(graph_title):
    return _single_graph(graph_title)