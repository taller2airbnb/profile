from profile.database import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User: {self.name}"
