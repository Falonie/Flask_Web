from flask import g
from wtforms import Form, StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import Email, EqualTo, InputRequired, Length
from ..forms import BaseForm
from utils import zlcache


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确邮箱'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确密码')])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确格式密码')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message='请密码保持一致')])
    # submit = SubmitField('submit')


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='请输入正确长度验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同邮箱')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID!')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入不板块id!')])
