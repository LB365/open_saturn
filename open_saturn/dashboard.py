import os
import json
from time import time

from flask import Blueprint, render_template, redirect, url_for, g, request

from datawrapper import Datawrapper

from inireader import reader
from tshistory.api import timeseries

from open_saturn.helper import generate_okta_secret
from dw_squared.client import (
    PlotConfig,
    create_single_plot,
    update_single_plot,
    get_data,
    saturn_to_frame
)

PLOTS = PlotConfig('plots.yaml')
REFINERY = reader('refinery.ini')
TSA = timeseries(REFINERY['db']['uri'])
DW = Datawrapper()


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

def _single_graph(tsa:timeseries, title:str, plots:PlotConfig):
    charts = {x['title']: x['id'] for x in DW.get_charts()}
    program = PLOTS.series_bounds([title])
    data = get_data(TSA, program)
    data = saturn_to_frame(data, plots, title)
    args = data, PLOTS, title, DW._access_token
    if title not in charts:
        plot = create_single_plot(*args)
    else:
        plot = update_single_plot(*args)
    return plot.data

@bp.route('/debug_single_graph/<graph_title>')
def debug_single_graph(graph_title):
    graph = _single_graph(TSA, graph_title, PLOTS)
    return render_template('single_graph.html', graph=graph)

@bp.route('/single_graph/<graph_title>')
def single_graph(graph_title):
    return _single_graph(TSA, graph_title, PLOTS)
