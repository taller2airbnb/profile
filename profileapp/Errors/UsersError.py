from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app


class UserNotExistentError(ProfileAppException):
    def __init__(self, user_info, message="Not exists User: "):
        current_app.logger.error("The user " + str(user_info) + " does not exist.")
        self.message = message + str(user_info)
        self.error_code = 404
        super().__init__(self.message, self.error_code)


class UserIsNotAnAdminError(ProfileAppException):
    def __init__(self, user_info):
        current_app.logger.error("The user " + str(user_info) + " is not an admin")
        self.message = "The User: " + str(user_info) + " is not an admin"
        self.error_code = 403
        super().__init__(self.message, self.error_code)


class UserIdentifierAlreadyTaken(ProfileAppException):
    def __init__(self, user_info):
        current_app.logger.error("User identifier is already taken: " + str(user_info))
        self.message = "Some User identifier is already taken: " + str(user_info)
        self.error_code = 403
        super().__init__(self.message, self.error_code)


class UserPasswordMustNotBeEmpty(ProfileAppException):
    def __init__(self):
        current_app.logger.error("User password must not be empty")
        self.message = "User Password must not be empty"
        self.error_code = 409
        super().__init__(self.message, self.error_code)


class UserPasswordInvalid(ProfileAppException):
    def __init__(self):
        current_app.logger.error("User password is invalid")
        self.message = "User Password is invalid"
        self.error_code = 401
        super().__init__(self.message, self.error_code)


class UserMailInvalid(ProfileAppException):
    def __init__(self, user_info):
        current_app.logger.error("The email " + str(user_info) + " is not registered")
        self.message = "The email: " + str(user_info) + " is not registered"
        self.error_code = 401
        super().__init__(self.message, self.error_code)


class EmptyModifySchema(ProfileAppException):
    def __init__(self):
        current_app.logger.error("No fields were submitted in the request to modify user.")
        self.message = "No fields were submitted in the request to modify user."
        self.error_code = 409
        super().__init__(self.message, self.error_code)


class UserTypeNotExistentError(ProfileAppException):
    def __init__(self, user_info, message="Not exists UserType: "):
        current_app.logger.error("The user type " + str(user_info) + " does not exist.")
        self.message = message + str(user_info)
        self.error_code = 404
        super().__init__(self.message, self.error_code)


class UserGoogleValidateFailed(ProfileAppException):
    def __init__(self):
        current_app.logger.error('Not able to validate token with GoogleAPI')
        self.message = 'Not able to validate token with GoogleAPI'
        self.error_code = 401
        super().__init__(self.message, self.error_code)


class UserIsNotGoogleUserError(ProfileAppException):
    def __init__(self):
        current_app.logger.error('User register without Google Auth')
        self.message = 'User register without Google Auth'
        self.error_code = 403
        super().__init__(self.message, self.error_code)


class UserIsGoogleUserError(ProfileAppException):
    def __init__(self):
        current_app.logger.error('User register with Google Auth cant recover password')
        self.message = 'User register with Google Auth cant recover password'
        self.error_code = 403
        super().__init__(self.message, self.error_code)


class UserIsBlockedError(ProfileAppException):
    def __init__(self, user_info, message="User is blocked: "):
        current_app.logger.error("The user " + str(user_info) + " is blocked.")
        self.message = message + str(user_info)
        self.error_code = 403
        super().__init__(self.message, self.error_code)


class UserTokenRecoverError(ProfileAppException):
    def __init__(self, user_info, message="Token recover invalid"):
        current_app.logger.error("The token for user: " + str(user_info) + " is invalid.")
        self.message = message + str(user_info)
        self.error_code = 403
        super().__init__(self.message, self.error_code)


class UserTokenRecoverExpiredError(ProfileAppException):
    def __init__(self, user_info, message="Time for token recover expired"):
        current_app.logger.error("Time for token recover expired for user: " + str(user_info))
        self.message = message + str(user_info)
        self.error_code = 403
        super().__init__(self.message, self.error_code)