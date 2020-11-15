from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app


class UserNotExistentError(ProfileAppException):
    def __init__(self, user_info, message="Not exists User: "):
        current_app.logger.error("The user " + str(user_info) + " does not exist.")
        self.message = message + str(user_info)
        super().__init__(self.message)


class UserIsNotAnAdminError(ProfileAppException):
    def __init__(self, user_info):
        current_app.logger.error("The user " + str(user_info) + " is not an admin")
        self.message = "The User: " + str(user_info) + " is not an admin"
        super().__init__(self.message)


class UserIdentifierAlreadyTaken(ProfileAppException):
    def __init__(self, user_info):
        current_app.logger.error("User identifier is already taken: " + str(user_info))
        self.message = "Some User identifier is already taken: " + str(user_info)
        super().__init__(self.message)


class UserPasswordMustNotBeEmpty(ProfileAppException):
    def __init__(self):
        current_app.logger.error("User password must not be empty")
        self.message = "User Password must not be empty"
        super().__init__(self.message)


class UserPasswordInvalid(ProfileAppException):
    def __init__(self):
        current_app.logger.error("User password is invalid")
        self.message = "User Password is invalid"
        super().__init__(self.message)


class UserMailInvalid(ProfileAppException):
    def __init__(self, user_info):
        current_app.logger.error("The email " + str(user_info) + " is not registered")
        self.message = "The email: " + str(user_info) + " is not registered"
        super().__init__(self.message)


class EmptyModifySchema(ProfileAppException):
    def __init__(self):
        current_app.logger.error("No fields were submitted in the request to modify user.")
        self.message = "No fields were submitted in the request to modify user."
        super().__init__(self.message)
