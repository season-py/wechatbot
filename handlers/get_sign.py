#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from tornado import gen
from tornado.web import asynchronous
from tornado.escape import url_unescape
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from models import User
from pony.orm import db_session



@urlmap(url=r'/get_sign')
class GetSignHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def get(self):
        wechat_uuid = None
        cli = AsyncHTTPClient()
        uri = url_unescape(self.get_argument('redirect_uri', None))
        with db_session:
            user = User.get(uuid=self.current_user)
            wechat_uuid = user.wechat_uuid
        yield cli.fetch(uri, self.callback)

    def callback(self, response):
        print response.headers.items()

