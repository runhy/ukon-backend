from backend.models.base import db
import os
import functools
from flask import g
from backend.apis.exceptions import ApiUserError
from backend.utils.common import ERROR, SUCCESS
from backend.utils.redis import redis_conn
from backend.utils.auth import LoginRegisterValidate, TokenService
from backend.models.user import Users
from datetime import datetime


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        error = TokenService().verify_token()
        if error:
            return error
        return view_func(*args, **kwargs)

    return wrapper


class UserLoginService(object):
    SMS_MAX_COUNT = 5  # message limit per day

    def __init__(self):
        pass

    def login(self, args, platform):
        phone = args.get('phone')
        password = args.get('password')
        if not LoginRegisterValidate(phone).phone_check():
            raise ApiUserError(ERROR.PHONE_ERROR)

        user = Users.get_by_phone_password(phone, Users.md5_password(password))
        if not user or user.status == -100:
            raise ApiUserError(ERROR.PHONE_PASSWORD_ERROR)

        # save token to redis
        token = TokenService().generate_platform_token(user.id, platform, 'access')
        redis_conn.set('user:{}platform:{}:token'.format(user.id, platform), token)
        user.update_last_login()
        user_info = user.info()
        return {'user': user_info, 'token': token}

    @staticmethod
    def logout(platform):
        redis_key = 'user:{}platform:{}:token'.format(g.user.id, platform)
        if redis_conn.exists(redis_key):
            redis_conn.delete(redis_key)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return SUCCESS.LOGIN_EXIT

    @staticmethod
    def reset_password(args):
        phone = args.get('phone')
        password = args.get('password')
        sms_code = args.get('sms_code')

        lrv = LoginRegisterValidate(phone, sms_code)
        if not lrv.phone_check():
            raise ApiUserError(ERROR.PHONE_ERROR)

        if os.getenv('ENV_NAME') == 'production':  # only verify in PROD
            if lrv.sms_code_expired():
                raise ApiUserError(ERROR.SMS_CODE_EXPIRED)

            # is it correct?
            if not lrv.sms_code_check():
                raise ApiUserError(ERROR.SMS_CODE_ERROR)

            # del sms code when verified
            lrv.del_sms_code()
        else:
            if str(sms_code) != '123456':
                raise ApiUserError(ERROR.SMS_CODE_ERROR)

        user = Users.get_by_phone(phone)
        if not user:
            raise ApiUserError("找不到用户")
        user.password = Users.md5_password(password)
        user.update_time = datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ApiUserError(e)

    @staticmethod
    def send_sms_code(phone):
        import random

        sms_code = '%06d' % random.randint(0, 999999)

        # Avoid repeated requests to send codes
        if redis_conn.get('sms_code_flag:%s' % phone):
            raise ApiUserError(ERROR.SMS_CODE_EXIST)
        else:
            # send limit
            UserLoginService().sms_count_check(phone)

            # validity period 300s
            redis_conn.set('sms_code:%s' % phone, sms_code, 300)

            # request limit
            redis_conn.set('sms_code_flag:%s' % phone, phone, 60)

        # celery send message via side service

        return 'ok'

    def sms_count_check(self, phone):

        day_time = datetime.now().strftime('%Y-%m-%d')
        time_stamp = int(datetime.strptime(day_time, '%Y-%m-%d').timestamp())
        phone_key = 'sms:{}:{}'.format(time_stamp, phone)
        if redis_conn.exists(phone_key):
            sms_count = redis_conn.get(phone_key)
            if int(sms_count) >= self.SMS_MAX_COUNT:
                raise ApiUserError(ERROR.SMS_CODE_FULL)
            redis_conn.incr(phone_key, 1)
        else:
            redis_conn.incr(phone_key, 1)
            redis_conn.expire(phone_key, 86400)  # 设置ttl
