#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
import re
import uuid
import time
import logging
from tornado import web

logger = logging.getLogger('RequestHandler')

class BaseHandler(web.RequestHandler):

    MsgPattern = re.compile('(.*?) ?= ?"?(.*?)"?; ?')

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    @staticmethod
    def get_timestamp():
        return int(time.time() * 1000)

    @property
    def current_user(self):
        return self.get_current_user()

    def extract(self, text):
        return dict(self.MsgPattern.findall(text.replace('\n', '')))

    def prepare(self):
        if not self.get_current_user():
            self.set_current_user()

    def set_current_user(self):
        self.set_secure_cookie('uuid', str(uuid.uuid1()))

    def get_current_user(self):
        return self.get_secure_cookie('uuid')


