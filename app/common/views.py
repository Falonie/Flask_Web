import random
import string
from io import BytesIO
from flask import Blueprint, request, make_response, jsonify
from .forms import SMSCaptcha
from exts import alidayu
from utils import restful, zlcache
from utils.captcha import Captcha
import qiniu

bp = Blueprint('common', __name__, url_prefix='/c')


# @bp.route('/sms_captcha/')
# def index():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码')
#     captcha = Captcha.gene_text(number=4)
#     print('sms is {}'.format(captcha))
#     if alidayu.send_sms(telephone, code=captcha):
#         return restful.success()
#     # return restful.params_error(message='短信验证码发送失败')
#     return restful.success()

@bp.route('/sms_captcha/', methods=['GET', 'POST'])
def index():
    # md5(timesleep+telephone+salt)
    form = SMSCaptcha(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print('sms is {}'.format(captcha))
        if alidayu.send_sms(telephone, code=captcha):
            zlcache.set(telephone, captcha)
            return restful.success()
        # return restful.params_error(message='短信验证码发送失败')
        zlcache.set(telephone, captcha)
        return restful.success()
    return restful.params_error(message='参数错误')


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = ''
    secret_key = ''
    q = qiniu.Auth(access_key, secret_key)
    bucket = ''
    token = q.upload_token(bucket)
    return jsonify({"uptoken": token})
