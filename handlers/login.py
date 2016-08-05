#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
import json
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from core.urls import UUID_URI


@urlmap(url=r'/login')
class LoginHandler(BaseHandler):


    @asynchronous
    @gen.coroutine
    def get(self):
        cli = AsyncHTTPClient()
        url = UUID_URI.format(**{'timestamp': self.get_timestamp()})
        yield cli.fetch(url, self.callback)

    def callback(self, response):
        msg = {'code': 1, 'uuid': ''}
        stat = dict(
            map(lambda kv: kv.split(' = '), 
                response.body.strip(';').split('; '))
            )
        if stat.get('window.QRLogin.code') == '200':
            uuid = stat.get('window.QRLogin.uuid').strip('"')
            msg['code'] = 0
            msg['uuid'] = uuid
        self.write(json.dumps(msg))
        self.finish()

