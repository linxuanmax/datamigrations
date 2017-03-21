#!/user/bin/env python
# -*- coding=utf-8 -*-

import traceback
import os
import datetime

from utils import sys_config, sys_log
from elasticsearch import Elasticsearch, helpers

# 配置文件名称
CONFIG_FILE = "datamigrations.conf"


class ESData():
    # elasticsearch数据处理类
    def __init__(self, cfgFile = None):
        self._configFile = cfgFile
        if self._configFile is None:
            self._configFile = os.path.split(os.path.realpath(__file__))[0] + "/conf/" + CONFIG_FILE
            if os.path.exists(self._configFile) is False:
                self._configFile = "/opt/datamigrations/conf/datamigrations/" + CONFIG_FILE

        conf = sys_config.SysConfig(self._configFile)
        eshost = conf.getConfig("elasticsearch", "esHost")
        esport = conf.getConfig("elasticsearch", "esPort")
        self._config = eshost + ':' + esport
        # 日志文件
        self._logFile = conf.getConfig("datamigrations", "logFile")
        # 实例名
        self._instance = conf.getConfig("datamigrations", "instanceName")

    def es_data(self, lst, fields, index_name, type_name, es_id_fld):
        # lst:数据    fields:数据表字段  index_name:表名
        now_time = datetime.datetime.now()
        a = now_time.strftime('%Y-%m-%d %H:%M:%S')
        now_time = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
        try:
            es = Elasticsearch(self._config)
            actions = []
            for data in lst:
                souce = dict(zip(fields, data))
                if es_id_fld is None or es_id_fld.strip(' ') == '':
                    action = {
                        '_index': index_name,
                        '_type': type_name,
                        '_source': {
                            index_name: souce,
                            'thread': index_name,
                            '__ctime__': now_time,
                            '__utime__': now_time,
                            '__valid__':'T'
                        }
                    }
                else:
                    es_id = type_name + '_' + str(souce[es_id_fld])
                    action = {
                        '_index': index_name,
                        '_type': type_name,
                        '_id': es_id,
                        '_source': {
                            index_name: souce,
                            'thread': index_name,
                            '__ctime__': now_time,
                            '__utime__': now_time,
                            '__valid__':'T'
                        }
                    }
                actions.append(action)
            helpers.bulk(es, actions, chunk_size=1000, max_chunk_bytes=73400320)
        except Exception, e:
            sys_log.SysLog(self._logFile, self._instance).writeLog("error", str(traceback.format_exc()))

