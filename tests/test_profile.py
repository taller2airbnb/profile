from profileapp.model import Profile


def test__create_valid_profile(app, database):
    with app.app_context():
        id_p = 0
        descrip_p = "Administrador"
        new_profile = Profile(id_profile=id_p, description=descrip_p)
        database.session.add(new_profile)
        database.session.commit()
        profile = Profile.query.first()
        assert profile.description == descrip_p


def test__try_create_duplicate_profile(app, database):
    with app.app_context():
        id_p = 0
        descrip_p = "Administrador"
        new_profile = Profile(id_profile=id_p, description=descrip_p)
        database.session.add(new_profile)
        database.session.commit()

        id_p2 = 1
        descrip_p2 = "Administrador"
        new_profile2 = Profile(id_profile=id_p2, description=descrip_p2)

        try:
            database.session.add(new_profile2)
            # database.session.commit()
        finally:
            database.session.rollback()
            database.session.remove()
        profile = Profile.query.first()
        assert profile.id_profile == id_p
