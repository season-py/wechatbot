#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com

import time
import requests
from wechatbot.core.urls import UUID_URI, QRCODE_URI
from wechatbot.core.qrcode import QrCode


class WeChatApi(object):

    def __init__(self):
        self.qrcode = QrCode()

    def get_uuid(self):
        ts = int(time.time() * 1000)
        ret = requests.get(UUID_URI.format(**{'timestamp': ts}))
        stat = dict(map(lambda kv: kv.split(' = '), 
                        ret.text.strip(';').split('; ')))
        if stat.get('window.QRLogin.code') == '200':
            return stat.get('window.QRLogin.uuid').strip('"')

    def get_qrcode(self, uuid):
        ret = requests.get(QRCODE_URI.format(**{'uuid': uuid}))
        return ret.content

    def show_qrcode(self, uuid):
        data = self.get_qrcode(uuid)
        self.qrcode.show_image(data)


if __name__ == '__main__':
    wechat = WeChatApi()
    uuid = wechat.get_uuid()
    wechat.show_qrcode(uuid)

