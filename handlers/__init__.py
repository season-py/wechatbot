#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com

import imp
from glob import glob
from os.path import join, abspath, basename, dirname

def initiate():
    for handler in glob(join(dirname(abspath(__file__)), '*.py')):
        if basename(handler).startswith('__'):
            continue
        imp.load_source('handlers', handler)
