from profileapp.model import Users


def test__try_create_invalid_user_error(app, database):
    with app.app_context():
        email = "some.email@server.com"
        new_user = Users(email=email)
        try:
            database.session.add(new_user)
        finally:
            database.session.rollback()
            database.session.remove()
        user = Users.query.first()
        assert user is None


def test__create_valid_user(app, database):
    with app.app_context():
        email = 'algo@algo.com'

        new_user = Users(name='Gonza', email=email, password='123456789', national_id='12345678',
                         national_id_type='DNI', alias='gonzalgo')
        database.session.add(new_user)
        database.session.commit()
        user = Users.query.first()
        assert user.email == email


def test__try_duplicate_alias_error(app, database):
    with app.app_context():

        email = 'algo@algo.com'

        new_user = Users(name='Gonza', email=email, password='123456789', national_id='12345678',
                         national_id_type='DNI', alias='gonzalgo')
        database.session.add(new_user)
        database.session.commit()

        user2 = Users(name='otroNombre', email='otroMail@algo.com', password='otropass', national_id='884734829',
                      national_id_type='DNI', alias='gonzalgo')

        try:
            database.session.add(user2)
        finally:
            database.session.rollback()
            database.session.remove()
        user = Users.query.first()
        assert user.email == email

