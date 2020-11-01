from sqlalchemy import event, DDL
from profileapp.model import Profile

import profileapp.database
import profileapp.commands
import os
from flask import Flask
from flask_cors import CORS
from profileapp.api.home_info import bp_homeinfo
from profileapp.api.register import bp_register
from profileapp.api.profiles import bp_profiles
from profileapp.api.login import bp_login


def create_app():
    # setup app
    app = Flask(__name__)
    # setup CORS
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # setup with the configuration provided by the user / environment
    app.config.from_object(os.environ['APP_SETTINGS'])
    # setup all our dependencies, for now only database using application factory pattern
    database.init_app(app)
    commands.init_app(app)

    CORS(bp_homeinfo)  # enable CORS on the bp_stinfo blue print
    CORS(bp_register)
    CORS(bp_profiles)
    CORS(bp_login)

    # event.listen(Profile.__table__, 'after_create', DDL(""" INSERT INTO profile (id_profile, description) VALUES (
    # 0, 'admin'), (1, 'anfitrion'), (2, 'huesped') """))

    @app.before_first_request
    def create_db():
        database.create_tables()

    app.register_blueprint(bp_homeinfo)
    app.register_blueprint(bp_register)
    app.register_blueprint(bp_profiles)
    app.register_blueprint(bp_login)

    return app
