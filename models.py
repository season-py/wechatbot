#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
from datetime import datetime
from settings import SETTINGS
from pony.orm import Database, Required, Optional, PrimaryKey

db = Database()
db.bind('sqlite', SETTINGS['sqlite_file'], create_db=True)

class User(db.Entity):
    uuid = PrimaryKey(str, 36)
    wechat_uuid = Optional(str, 36)
    is_valid = Required(int, size=8)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')


db.generate_mapping(create_tables=True)
