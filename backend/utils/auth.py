import os
import re
from flask import current_app, request, g
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from backend.models.user import Users
from backend.utils.redis import redis_conn
from backend.utils.common import ERROR
from backend.apis.exceptions import ApiUserError


class TokenService(object):
    """
    token服务类
    """

    def __init__(self):
        # token有效期,刷新令牌有效期30天
        self.access_token_expired = 60 * 60 * 24    # 访问token过期时间
        self.refresh_token_expired = 86400 * 30   # 刷新token过期时间
        self.cms_token_expired = 86400
        self.auto_login_token = 86400 * 7
        self.dict = {'access': self.access_token_expired,
                     'refresh': self.refresh_token_expired,
                     'cms': self.cms_token_expired}

    def get_token(self, user_id):
        # 获取用户id，传入生成token的方法，并返回的token
        access_token = self.generate_token(user_id, 'access')
        refresh_token = self.generate_token(user_id, 'refresh')
        return access_token, refresh_token

    def generate_token(self, user_id, expired_type):
        """
        生成验证令牌token，用于保持用户状态
        :param user_id:用户id
        :param expired_type:过期类型,对应不同的过期时间
        :return: token
        """
        # 第一个参数是内部的私钥，这里写在共用的配置信息里
        # 第二个参数是有效期(秒)
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=self.dict.get(expired_type))
        # 接收用户id转换与编码
        token = s.dumps({"id": user_id}).decode("ascii")
        return token

    # def generate_pc_token(self, user_id):
    #     """
    #     生成验证令牌token，用于保持用户状态/pc端
    #     :param user_id:用户id
    #     :return: token
    #     """
    #     # 第一个参数是内部的私钥，这里写在共用的配置信息里
    #     # 第二个参数是有效期(秒)
    #     s = Serializer(current_app.config["SECRET_KEY"], expires_in=self.cms_token_expired)
    #     # 接收用户id转换与编码
    #     token = s.dumps({"id": user_id, 'login': 'pc'}).decode("ascii")
    #     return token

    # def generate_h5_token(self, user_id):
    #     """
    #     生成验证令牌token，用于保持用户状态/h5端
    #     :param user_id:用户id
    #     :return: token
    #     """
    #     # 第一个参数是内部的私钥，这里写在共用的配置信息里
    #     # 第二个参数是有效期(秒)
    #     s = Serializer(current_app.config["SECRET_KEY"], expires_in=self.cms_token_expired)
    #     # 接收用户id转换与编码
    #     token = s.dumps({"id": user_id, 'login': 'h5'}).decode("ascii")
    #     return token

    def generate_cms_token(self, user_id, phone, expired_type):
        """
        生成验证令牌token，用于保持用户状态
        :param user_id:用户id
        :param phone:用户手机
        :param expired_type:过期类型,对应不同的过期时间
        :return: token
        """
        # 第一个参数是内部的私钥，这里写在共用的配置信息里
        # 第二个参数是有效期(秒)
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=self.dict.get(expired_type))
        # 接收用户id转换与编码
        token = s.dumps({"id": user_id, "phone": phone}).decode("ascii")
        return token

    def generate_platform_token(self, user_id, platform, expired_type):
        """
        生成验证令牌token，用于保持用户状态
        :param user_id:用户id
        :param platform:用户手机
        :param expired_type:过期类型,对应不同的过期时间
        :return: token
        """
        # 第一个参数是内部的私钥，这里写在共用的配置信息里
        # 第二个参数是有效期(秒)
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=self.dict.get(expired_type))
        # 接收用户id转换与编码
        token = s.dumps({"id": user_id, "platform": platform}).decode("ascii")
        return token

    def generate_auto_token(self, user_id, user_phone):
        """
        自动登录生成验证令牌token，用于保持用户状态
        :param user_id:用户id
        :param user_phone:用户手机号
        :return: token
        """
        # 第一个参数是内部的私钥，这里写在共用的配置信息里
        # 第二个参数是有效期(秒)
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=self.auto_login_token)
        # 接收用户id转换与编码
        token = s.dumps({"id": user_id, "phone": user_phone}).decode("ascii")
        return token

    def refresh(self, refresh_token):
        """刷新token有效期"""
        self.verify_refresh_token(refresh_token)
        # 验证通过，获得token
        access_token, refresh_token = TokenService().get_token(g.user.id)
        redis_conn.set('user:{}:token'.format(g.user.id), access_token)   # 将新token放入redis中
        data = {'access_token': access_token, 'refresh_token': refresh_token}
        return data

    @staticmethod
    def verify_refresh_token(token):
        """验证刷新token"""

        # 初始化
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
            u_id = data["id"]
            user = Users.get_by_id(u_id)
            g.user = user
        # 令牌过期
        except SignatureExpired:
            raise ApiUserError(**ERROR.REFRESH_TOKEN_EXPIRED)

        # 刷新令牌被篡改，无效token
        except BadSignature:
            raise ApiUserError(**ERROR.INVALID_TOKEN)

        except Exception as e:
            # 未知错误
            raise ApiUserError(ERROR.UNKNOWN_ERROR)

    def verify_token(self, cms=False):
        """验证token"""
        try:
            # 在请求头上拿到token
            token = request.headers["Authorization"]
        except Exception as e:
            # 没接收的到token,给前端提示
            return TokenService.error(**ERROR.TOKEN_NEED)
            # raise ApiUserError(**ERROR.TOKEN_NEED)
        # 初始化
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
            if cms:  # cms用户
                user = Users.get_by_id(data["id"])
                if not user:
                    return self.error(ERROR.USER_NULL)
            else:  # app用户
                u_id = data["id"]
                if data.get('platform') == 2:  # pc端登陆
                    pass
                else:
                    redis_key = 'user:{}platform:{}:token'.format(u_id, data.get('platform'))
                    if not redis_conn.exists(redis_key):
                        return self.error(**ERROR.LOGIN_EXPIRED)
                    if token != redis_conn.get(redis_key):
                        return self.error(**ERROR.USER_LOGINED)
                user = Users.get_by_id(u_id)
            g.user = user
        # 令牌过期
        except SignatureExpired:
            return self.error(**ERROR.LOGIN_EXPIRED)

        # 刷新令牌被篡改，无效token
        except BadSignature:
            return self.error(**ERROR.INVALID_TOKEN)
        except Exception as e:
            # 未知错误
            return self.error(ERROR.UNKNOWN_ERROR)


    @staticmethod
    def error(message='', status_code=400, user_id=0):
        data = {
            "success": False,
            "message": message,
            "code": status_code
        }
        if user_id:
            data.update({'user_id': user_id})

        return data


