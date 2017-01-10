#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from models import User
from pony.orm import db_session


@urlmap(url=r'/get_qrcode')
class GetQrCodeHandler(BaseHandler):

    wechat_qrcode_uri = 'https://login.weixin.qq.com/qrcode/{uuid}'

    @asynchronous
    @gen.coroutine
    def get(self):
        wechat_uuid = None
        cli = AsyncHTTPClient()
        with db_session:
            user = User.get(uuid=self.current_user)
            wechat_uuid = user.wechat_uuid
        uri = self.wechat_qrcode_uri.format(**{'uuid': wechat_uuid})
        yield cli.fetch(uri, self.callback)

    def callback(self, response):
        self.set_header("Content-type",  "image/jpeg")
        self.write(response.body)
        self.flush()
        self.finish()
