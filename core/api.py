# coding=utf-8
# author=haishan09@gmail.com
import gtk
import time
import pygtk
import requests
from urls import UUID_URI, QRCODE_URI

pygtk.require('2.0')

class WeChatApi(object):

    def __init__(self):
        pass

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
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.connect("destroy", lambda _: gtk.main_quit())
        img = gtk.Image()
        loader = gtk.gdk.PixbufLoader()
        loader.set_size(430, 430)
        loader.write(data)
        loader.close()
        img.set_from_pixbuf(loader.get_pixbuf())
        win.add(img)
        img.show()
        win.show()
        gtk.main()





if __name__ == '__main__':
    wechat = WeChatApi()
    uuid = wechat.get_uuid()
    wechat.show_qrcode(uuid)

