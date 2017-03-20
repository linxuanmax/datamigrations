# coding=utf-8
import MySQLdb
from dbase import DbTools


class MySql(DbTools):

    def get_cursor(self):
        # 获取游标
        cursor = ''
        try:
            conn = MySQLdb.Connect(host=self._host, port=int(self._port), user=self._user, passwd=self._pass,
                                   db=self._name, charset='utf8')
            cursor = conn.cursor()
        except Exception as e:
            raise
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
        return sql

    def get_data(self, pos):
        # 抽取数据
        lst = ''

        try:
            cur = self.get_cursor()
            sql = self.create_sql(pos)
            cur.execute(sql)
            lst = cur.fetchall()
            lst = list(lst)
            cur.close()
        except Exception as e:
            print 'Failed to get data'
            raise e
        finally:
            return lst


