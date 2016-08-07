#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
import uuid
import time
import logging
from tornado import web

logger = logging.getLogger('RequestHandler')

class AccessDeny(Exception):
    pass


class Context(dict):

    def __getattr__(self, key):
        if not key.startswith('__'):
            return self[key]
        else:
            super(Context, self).__getattr__(key)

    def __setattr__(self, key, value):
        self[key] = value


class BaseHandler(web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    @staticmethod
    def get_timestamp():
        return int(time.time() * 1000)

    def prepare(self):
        self.context = Context()
        if not self.get_uuid():
            self.set_uuid()

    def set_uuid(self):
        _uuid = str(uuid.uuid1())
        logger.debug('设置用户uuid: {0}'.format(_uuid))
        self.set_secure_cookie('uuid', _uuid)

    def get_uuid(self):
        return self.get_secure_cookie('uuid')


