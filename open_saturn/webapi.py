import io

from flask import (
    Blueprint,
    render_template,
)

from sqlalchemy import create_engine
from rework import api
from pml import HTML
from tshistory_refinery.webapi import make_app as refinery_app

from tshistory_refinery import helper
from tshistory_refinery.webapi import make_app


def make_open_app(config):
    tsa = helper.apimaker(config)
    app = refinery_app(config, tsa)

    bp = Blueprint(
        'open_saturn',
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    @bp.route('/')
    def welcome():

        return render_template(
            'summary.html',
            has_write_permission=True
        )

    app.register_blueprint(bp)
    return app
