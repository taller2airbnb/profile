from profileapp.database import db


class Users(db.Model):

    #__tablename__= 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    national_id = db.Column(db.String(50))
    national_id_type = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    blocked = db.Column(db.BOOLEAN, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"User: {self.name}"


class Profile(db.Model):

    #__tablename__ = 'profile'

    id_profile = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Profile: {self.description}"


class ProfileUser(db.Model):

    #__tablename__ = 'profile_user'

    id_profile = db.Column(db.Integer, db.ForeignKey('profile.id_profile'), primary_key=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"User Profile: {self.id_user, self.id_profile}"
