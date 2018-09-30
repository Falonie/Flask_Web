import os

DEBUG = True
# SECRET_KEY = os.urandom(24)
SECRET_KEY = "weddsfjksakjdfiowefksdo"
DB_URI = "mysql+pymysql://root:1234@localhost:3306/flask_bbs"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# PERMANENT_SESSION_LIFETIME=
CMS_USER_ID = ''
FRONT_USER_ID = 'AAAA'

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
# MAIL_PORT = "465"
MAIL_USE_TLS = True
# MAIL_USE_SSL = True
# MAIL_DEBUG : default app.debug
MAIL_USERNAME = "541002901@qq.com"
MAIL_PASSWORD = "ecerlujhbaahbdib"
MAIL_DEFAULT_SENDER = "541002901@qq.com"
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False

ALIDAYU_APP_KEY = ''
ALIDAYU_APP_SECRET = ''
ALIDAYU_SIGN_NAME = ''
ALIDAYU_TEMPLELATE_CODE = 'SMS_133966854'

# d={'name':'falonie'}
# print('name' in d)

# flask-paginate
PER_PAGE = 10

# celery
CELERY_RESULT_BACKEND = "redis://:falonie@127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://:falonie@127.0.0.1:6379/0"
