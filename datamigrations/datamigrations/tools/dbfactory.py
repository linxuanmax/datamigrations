#!/usr/bin/env python
# -*- coding=utf-8 -*-

from mysql import MySql
from postgresql import Postgres


class DbFactory:

    # 数据库类工厂
    def __init__(self, task):
        # task：数据库相关字典
        # 包括的keys有：dbhost, dbport, dbname, dbuser, dbpass
        self._params = task

    def factory(self, dbtype):
        dbtype = dbtype.lower()
        if dbtype == 'mysql':
            return MySql(self._params)
        elif dbtype == 'postgresql':
            return Postgres(self._params)
        else:
            return None
