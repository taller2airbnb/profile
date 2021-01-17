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
    push_token = db.Column(db.String(255))

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


class RecoverUserToken(db.Model):

    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True, nullable=False)
    recover_token = db.Column(db.String(32), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Token Generated for user: {self.id_user}"


class APIKeyToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_from = db.Column(db.String(80), nullable=False)
    api_key_token = db.Column(db.String(32), nullable=False)
    active = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
        return f"Api Token Generated for: {self.name_from}"


def insert_initial_values():
    api_token_bc = os.environ.get('API_BC')
    if api_token_bc is None:
        api_token_bc = 'test'

    api_token_bo = os.environ.get('API_BO')
    if api_token_bo is None:
        api_token_bo = 'test'

    db.session.add(APIKeyToken(id=0, name_from='BusinessCore', api_key_token=str(api_token_bc), active=True))
    db.session.add(APIKeyToken(id=1, name_from='BackOffice', api_key_token=str(api_token_bo), active=True))
    db.session.commit()

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
        db.session.add(Users(first_name='Norbert', last_name='Degoas', email='buenosaires@elcondor.mardelplata',
                             password=password, national_id='99999999', national_id_type='DNI',
                             alias='norbertdegoas'))
        db.session.add(Users(first_name='Steven', last_name='Seagal', email='steven@seagal.com',
                             password=password, national_id='88888888', national_id_type='DNI',
                             alias='stevenseagal'))
        db.session.add(Users(first_name='John', last_name='McClane', email='hard@to.kill',
                             password=password, national_id='77777777', national_id_type='DNI',
                             alias='hardtokill'))
        db.session.add(Users(first_name='Michael', last_name='Scott', email='michael@scott.com',
                             password=password, national_id='77777777', national_id_type='DNI',
                             alias='michaelscott'))
        db.session.commit()
        # Profile User
        db.session.add(ProfileUser(id_user=1, id_profile=0))
        db.session.add(ProfileUser(id_user=2, id_profile=1))
        db.session.add(ProfileUser(id_user=3, id_profile=2))
        db.session.add(ProfileUser(id_user=4, id_profile=2))
        db.session.commit()



