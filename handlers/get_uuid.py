#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
import json
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from models import User
from pony.orm import db_session


@urlmap(url=r'/get_uuid')
class GetUuidHandler(BaseHandler):

    wechat_uuid_uri = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_US&_={timestamp}'

    @asynchronous
    @gen.coroutine
    def get(self):
        cli = AsyncHTTPClient()
        uri = self.wechat_uuid_uri.format(**{'timestamp': self.get_timestamp()})
        yield cli.fetch(uri, self.callback)

    def callback(self, response):
        msg = {'code': 1, 'wechat_uuid': ''}
        stat = self.extract(response.body)
        if stat.get('window.QRLogin.code') == '200':
            wechat_uuid = stat.get('window.QRLogin.uuid')
            msg['code'] = 0
            msg['wechat_uuid'] = wechat_uuid
            with db_session:
                user = User.get(uuid=self.current_user)
                if not user:
                    user = User(uuid=self.current_user, is_valid=1)
                user.wechat_uuid = wechat_uuid 
        self.redirect('/get_qrcode')

