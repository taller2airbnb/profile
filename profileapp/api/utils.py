from profileapp.model import Users, Profile, ProfileUser
import hashlib

# common functions used by  the other blueprints


def user_password_empty(new_user_password):
    return new_user_password == ''


def profile_exists(new_user_profile):
    return Profile.query.filter_by(id_profile=new_user_profile).first() is not None


def user_exists(new_user_mail, new_user_alias=None):
    if not Users.query.filter_by(email=new_user_mail).first() is None:
        return True
    if new_user_alias is not None:
        if not Users.query.filter_by(alias=new_user_alias).first() is None:
            return True
    return False


def correct_password(password_login, user_password):
    login_password = hashlib.md5(password_login.encode()).hexdigest()
    return user_password == login_password


def profile_is_admin(new_user_profile):
    profile_description = Profile.query.filter_by(id_profile=0).first().description
    return 'admin' in profile_description.lower()
