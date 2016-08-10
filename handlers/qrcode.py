#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from core.urls import QRCODE_URI
from models import User
from pony.orm import db_session


@urlmap(url=r'/qrcode')
class QrCodeHandler(BaseHandler):


    @asynchronous
    @gen.coroutine
    def get(self):
        wechat_uuid = None
        with db_session:
            user = User.get(uuid=self.current_user)
            wechat_uuid = user.wechat_uuid
        cli = AsyncHTTPClient()
        url = QRCODE_URI.format(**{'uuid': wechat_uuid})
        yield cli.fetch(url, self.callback)

    def callback(self, response):
        self.set_header("Content-type",  "image/jpeg")
        self.write(response.body)
        self.flush()
        self.finish()
