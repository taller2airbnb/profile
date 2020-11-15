from profileapp.model import Users, Profile, ProfileUser
import hashlib
from profileapp.database import db
from profileapp.Errors import UsersError, ProfileError


def validate_user_password(user_password, stored_password=None):
    if user_password == '':
        raise UsersError.UserPasswordMustNotBeEmpty()
    if stored_password is not None:
        encoded_password = hashlib.md5(user_password.encode()).hexdigest()
        if stored_password != encoded_password:
            raise UsersError.UserPasswordInvalid


def validate_existent_profile_id(profile_id):
    if Profile.query.filter_by(id_profile=profile_id).first() is None:
        raise ProfileError.ProfileNotExistentById(profile_id)


def validate_free_user_identifiers(new_user_mail, new_user_alias=None):
    mail_taken = Users.query.filter_by(email=new_user_mail).first() is not None
    alias_taken = Users.query.filter_by(alias=new_user_alias).first() is not None
    if new_user_alias is None:
        new_user_alias = ''
    if mail_taken or alias_taken:
        raise UsersError.UserIdentifierAlreadyTaken(new_user_mail + " or " + new_user_alias)


def validate_existent_user_by_mail(user_mail):
    mail_taken = Users.query.filter_by(email=user_mail).first() is not None
    if not mail_taken:
        raise UsersError.UserMailInvalid(user_mail)


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


def validate_modify_schema_not_empty(data, fields):
    valid = False
    for field in fields:
        if field in data and data[field] != '':
            valid = True
            break
    if not valid:
        raise UsersError.EmptyModifySchema()
