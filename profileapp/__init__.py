import logging
import os

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail

import profileapp.commands
import profileapp.database
import profileapp.model
from profileapp.api.home_info import bp_homeinfo
from profileapp.api.login import bp_login
from profileapp.api.profiles import bp_profiles
from profileapp.api.user import bp_user
from profileapp.api.recover_token import bp_recover_token
from profileapp.api.apikey import bp_apikey
from profileapp.api.db_manage import bp_db_manage


def create_app(my_config=None):
    # setup app
    app = Flask(__name__)
    # setup CORS
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # setup with the configuration provided by the user / environment
    if my_config is None:
        app.config.from_object(os.environ['APP_SETTINGS'])
    else:
        app.config.from_object(my_config)
    # setup all our dependencies, for now only database using application factory pattern
    database.init_app(app)
    commands.init_app(app)

    # setup mail sender
    mail = Mail(app)

    CORS(bp_homeinfo)  # enable CORS on the bp_stinfo blue print
    CORS(bp_profiles)
    CORS(bp_login)
    CORS(bp_user)
    CORS(bp_recover_token)
    CORS(bp_apikey)
    CORS(bp_db_manage)

    @app.before_first_request
    def create_db():
        database.create_tables()

    #    model.insert_initial_values()

    app.register_blueprint(bp_homeinfo)
    app.register_blueprint(bp_profiles)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_recover_token)
    app.register_blueprint(bp_apikey)
    app.register_blueprint(bp_db_manage)

    # setup swagger
    SWAGGER_TEMPLATE = {
        "securityDefinitions": {"APIKeyHeader": {"type": "apiKey", "name": "Token", "in": "header"}}}

    swagger = Swagger(app, template=SWAGGER_TEMPLATE)

    # setup logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.logger.info('New session started. Database up and running')

    return app