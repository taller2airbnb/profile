from profileapp.model import Users, Profile, ProfileUser


def test__create_invalid_relation_non_existing_profile(app, database):
    with app.app_context():
        id_u = 1
        new_user = Users(first_name='Gonza', last_name='Apellido', email='algo@algo.com', password='123456789', national_id='12345678',
                         national_id_type='DNI', alias='gonzalgo')
        database.session.add(new_user)
        database.session.commit()

        id_prof = 0

        new_profile_user = ProfileUser(id_user=id_u, id_profile=id_prof)
        try:
            database.session.add(new_profile_user)
        finally:
            database.session.rollback()
            database.session.remove()
        profile_user = ProfileUser.query.first()
        assert profile_user is None

def test__create_invalid_relation_non_existing_user(app, database):
    with app.app_context():
        id_u = 1

        new_user = Users(first_name='Gonza', last_name='Apellido', email='algo@algo.com', password='123456789', national_id='12345678',
                         national_id_type='DNI', alias='gonzalgo')
        database.session.add(new_user)
        database.session.commit()

        id_p = 0
        description_p = "Administrador"
        new_profile = Profile(id_profile=id_p, description=description_p)
        database.session.add(new_profile)
        database.session.commit()

        new_profile_user = ProfileUser(id_user=id_u, id_profile=id_p)
        database.session.add(new_profile_user)
        database.session.commit()

        profile_user = ProfileUser.query.first()
        assert profile_user.id_user == id_u
        assert profile_user.id_profile == id_p


def test__create_valid_relation(app, database):
    with app.app_context():
        id_u = 1

        id_p = 0
        description_p = "Administrador"
        new_profile = Profile(id_profile=id_p, description=description_p)
        database.session.add(new_profile)
        database.session.commit()

        new_profile_user = ProfileUser(id_user=id_u, id_profile=id_p)
        try:
            database.session.add(new_profile_user)
        finally:
            database.session.rollback()
            database.session.remove()
        profile_user = ProfileUser.query.first()
        assert profile_user is None
