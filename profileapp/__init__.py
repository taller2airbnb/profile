import profileapp.model
import profileapp.database
import profileapp.commands
import os
from flask import Flask
from flask_cors import CORS
from profileapp.api.home_info import bp_homeinfo
from profileapp.api.profiles import bp_profiles
from profileapp.api.login import bp_login
from profileapp.api.change_password import bp_change_password
from profileapp.api.user import bp_user
from flasgger import Swagger
import logging


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

    CORS(bp_homeinfo)  # enable CORS on the bp_stinfo blue print
    CORS(bp_profiles)
    CORS(bp_login)
    CORS(bp_change_password)
    CORS(bp_user)

    @app.before_first_request
    def create_db():
        database.create_tables()
        model.insert_initial_values()

    app.register_blueprint(bp_homeinfo)
    app.register_blueprint(bp_profiles)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_change_password)
    app.register_blueprint(bp_user)

    # setup swagger
    swagger = Swagger(app)

    # setup logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.logger.info('New session started. Database up and running')

    return app
