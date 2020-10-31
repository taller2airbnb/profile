from sqlalchemy.exc import IntegrityError

from profileapp.model import Users


def test__try_create_invalid_user_error(app, database):
    with app.app_context():
        email = "some.email@server.com"
        new_user = Users(email=email)
        try:
            database.session.add(new_user)
            # database.session.commit()
        finally:
            database.session.rollback()
            database.session.remove()
        user = Users.query.first()
        assert user is None


def test__create_valid_user(app, database):
    with app.app_context():
        name = 'Gonza'
        email = 'algo@algo.com'
        password = '123456789'
        national_id = '12345678'
        national_id_type = 'DNI'
        alias = 'gonzalgo'
        new_user = Users(name=name, email=email, password=password, national_id=national_id,
                     national_id_type=national_id_type, alias=alias)
        database.session.add(new_user)
        database.session.commit()
        user = Users.query.first()
        assert user.email == email

def test__try_duplicate_alias_error(app, database):
    with app.app_context():
        name = 'Gonza'
        email = 'algo@algo.com'
        password = '123456789'
        national_id = '12345678'
        national_id_type = 'DNI'
        alias = 'gonzalgo'
        new_user = Users(name=name, email=email, password=password, national_id=national_id,
                     national_id_type=national_id_type, alias=alias)
        database.session.add(new_user)
        database.session.commit()

        name2 = 'otroNombre'
        email2 = 'otroMail@algo.com'
        password2 = 'otropass'
        national_id2 = '884734829'
        national_id_type2 = 'DNI'
        alias2 = 'gonzalgo'
        user2 = Users(name=name2, email=email2, password=password2, national_id=national_id2,
                     national_id_type=national_id_type2, alias=alias2)

        try:
            database.session.add(user2)
        finally:
            database.session.rollback()
            database.session.remove()
        user = Users.query.first()
        assert user.email == email