class LoginRegisterValidate(object):
    """
    注册/登录验证类
    """

    def __init__(self, phone, sms_code=''):
        self.phone = phone
        self.sms_code = sms_code
        self.prefix = "sms_code:"
        self.flag_prefix = "sms_code_flag:"

    def phone_check(self):
        """
        手机格式验证
        :return:
        """
        res = re.match(r"^1[3456789]\d{9}$", self.phone)
        return True if res else False

    def get_sms_code(self):
        """
        获取redis中验证码
        :return:
        """
        return redis_conn.get(self.prefix + self.phone)

    def sms_code_expired(self):
        """
        验证码是否过期
        :return:
        """
        return False if self.get_sms_code() else True

    def sms_code_check(self):
        """
        验证码是否一致
        :return:
        """
        redis_sms_code = self.get_sms_code()
        if self.sms_code != redis_sms_code:
            return False
        return True

    def del_sms_code(self):
        """
        删除验证码
        :return:
        """
        redis_conn.delete(self.prefix + self.phone)
        redis_conn.delete(self.flag_prefix + self.phone)

    def check_sms_code(self):
        if not self.phone_check():
            raise ApiUserError(ERROR.PHONE_ERROR)
        # 验证码是否过期
        if os.getenv('ENV_NAME') == 'production':  # 生产环境
            if self.sms_code_expired():
                raise ApiUserError(ERROR.SMS_CODE_EXPIRED)
            # 验证码是否正确
            if not self.sms_code_check():
                raise ApiUserError(ERROR.SMS_CODE_ERROR)
            # 验证结束删除验证码
            self.del_sms_code()
        else:
            if self.sms_code != '123456':
                raise ApiUserError(ERROR.SMS_CODE_ERROR)