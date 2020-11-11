from profileapp.Errors.ProfileAppException import ProfileAppException


class ProfileNotExistentByDescription(ProfileAppException):
    def __init__(self, profile_info, message="Not exists Profile by description: "):
        self.message = message + str(profile_info)
        super().__init__(self.message)


class ProfileNotExistentById(ProfileAppException):
    def __init__(self, profile_info, message="Not exists Profile by id: "):
        self.message = message + str(profile_info)
        super().__init__(self.message)
