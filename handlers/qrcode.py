#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from core.urls import QRCODE_URI, LOGIN_URI


@urlmap(url=r'/qrcode/(?P<uuid>[^\/]+)')
class QrCodeHandler(BaseHandler):


    @asynchronous
    @gen.coroutine
    def get(self, uuid):
        cli = AsyncHTTPClient()
        url = QRCODE_URI.format(**{'uuid': uuid})
        yield cli.fetch(url, self.callback)

    def callback(self, response):
        self.set_header("Content-type",  "image/jpeg")
        self.write(response.body)
        login_url = LOGIN_URI.format(**{'timestamp': self.get_timestamp(), 'uuid': uuid})
