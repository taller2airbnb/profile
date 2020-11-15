from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app


class ProfileNotExistentByDescription(ProfileAppException):
    def __init__(self, profile_info, message="Not exists Profile by description: "):
        current_app.logger.error("Profile with description " + profile_info + ' does not exist.')
        self.message = message + str(profile_info)
        super().__init__(self.message)


class ProfileNotExistentById(ProfileAppException):
    def __init__(self, profile_info, message="Not exists Profile by id: "):
        current_app.logger.error("Profile with id " + str(profile_info) + ' does not exist.')
        self.message = message + str(profile_info)
        super().__init__(self.message)
