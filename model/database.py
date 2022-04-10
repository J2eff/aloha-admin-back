TABLE_NAME = "Aloha"
GSI_INDEX = "aloha_gsi"

PK = "pk"
SK = "sk"
DK = "data"

USER_APPLE = "APPLE"
USER_KAKAO = "KAKAO"
USER_IMAGE = "IMAGE"

USER = "USER"
USER_KEY = "USER#{user_id}"
SOCIAL_KEY = "SOCIAL#{provider}#{provider_id}"
USERNAME_KEY = "USERNAME#{username}"
PROFILE = "PROFILE"
PHONE = "PHONE"
PHONE_KEY = "PHONE#{phone}"
NICKNAME_KEY = "NICKNAME#{nickname}"
DEVICE = "DEVICE"
DEVICE_KEY = "DEVICE#{registration_id}"

BLOCK_KEY = "BLOCK#{user_id}"
BLOCK = "BLOCK"

SMS_KEY = "SMS#{phone}"
SMS_CODE_KEY = "SMS#{phone}#{code}"

LEISURE = "LEISURE"
LEISURE_KEY = "LEISURE#{leisure_id}"

SCHEDULE = "SCHEDULE"
SCHEDULE_KEY = "SCHEDULE#{schedule_id}"
DATE = "DATE"
DATE_KEY = "DATE#{start}#{end}"
DATETIME = "DATETIME"
DATETIME_KEY = "DATETIME#{datetime}"

REQUEST = "REQUEST"
REQUEST_KEY = "REQUEST#{user_id}"

TAG = "TAG"
TAG_KEY = "TAG#{tag_id}"

FRIEND = "FRIEND"
FRIEND_KEY = "FRIEND#{user_id}"

REPORT_KEY = "REPORT#{report_id}"

NOTIFICATION = "NOTIFICATION"
NOTIFICATION_KEY = "NOTIFICATION#{notification_id}"

CHAT = "CHAT"
CHAT_KEY = "CHAT#{chat_id}"

MESSAGE = "MESSAGE"
MESSAGE_KEY = "MESSAGE#{created}#{message_id}"

ABUSE = "ABUSE"
ABUSE_KEY = "ABUSE#{text}"
