from profileapp.database import db
from profileapp.model import Users


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def create_model_table():
    """ Create table model in the database """
    Users.__table__.create(db.engine)


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, create_model_table]:
        app.cli.add_command(app.cli.command()(command))