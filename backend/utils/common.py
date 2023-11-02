_BLOCK_SIZE = 1024 * 1024 * 10


# error message
class ERROR:
    LOGIN_ERROR = "Login error"
    PHONE_ERROR = "Wrong phone number"
    PHONE_PASSWORD_ERROR = "Wrong phone or password"
    NAME_ERROR = "Wrong account"
    PASSWORD_ERROR = "Wrong password"
    NAME_PASSWORD_ERROR = "Wrong name or password"
    NOT_CONFIRMED = "Not confirmed"
    USER_NAME_EXIST = "Username already exists"
    USER_ERROR = "User error"
    PARAMS_ERROR = "Parameters error"
    PARAMS_FAIL = "Parameters fail"
    BAD_PARAMS = "Bad parameters"
    PHONE_EXIST = "Phone number already exists"
    PHONE_NULL = "Phone number is null"
    USER_NULL = "User not found"
    PASSWORD_CONFIRM_ERROR = "Passwords do not match"
    TOKEN_NEED = {"message": "Token is required", "status_code": 1001}
    LOGIN_EXPIRED = {"message": "Login expired", "status_code": 1002}
    INVALID_TOKEN = {"message": "Invalid token", "status_code": 1003}
    USER_LOGINED = {"message": "User has already logged in", "status_code": 1004}
    USER_IN_BLACKLIST = {"message": "User is in the blacklist", "status_code": 1005}
    REFRESH_TOKEN_EXPIRED = {"message": "Refresh token expired", "status_code": 1006}
    PRINT_LOG_ERROR = {"message": "Print log error", "status_code": 100500}
    SMS_CODE_EXISTS = "Already sent, please wait"
    SMS_CODE_EXPIRED = "SMS code expired"
    SMS_CODE_ERROR = "SMS code error"
    SMS_CODE_FULL = "SMS code limit full"
    UNKNOWN_ERROR = "Unknown error"


# success message
class SUCCESS:
    USER_ADDED = "User added successfully"
    ADD_OK = "Add operation successful"
    GET_OK = "Get operation successful"
    PATCH_OK = "Patch operation successful"
    DELETE_OK = "Delete operation successful"
    LOGIN_SUCCESS = "Login successful"
    LOGIN_EXIT = "Logout successful"
    OPERATE_SUCCESS = "Operation successful"
    UPDATE_SUCCESS = "Update successful"


class STATUS:
    NORMAL = 0
    DELETE = -100


class ADMIN:
    YES = 1
    NO = 0
