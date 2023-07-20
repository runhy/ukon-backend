

class WebException(Exception):
    status_code = 400


class UserError(WebException):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None, user_id=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or self.status_code
        self.payload = payload
        if user_id:
            self.user_id = user_id

    def as_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['message'] = self.message
        rv['code'] = self.status_code
        return rv


class ApiUserError(UserError):
    status_code = 10400
