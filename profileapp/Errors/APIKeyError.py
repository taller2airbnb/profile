from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app


class APIKeyNotExistent(ProfileAppException):
    def __init__(self, profile_info, message="Invalid API Key: "):
        current_app.logger.error("API Key " + profile_info + ' does not exist.')
        self.message = message + str(profile_info)
        self.error_code = 401
        super().__init__(self.message, self.error_code)
