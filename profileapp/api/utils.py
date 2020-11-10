from profileapp.model import Users, Profile, ProfileUser
import hashlib
from profileapp.database import db
from profileapp.Errors import UsersError, ProfileError
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
    profile_description = Profile.query.filter_by(id_profile=new_user_profile).first().description
    return 'admin' in profile_description.lower()


def validate_user_id_exists(user_id):
    exists = db.session.query(db.exists().where(Users.id_user == user_id)).scalar()
    if not exists:
        raise UsersError.UserNotExistentError(user_id)
    return exists


def get_profile_from_user_id(user_id):
    validate_user_id_exists(user_id)
    return ProfileUser.query.filter_by(id_user=user_id).first().id_profile


def get_id_profile_from_description(profile_description):
    id_profile = Profile.query.filter_by(description=profile_description).first().id_profile
    if id_profile is None:
        raise ProfileError.ProfileNotExistentByDescription(profile_description)
    return id_profile


def validate_user_is_admin(user_id):
    if not (profile_is_admin(get_profile_from_user_id(user_id))):
        raise UsersError.UserIsNotAnAdminError(user_id)
