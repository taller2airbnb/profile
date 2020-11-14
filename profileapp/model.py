import hashlib
import os

from flask import current_app
from profileapp.database import db


class Users(db.Model):
    # __tablename__= 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    national_id = db.Column(db.String(50))
    national_id_type = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    blocked = db.Column(db.BOOLEAN, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"User: {self.first_name}"


class Profile(db.Model):
    # __tablename__ = 'profile'

    id_profile = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Profile: {self.description}"


class ProfileUser(db.Model):
    # __tablename__ = 'profile_user'

    id_profile = db.Column(db.Integer, db.ForeignKey('profile.id_profile'), primary_key=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"User Profile: {self.id_user, self.id_profile}"


def insert_initial_values():
    if not current_app.config['TESTING']:
        #Profiles
        db.session.add(Profile(id_profile=0, description='admin'))
        db.session.add(Profile(id_profile=1, description='anfitrion'))
        db.session.add(Profile(id_profile=2, description='huesped'))
        db.session.commit()
        # User
        password = os.environ.get('ADM_PASS')
        if password is None:
            password = 'test'
        password = hashlib.md5(password.encode()).hexdigest()
        db.session.add(Users(first_name='norbert', last_name='degoas', email='buenosaires@elcondor.mardelplata',
                             password=password, national_id='99999999', national_id_type='DNI',
                             alias='norbertdegoas'))
        db.session.commit()
        # Profile User
        db.session.add(ProfileUser(id_user=1, id_profile=0))
        db.session.commit()
