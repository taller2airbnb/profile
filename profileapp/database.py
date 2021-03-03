from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def create_tables():
    if current_app.config['START_DB']:
        db.create_all()
    if current_app.config['TESTING']:
        db.drop_all()
        db.create_all()


def drop_and_create_tables():
    if current_app.config['START_DB']:
        db.drop_all()
        db.create_all()
