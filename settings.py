#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com

import os

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

SETTINGS = {
    'debug': True,
    'cookie_secret': '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
    'xsrf_cookies': True,
    'autoreload': True,
    'login_url': '/login',
    'template_path': os.path.join(WORKSPACE, 'templates'),
    'static_path': os.path.join(WORKSPACE, 'static'),
    'media_path': os.path.join(WORKSPACE, 'media'),
}

