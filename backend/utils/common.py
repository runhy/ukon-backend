import requests
from functools import wraps


_BLOCK_SIZE = 1024 * 1024 * 10


# 自定义的枚举
def enum(**status):
    return type('Enum', (), status)


# 错误信息
ERROR = enum(LOGIN_ERROR='LOGIN_ERROR',
             PHONE_ERROR='WRONG PHONE NUMBER',
             PHONE_PASSWORD_ERROR='WRONG PHONE OR PASSWORD',
             NAME_ERROR='WRONG ACCOUNT',
             PASSWORD_ERROR='WRONG PASSWORD',
             NAMW_PASSWORD_ERROR='WRONG NAME OR PASSWORD',
             NOT_CONFIRMED='NOT_CONFIRMED',
             USER_NAME_EXIST='USER_NAME_EXIST',
             USER_ERROR='USER_ERROR',
             PARAMS_ERROR='PARAMS_ERROR',
             PARAMS_FAIL='PARAMS_FAIL',
             BAD_PARAMS='BAD_PARAMS',
             PHONE_EXIST='PHONE_EXIST',
             PHONE_NULL='PHONE_NULL',
             USER_NULL='USER NOT FOUND',
             PASSWORD_ERROR_1='TWO PASSWORD WAS NOT MATCH',
             TOKEN_NEED={'message': 'TOKEN_NEED', 'status_code': 1001},
             LOGIN_EXPIRED={'message': 'LOGIN_EXPIRED', 'status_code': 1002},
             INVALID_TOKEN={'message': 'INVALID_TOKEN', 'status_code': 1003},
             USER_LOGINED={'message': 'USER_HAS_LOGIN', 'status_code': 1004},
             USER_IN_BLACKLIST={'message': 'USER_IN_BLACKLIST', 'status_code': 1005},
             REFRESH_TOKEN_EXPIRED={'message': 'REFRESH_TOKEN_EXPIRED', 'status_code': 1006},
             PRINT_LOG_ERROR={'message': 'PRINT_LOG_ERROR', 'status_code': 100500},
             SMS_CODE_EXISTS='SMS_CODE_EXISTS',
             SMS_CODE_EXPIRED='SMS_CODE_EXPIRED',
             SMS_CODE_ERROR='SMS_CODE_ERROR',
             SMS_CODE_FULL='SMS_CODE_FULL',
             UNKNOWN_ERROR='UNKNOWN_ERROR',
             )

# 成功信息
SUCCESS = enum(USER_ADDED='USER_ADDED',
               ADD_OK='ADD_OK',
               GET_OK='GET_OK',
               PATCH_OK='PATCH_OK',
               DELETE_OK='DELETE_OK',
               LOGIN_SUCCESS='LOGIN_SUCCESS',
               LOGIN_EXIT='LOGIN_EXIT',
               OPERATE_SUCCESS='OPERATE_SUCCESS',
               UPDATE_SUCCESS='UPDATE_SUCCESS'
               )

STATUS = enum(NORMAL=0, DELETE=-100)

ADMIN = enum(YES=1, NO=0)
