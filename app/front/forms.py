from wtforms import Form, StringField, IntegerField
from wtforms.validators import Regexp, InputRequired, EqualTo, ValidationError
from ..forms import BaseForm
from utils import zlcache


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确格式手机号码')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式短信验证码')])
    username = StringField(validators=[Regexp(r'.{2,20}', message='请输入正确格式用户名')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式密码')])
    password2 = StringField(validators=[EqualTo("password1", message='两次输入密码不一致')])

    # graph_captcha = StringField(validators=[Regexp(r"\w{4}", message='请输入正确格式验证码')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_mem = zlcache.get(telephone)
        print('sms_captcha {}'.format(sms_captcha))
        print('sms_captcha_mem {}'.format(sms_captcha_mem))
        if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    # def validate_graph_captcha(self, field):
    #     graph_captcha = field.data
    #     graph_captcha_mem = zlcache.get(graph_captcha.lower())
    #     if not graph_captcha_mem:
    #         raise ValidationError(message='图形验证码错误')


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确格式手机号码')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式密码')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])


class AddCommentForm(BaseForm):
    comment_content = StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子ID')])