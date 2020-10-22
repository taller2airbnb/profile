from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def create_tables():
    if not current_app.config['TESTING']:
        db.create_all()
