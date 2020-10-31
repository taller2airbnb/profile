from profileapp.model import Users, Profile, ProfileUser


def test__create_invalid_relation_not_existing_profile(app, database):
    with app.app_context():
        id_u = 1
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

        id_prof = 0

        new_profileUser = ProfileUser(id_user=id_u, id_profile=id_prof)
        try:
            database.session.add(new_profileUser)
        finally:
            database.session.rollback()
            database.session.remove()
        profileUser = ProfileUser.query.first()
        assert profileUser is None

def test__create_invalid_relation_not_existing_user(app, database):
    with app.app_context():
        id_u = 1
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

        id_p = 0
        descrip_p = "Administrador"
        new_profile = Profile(id_profile=id_p, description=descrip_p)
        database.session.add(new_profile)
        database.session.commit()

        new_profileUser = ProfileUser(id_user=id_u, id_profile=id_p)
        database.session.add(new_profileUser)
        database.session.commit()

        profileUser = ProfileUser.query.first()
        assert profileUser.id_user == id_u
        assert profileUser.id_profile == id_p


def test__create_valid_relation(app, database):
    with app.app_context():
        id_u = 1

        id_p = 0
        descrip_p = "Administrador"
        new_profile = Profile(id_profile=id_p, description=descrip_p)
        database.session.add(new_profile)
        database.session.commit()

        new_profileUser = ProfileUser(id_user=id_u, id_profile=id_p)
        try:
            database.session.add(new_profileUser)
        finally:
            database.session.rollback()
            database.session.remove()
        profileUser = ProfileUser.query.first()
        assert profileUser is None
