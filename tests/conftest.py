import pytest

from profileapp import create_app
from profileapp.database import db


@pytest.fixture
def app():
    app = create_app()
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'

    return app


@pytest.fixture(scope="function")
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db
