import hashlib
from time import time
from urllib import request, parse
import json
import logging
import requests

class AlidayuAPI(object):
    APP_KEY_FIELD = 'ALIDAYU_APP_KEY'
    APP_SECRET_FIELD = 'ALIDAYU_APP_SECRET'
    SMS_SIGN_NAME_FIELD = 'ALIDAYU_SIGN_NAME'
    SMS_TEMPLELATE_CODE_FIELD = 'ALIDAYU_TEMPLELATE_CODE'

    def __init__(self, app=None):
        self.url = 'https://eco.taobao.com/router/rest'
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
        }
        if app:
            self.init_app(app)

    def init_app(self, app):
        pass

    def send_sms(self, telephone=None, code=None,**params):
        # self.api_params['timestamp']=str(int(time()*1000))
        # self.api_params['sms_param']=str(params)
        # self.api_params['rec_num']=telephone
        #
        # newparams=''.join('%s%s'%(k,v) for k,v in sorted(self.api_params.items()))
        # newparams=self.secret+newparams+self.secret
        # sign=hashlib.md5(newparams.encode('utf-8').hexdigest().upper())
        # self.api_params['sign']=sign
        #
        # resp=requests.post(self.url,params=self.api_params,headers=self.headers)
        # data=resp.json()
        # try:
        #     result=data['alibaba_aliqin_fc_sms_num_send_response']['result']['success']
        #     return result
        # except:
        #     print('='*10)
        #     print('{}'.format(data))
        #     print('='*10)
        #     return False
        return