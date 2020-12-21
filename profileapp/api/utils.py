from datetime import datetime

from profileapp.model import Users, Profile, ProfileUser, RecoverUserToken
import hashlib
from profileapp.database import db
from profileapp.Errors import UsersError, ProfileError
from profileapp.api import valid_user_types


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


def get_email_from_user_id(user_id):
    validate_user_id_exists(user_id)
    return Users.query.filter_by(id_user=user_id).first().email


def get_user_id_from_mail(user_mail):
    validate_existent_user_by_mail(user_mail)
    return Users.query.filter_by(email=user_mail).first().id_user


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


def validate_user_type(user_type):
    if user_type not in valid_user_types:
        raise UsersError.UserTypeNotExistentError(user_type)


def validate_google_response(response):
    if "error" in response:
        raise UsersError.UserGoogleValidateFailed()


def validate_is_google_user(user):
    if user.password is not None:
        raise UsersError.UserIsNotGoogleUserError()


def validate_is_not_google_user_by_id(user_id):
    user = Users.query.filter_by(id_user=user_id).first()
    if user.password is None:
        raise UsersError.UserIsGoogleUserError()


def validate_user_not_blocked(user_id):
    if Users.query.filter_by(id_user=user_id).first().blocked:
        raise UsersError.UserIsBlockedError(user_id)


def validate_password_recovery(user_id, token):
    recover_token_entry = RecoverUserToken.query.filter_by(id_user=user_id).first()
    recover_token_str = recover_token_entry.recover_token
    time_elapsed = datetime.now() - recover_token_entry.date_created
    if recover_token_str != token:
        raise UsersError.UserTokenRecoverError(user_id)
    if time_elapsed.total_seconds() > 5*60:
        raise UsersError.UserTokenRecoverExpiredError(user_id)
