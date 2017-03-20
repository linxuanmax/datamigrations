#!usr/bin/env python
# coding=utf-8
from utils import sys_config, sys_log
from tools import dblocation, dbfactory

import globalvariable
import os
import multiprocessing
import esdataextract
import time
import traceback
import datetime
# 配置文件
configFile = os.path.split(os.path.realpath(__file__))[0] + "/conf/datamigrations.conf"
print configFile
if os.path.exists(configFile) is False:
    configFile = "/opt/datamigrations/conf/datamigrations/datamigrations.conf"


def run():
    # 传进任务列表（列表形式）， 数据库连接 （字典形式）
    task_list = globalvariable.task_list
    connection_list = globalvariable.connection_list
    # 如果任务列表不为空以及列表元素大小零，执行任务
    if task_list is not None and len(task_list) > 0:
        create_task(task_list, connection_list)


def create_task(task_list, connection_list):
    for task in task_list:
        conn_info = connection_list[task['connection']]
        # 把执行任务所需要的参数放进一个变量中，创建多进程执行任务
        argus = (task, conn_info)
        p = multiprocessing.Process(name="Process", target=task_func, args=argus)
        p.start()


def task_func(task, conn_info):
    es = esdataextract.ESData(configFile)

    task['dbhost'] = conn_info["hostname"]
    task['dbport'] = conn_info["port"]
    task['dbname'] = conn_info["dbname"]
    task['dbuser'] = conn_info["username"]
    task['dbpass'] = conn_info["userpass"]

    task_name = task['task_name']
    task_type = task['task_type']
    main_fld_type = task['main_fld_type']
    fields = task['fields']
    index_name = task['index_name']
    type_name = task['type_name']
    days_range = task['days_range']
    hours_range = task['hours_range']
    es_id_fld = task['es_id_fld']
    time_fld_format = task['time_fld_format']

    pos = {'curpos': None, 'curpos_stime': None, 'curpos_etime': None}
    pos = dblocation.load_pos(task_name, task_type, main_fld_type, time_fld_format, pos)
    db_fac = dbfactory.DbFactory(task)
    db = db_fac.factory(conn_info["data_type"])
    if db is not None:
        while True:
            try:
                lst = db.get_data(pos)
                print 'Task: %s is running ' % task_name
                # 时间增量任务
                if task_type == 2:
                    if len(lst) > 0:
                        es.es_data(lst, fields, index_name, type_name, es_id_fld)
                        # 取返回列表的最后一位元素，再取这个元组（元素）的第一位。
                        if task['main_fld_type'][0] == 'time':
                            pos['curpos'] = lst[-1][0].strftime(task['main_fld_type'][1])
                        else:
                            pos['curpos'] = lst[-1][0]
                            print pos['curpos']
                        dblocation.save_pos(task_name, pos)
                    else:
                        # 如果返回的列表中没有值则移动时间间隔
                        pos = dblocation.add_location(main_fld_type, time_fld_format, days_range, hours_range, pos)
                        dblocation.save_pos(task_name, pos)
                # 主键自增任务
                elif task_type == 1:
                    if len(lst) > 0:
                        es.es_data(lst, fields, index_name, type_name, es_id_fld)
                        if task['main_fld_type'][0] == 'time':
                            pos['curpos'] = lst[-1][0].strftime(task['main_fld_type'][1])
                        else:
                            pos['curpos'] = lst[-1][0]
                        dblocation.save_pos(task_name, pos)
                    else:
                        # 每5秒钟循环一次
                        time.sleep(5)
                # 一次性导入任务
                elif task_type == 0:
                    if len(lst) > 0:
                        es.es_data(lst, fields, index_name, type_name, es_id_fld)
                        if task['main_fld_type'][0] == 'time':
                            pos['curpos'] = lst[-1][0].strftime(task['main_fld_type'][1])
                        else:
                            pos['curpos'] = lst[-1][0]
                        dblocation.save_pos(task_name, pos)
                    else:
                        # 如果没有数据则5秒钟之后删除存储位置的文件
                        dblocation.del_pos(task_name)
                        break
            # 如果出现 IOError 则中断
            except IOError:
                break
            # 其它错误均写入日志
            except Exception as e:
                conf = sys_config.SysConfig(configFile)
                _logFile = conf.getConfig("datamigrations", "logFile")
                _instance = conf.getConfig("datamigrations", "instanceName")
                sys_log.SysLog(_logFile, _instance).writeLog("error", "tbname" + " --- " + str(traceback.format_exc()))

