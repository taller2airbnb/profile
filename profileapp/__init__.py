import profileapp.database
import profileapp.commands
import os
from flask import Flask
from flask_cors import CORS
from profileapp.status_info import bp_stinfo


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

    CORS(bp_stinfo)  # enable CORS on the bp_stinfo blue print

    @app.before_first_request
    def create_db():
        database.create_tables()

    app.register_blueprint(bp_stinfo)

    return app
