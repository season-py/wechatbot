#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from tornado import gen
from tornado.web import asynchronous
from tornado.escape import url_escape
from tornado.httpclient import AsyncHTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from models import User
from pony.orm import db_session


@urlmap(url=r'/get_ticket')
class GetTicketHandler(BaseHandler):

    wechat_ticket_uri = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={uuid}&tip=0&_={timestamp}'

    @asynchronous
    @gen.coroutine
    def get(self):
        wechat_uuid = None
        cli = AsyncHTTPClient()
        with db_session:
            user = User.get(uuid=self.current_user)
            wechat_uuid = user.wechat_uuid
        uri = self.wechat_ticket_uri.format(**{'timestamp': self.get_timestamp(), 'uuid': wechat_uuid})
        yield cli.fetch(uri, self.callback)

    def callback(self, response):
        stat = self.extract(response.body)
        if stat['window.code'] == '200':
            ticket_uri = stat['window.redirect_uri']
            self.redirect('/get_sign?redirect_uri=' + url_escape(ticket_uri))
            
