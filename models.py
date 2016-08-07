#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from pony.orm import *
from settings import sqlite_file

db = Database()
db.bind('sqlite', sqlite_file, create_db=True)
db.generate_mapping(create_tables=True)
