from hashlib import md5
from app.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp, InputRequired,Regexp,EqualTo,ValidationError
from utils import zlcache

class SMSCaptcha(BaseForm):
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])
    salt = 'werqewr2jmvspo2938lwsop'

    def validate(self):
        result = super(SMSCaptcha, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        sign2 = md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()
        print('sign {}'.format(sign))
        print('sign2 {}'.format(sign2))
        if sign == sign2:
            return True
        return False