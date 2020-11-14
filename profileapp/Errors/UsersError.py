from profileapp.Errors.ProfileAppException import ProfileAppException


class UserNotExistentError(ProfileAppException):
    def __init__(self, user_info, message="Not exists User: "):
        self.message = message + str(user_info)
        super().__init__(self.message)


class UserIsNotAnAdminError(ProfileAppException):
    def __init__(self, user_info):
        self.message = "The User: " + str(user_info) + " is not an admin"
        super().__init__(self.message)


class UserIdentifierAlreadyTaken(ProfileAppException):
    def __init__(self, user_info):
        self.message = "Some User identifier is already taken: " + str(user_info)
        super().__init__(self.message)


class UserPasswordMustNotBeEmpty(ProfileAppException):
    def __init__(self):
        self.message = "User Password must not be empty"
        super().__init__(self.message)


class UserPasswordInvalid(ProfileAppException):
    def __init__(self):
        self.message = "User Password is invalid"
        super().__init__(self.message)


class UserMailInvalid(ProfileAppException):
    def __init__(self, user_info):
        self.message = "The email: " + str(user_info) + " is not registered"
        super().__init__(self.message)