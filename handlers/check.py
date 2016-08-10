#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from core.urls import CHECK_LOGIN_URI
from models import User
from pony.orm import db_session



@urlmap(url=r'/check')
class CheckHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def get(self):
        wechat_uuid = None
        cli = AsyncHTTPClient()
        with db_session:
            user = User.get(uuid=self.current_user)
            wechat_uuid = user.wechat_uuid
        check_url = CHECK_LOGIN_URI.format(**{'timestamp': self.get_timestamp(), 'uuid': wechat_uuid})
        yield cli.fetch(check_url, self.callback)

    def callback(self, response):
        print self.extract(response.body)


