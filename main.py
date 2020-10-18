import os
import requests

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/business-status")
def business():
    response = requests.get('https://taller2airbnb-businesscore.herokuapp.com/health')
    return response.json()


@app.route("/health.json")
def health():
    return jsonify({"status": "UP", "from": "Profile"}), 200


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
