from profileapp.Errors.ProfileAppException import ProfileAppException


class UserNotExistentError(ProfileAppException):
    def __init__(self, user_info, message="Not exists User: "):
        self.message = message + str(user_info)
        super().__init__(self.message)


class UserIsNotAnAdminError(ProfileAppException):
    def __init__(self, user_info):
        self.message = "The User: " + str(user_info) + " is not an admin"
        super().__init__(self.message)
