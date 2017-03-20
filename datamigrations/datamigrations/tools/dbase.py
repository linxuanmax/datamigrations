#!/usr/bin/env python
# -*- coding=utf-8 -*-


class DbTools:
    # 数据库基类
    def __init__(self, task):
        self._host = task['dbhost']
        self._port = task['dbport']
        self._name = task['dbname']
        self._user = task['dbuser']
        self._pass = task['dbpass']

        self._index_name = task['index_name']
        self._main_type = task['main_fld_type']
        self._time_fld = task['time_fld']
        self._task_type = task['task_type']
        self._fields = task['fields']
        self._task_name = task['task_name']
        self._sql = task['sql']


