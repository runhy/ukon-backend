from .abstract import ActionApi
from backend.views.abstract import parse_arguments
from backend.services.user import UserLoginService, login_required
from backend.apis.exceptions import ApiUserError
from backend.utils import UkonArgument as Argument


class UserLoginAPI(ActionApi):
    @parse_arguments(
        Argument("phone", type=str, required=True),
        Argument("password", type=str, required=True),
    )
    def post(self, arguments):
        try:
            data = UserLoginService().login(arguments, 2)
            return self.done(data)
        except ApiUserError as e:
            return self.user_fail(e)

        except Exception as e:
            return self.fail(e)

    @parse_arguments(
        Argument("phone", type=str, required=True),
        Argument("password", type=str, required=True),
        Argument("sms_code", type=str, required=True),
    )
    def patch(self, arguments):
        try:
            data = UserLoginService.reset_password(arguments)
            return self.done(data)
        except ApiUserError as e:
            return self.user_fail(e)
        except Exception as e:
            return self.fail(e)

    @login_required
    def delete(self):
        try:
            data = UserLoginService.logout(platform=2)
            return self.done(data)
        except ApiUserError as e:
            return self.user_fail(e)

        except Exception as e:
            return self.fail(e)


class SendCodeAPI(ActionApi):
    """phone massage"""

    @parse_arguments(Argument("phone", type=str))
    def post(self, arguments):
        try:
            phone = arguments.get("phone")
            data = UserLoginService.send_sms_code(phone)
            return self.done(data)
        except ApiUserError as e:
            return self.user_fail(e)
        except Exception as e:
            return self.fail(e)
