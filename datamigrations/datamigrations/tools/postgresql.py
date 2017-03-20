# coding=utf-8

import psycopg2
import psycopg2.extras
import sys
from dbase import DbTools


class Postgres(DbTools):
    # Postgres数据库类

    def get_cursor(self):
        # reload(sys)
        # sys.setdefaultenoding('utf8')
        # 获取postgresql数据库的游标
        cursor = ''
        try:
            conn = psycopg2.connect(host=self._host, port=int(self._port), user=self._user, password=self._pass, database=self._name)
            cursor = conn.cursor()
        except Exception as e :
            raise   # 原封不动的把异常抛出到上层调用代码
        return cursor

    def create_sql(self, pos):
        sql = ''
        # 确定sql语句
        fields = ','.join(self._fields)
        if self._task_type == 2:
            sql = self._sql % (fields, pos['curpos'], pos['curpos_stime'], pos['curpos_etime'])
        elif self._task_type == 1:
            sql = self._sql % (fields, pos['curpos'])
        elif self._task_type == 0:
            sql = self._sql % (fields, pos['curpos'])
        print 'ok'
        return sql

    def get_data(self, pos):
        # 抽取数据
        try:
            cur = self.get_cursor()
            sql = self.create_sql(pos)
            cur.execute(sql)
            lst = cur.fetchall()
            lst = list(lst)
            cur.close()
            return lst
        except Exception as e:
            print 'Failed to get data'
