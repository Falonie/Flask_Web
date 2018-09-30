from werkzeug.security import generate_password_hash, check_password_hash

# d={'sms_captcha': ['短信验证码错误']}
# m=d.popitem()[1][0]
# print(m)

# print('\u8bf7\u8f93\u5165\u8bc4\u8bba\u5185\u5bb9'.encode('utf-8').decode('utf-8'))
# print('\u90ae\u7bb1\u9a8c\u8bc1\u7801\u9519\u8bef')

FOLLOW = 0x11
COMMENT = 0x02
WRITE_ARTICLES = 0x04
MODERATE_COMMENTS = 0x08
ADMINISTER = 0x80
roles = {
    'user': (FOLLOW | COMMENT | WRITE_ARTICLES, True),
    'moderator': (FOLLOW | COMMENT | WRITE_ARTICLES | MODERATE_COMMENTS, False),
    'administrator': (0xff, False)
}

for r in roles:
    print(r)
    print(roles[r][0], roles[r][1])

# print(int('0b01000000',2))
print(int('0x11', 16))
print(int('0x02', 16))
print(int('0x04', 16))
print(int('0x08', 16))
print(int('0x80', 16))
print(int('0xff', 16))
