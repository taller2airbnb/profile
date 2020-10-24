from profile.model import Users
import profile.database
import profile.commands
import os
import requests
from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# setup with the configuration provided by the user / environment
app.config.from_object(os.environ['APP_SETTINGS'])
# setup all our dependencies, for now only database using application factory pattern
database.init_app(app)
commands.init_app(app)


@app.before_first_request
def create_db():
    database.create_tables()


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/add/<string:item>", methods=['POST'])
def add_new_item(item):
    model = Users(name=item)

    # add to the database session
    database.db.session.add(model)

    # commit to persist into the database
    database.db.session.commit()

    return jsonify({"success": model.name})


@app.route("/business-status")
@cross_origin()
def business():
    response = requests.get('https://taller2airbnb-businesscore.herokuapp.com/health')
    return response.json()


@app.route("/health")
@cross_origin()
def health():
    return jsonify({"status": "UP", "from": "Profile"}), 200


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
