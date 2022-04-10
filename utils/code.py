AUTH_REQUIRED = {"status_code": 401, "detail": "AUTH_REQUIRED"}
AUTH_FAIL = {"status_code": 403, "detail": "AUTH_FAIL"}
USERNAME_ALREADY_EXIST = {"status_code": 400, "detail": "USERNAME_ALREADY_EXIST"}
USER_NOT_EXIST = {"status_code": 400, "detail": "USER_NOT_EXIST"}
WRONG_PASSWORD = {"status_code": 400, "detail": "WRONG_PASSWORD"}
TIME_REQUIRED = {"status_code": 400, "detail": "TIME_REQUIRED"}

INVALID_TOKEN = {"status_code": 403, "detail": "INVALID_TOKEN"}
INVALID_AUTH_SCHEMA = {"status_code": 403, "detail": "INVALID_AUTH_SCHEMA"}
INVALID_AUTH = {"status_code": 403, "detail": "INVALID_AUTH"}
ONLY_ADMIN = {"status_code": 403, "detail": "ONLY_ADMIN"}

FAIL_SEND_SMS = {"status_code": 400, "detail": "FAIL_SEND_SMS"}
FAIL_AUTH_SMS = {"status_code": 400, "detail": "FAIL_AUTH_SMS"}
EXPIRE_AUTH_SMS = {"status_code": 400, "detail": "EXPIRE_AUTH_SMS"}

NOT_FOUND = {"status_code": 404, "detail": "NOT_FOUND"}
FORBIDDEN = {"status_code": 403, "detail": "FORBIDDEN"}

FRIEND_REQUEST_NOT_FOUND = {"status_code": 400, "detail": "FRIEND_REQUEST_NOT_FOUND"}
EXCEED_MEMBER = {"status_code": 400, "detail": "EXCEED_MEMBER"}

MESSAGE_ABUSE = {"status_code": 400, "detail": "MESSAGE_ABUSE"}

OK = {"status_code": 200}
CREATED = {"status_code": 201}
NO_CONTENT = {"status_code": 204}
