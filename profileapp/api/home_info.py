from profileapp import database
from profileapp.model import Users
import requests
from flask import Blueprint
from flask import jsonify, render_template

bp_homeinfo = Blueprint('status_info', __name__, url_prefix='/')


@bp_homeinfo.route("/")
def home():
    return render_template("home.html")


@bp_homeinfo.route("/business-status")
def business():
    response = requests.get('https://taller2airbnb-businesscore.herokuapp.com/health')
    return response.json()


@bp_homeinfo.route("/health")
def health():
    return jsonify({"status": "UP", "from": "Profile"}), 200
