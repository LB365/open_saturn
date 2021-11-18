import os
import json
import logging

from flask import Blueprint, render_template, redirect, url_for, g, request
from tshistory_refinery.webapi import make_app as refinery_app
from tshistory_refinery import helper

from open_saturn.helper import generate_okta_secret

bp = Blueprint(
    'open_saturn',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@bp.route('/')
def index():
    return render_template(
        'summary.html',
        has_write_permission=True
    )


def init_app(config):
    tsa = helper.apimaker(config)
    app = refinery_app(config, tsa)
    return app


def make_open_app(config):
    app = init_app(config)
    app.register_blueprint(bp)
    return app


def _generate_client_secrets(path):
    secrets = generate_okta_secret()
    with open(path, 'w') as f:
        json.dump(secrets, f)


def make_okta_app(config):
    path = 'client_secrets.json'
    app = init_app(config)
    org = os.environ['OKTA_CLIENT_ORGURL']
    token = os.environ['OKTA_CLIENT_TOKEN']
    _generate_client_secrets(path)
    app.config["OIDC_CLIENT_SECRETS"] = path
    app.config["OIDC_COOKIE_SECURE"] = False
    app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
    app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
    app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
    app.secret_key = os.environ['RANDOM_SECRET_KEY']
    from flask_oidc import OpenIDConnect
    oidc = OpenIDConnect(app)
    from okta import UsersClient as OktaClient
    okta_client = OktaClient(org, token)
    app.register_blueprint(bp)
    views = app.view_functions
    open_views = [
        'tshistory_rest',   # Rest API
        'xlapi',            # Excel API
        '_oidc_callback',   # Callbacks
        'logout',           # Logout
        'open_saturn.index' # Landing page
    ]
    secure_views = {k: v for k, v in views.items() if
                    not any(e in k for e in open_views)}

    @app.route("/logout")
    def logout():
        """
        Force the user to login, then redirect them to the dashboard.
        """
        return oidc.logout()

    @app.route("/")
    @oidc.require_login
    def index():
        return render_template(
            'summary.html',
            has_write_permission=True
        )

    @app.before_request
    def before_request():
        endpoint = request.endpoint
        if endpoint in secure_views:
            if oidc.user_loggedin:
                g.user = okta_client.get_user(oidc.user_getfield("sub"))
            else:
                return redirect(url_for('open_saturn.index'))

    return app
