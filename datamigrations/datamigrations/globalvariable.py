#!/usr/bin/env python
# -*- coding=utf-8 -*-

# 连接数据库的信息:为字典形式
# 例：mysql1:数据库连接的配置（键）名称
# hostname:IP地址
# port:端口
# dbname:连接的数据库的名称
# username:数据库的用户名
# userpass:与用户名对应的密码
# connection:要导入的数据库类型  ***db_type


connection_list = {

    'db_1': {'hostname': '192.168.1.225', 'port': '3306', 'dbname': 'test_a', 'username': 'root', 'userpass': '123465', 'data_type': 'mysql'},
    'db_2': {'hostname': '192.168.1.225', 'port': '3306', 'dbname': 'test_b', 'username': 'root', 'userpass': '123465', 'data_type': 'mysql'},
    'db_3': {'hostname': '192.168.1.225', 'port': '3306', 'dbname': 'test_c', 'username': 'root', 'userpass': '123465', 'data_type': 'mysql'},
    'db_4': {'hostname': '127.0.0.1', 'port': '5432', 'dbname': 'exampledb', 'username': 'dbname','userpass': 'yzl', 'data_type': 'postgresql'},
    'db_5': {'hostname': '192.168.1.225', 'port': '3306', 'dbname': 'test_data', 'username': 'root', 'userpass': '123465', 'data_type': 'mysql'},
    'db_6': {'hostname': '192.168.1.225', 'port': '3306', 'dbname': 'test_b', 'username': 'root', 'userpass': '123465', 'data_type': 'mysql'},
}


# 任务列表:列表形式，以下task_list中的几个元素是添加任务的例子,添加或修改任务需要重新启动程序
# 1/task_name:命名， 第一位代表 数据库类型 1:mysql 2:postgresql  第二位代表增量方式 1：主键自增 2：时间增量 0：一次性导入 第三位为任务标号 依次增加
# 2/connection:数据库配置
# 3/task_type:数据的增长方式（1：主键增量 2：时间增量 0：一次性导入）
# 4/time_fld:当导入的方式是时间增量时，此字段为时间增量字段.(task_type == 2时塡写，其它情况均填写: 'time_fld':'')
# 5/main_fld:主键字段
# 6/main_fld_type:主键字段的数据类型 'number', 'string', 'time'
# 7/index_name:数据表的名称 固定为 idx_threat_intelligence
# 8/type_name:ES的_type名称，默认为数据表的名字
# 9/fields:数据表的字段（注意：主键放在第一位，（当为时间增量方式时）时间增量字段放在最后一位）
# 10/days_range: 任务为时间增量时（其它增量方式时写 'days_range':-2），每次导入数据的时间段，数据类型为 number，单位为小时
# 11/hours_range: 任务为时间增时（其它增量方式时写 'hours_range':12），每次导入数据的时间段，数据类型为 number，单位为天
# 12/es_id_fld:插入ES中所需要的_id 值， 如果为None则会自动生成，如果指定字段名称，则使用指定的名称
# 13/time_fld_format:时间格式，根据实际情况填写 例如：'####-##-## ##：##：##',
# '####/##/## ##：##：##'  等等 (只有当主键类型为时间或任务为时间增量类型时填写，其它情况写  'time_fld_format':'')
# 14/sql:提取数据的sql语句，根据实际情况填写.并注意引号的使用,对于postgresql数据库，写sql语句的时候一定要在最外层用双引号，内部用单引号

task_list = [

    # 多表联合查询模板
    # {
    #     'task_name': '1_1_4',
    #     'connection': 'db_6',
    #     'task_type': 1,
    #     'time_fld': '',
    #     'main_fld': 'u_id',
    #     'main_fld_type': ['number'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'u_user',
    #     'fields': ['u_id', 'u_name', 'u_pwd', 'u_truename', 'u_email'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld': None,
    #     'time_fld_format': '',
    #     'sql': 'select %s from s_user,s_factory where s_user.u_id = s_factory.f_id and u_id > %s order by u_id asc limit 1 ;'
    # },
    #
    # {
    #     'task_name': '1_1_1',
    #     'connection': 'db_1',
    #     'task_type': 1,
    #     'time_fld': '',
    #     'main_fld': 'ID',
    #     'main_fld_type': ['number'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_aa',
    #     'fields': ['ID', 'name', 'curtime'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld':None,
    #     'time_fld_format': '',
    #     'sql': 'select %s from info_aa where ID > %s order by ID asc limit 5 ;',
    # },
    #
    #
    # {
    #     'task_name': '1_1_2',
    #     'connection': 'db_1',
    #     'task_type': 1,
    #     'time_fld': '',
    #     'main_fld': 'ID',
    #     'main_fld_type': ['string'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_ba',
    #     'fields': ['ID', 'name'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld':None,
    #     'time_fld_format': '',
    #     'sql': 'select %s from info_ba where ID > "'"%s"'" order by ID asc limit 5 ;',
    # },
    #
    #
    # {
    #     'task_name': '1_1_3',
    #     'connection': 'db_1',
    #     'task_type': 1,
    #     'time_fld': '',
    #     'main_fld': 'ID',
    #     'main_fld_type': ['time', '%Y-%m-%d %H:%M:%S'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_ca',
    #     'fields': ['ID', 'name'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld':None,
    #     'time_fld_format': '%Y-%m-%d %H:%M:%S',
    #     'sql': 'select %s from info_ca where ID > "'"%s"'" order by ID asc limit 5 ;',
    # },
    #
    #
    # {
    #     'task_name': '1_2_1',
    #     'connection': 'db_2',
    #     'task_type': 2,
    #     'time_fld': 'curtime',
    #     'main_fld': 'ID',
    #     'main_fld_type': ['number'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_ab',
    #     'fields': ['ID', 'curtime'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld': None,
    #     'time_fld_format': '%Y-%m-%d %H:%M:%S',
    #     'sql': 'select %s from info_ab where  ID > %s and curtime > "'"%s"'" and curtime <= "'"%s"'" order by ID asc limit 5 ;',
    # },
    #
    #
    # {
    #     'task_name': '1_2_2',
    #     'connection': 'db_2',
    #     'task_type': 2,
    #     'time_fld': 'curtime',
    #     'main_fld': 'ID',
    #     'main_fld_type': ['string'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_bb',
    #     'fields': ['ID', 'curtime'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld': None,
    #     'time_fld_format': '%Y-%m-%d %H:%M:%S',
    #     'sql': 'select %s from info_bb where  ID > "'"%s"'" and curtime > "'"%s"'" and curtime <= "'"%s"'" order by ID asc limit 5 ;',
    # },
    #
    #
    #
    # {
    #     'task_name': '1_2_3',
    #     'connection': 'db_2',
    #     'task_type': 2,
    #     'time_fld': 'curtime',
    #     'main_fld': 'ID',
    #     'main_fld_type': ['time', '%Y-%m-%d %H:%M:%S'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_cb',
    #     'fields': ['ID', 'curtime'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld': 'ID',
    #     'time_fld_format': '%Y-%m-%d %H:%M:%S',
    #     'sql': 'select %s from info_cb where  ID > "'"%s"'" and curtime > "'"%s"'" and curtime <= "'"%s"'" order by ID asc limit 5 ;'
    # },


    {
        'task_name': '1_0_1',
        'connection': 'db_3',
        'task_type': 0,
        'time_fld': '',
        'main_fld': 'ID',
        'main_fld_type': ['number'],
        'index_name': 'idx_threat_intelligence',
        'type_name': 'info_ac',
        'fields': ['ID', 'name'],
        'days_range': -2,
        'hours_range':12,
        'es_id_fld': None,
        'time_fld_format': '',
        'sql':'select %s from info_ac where ID > "'"%s"'" limit 2;'
    },


    # {
    #     'task_name': '2_0_1',
    #     'connection': 'db_4',
    #     'task_type': 0,
    #     'time_fld': '',
    #     'main_fld': 'id',
    #     'main_fld_type': ['number'],
    #     'index_name': 'idx_threat_intelligence',
    #     'type_name': 'info_ad',
    #     'fields': ['id', 'name'],
    #     'days_range': -2,
    #     'hours_range':12,
    #     'es_id_fld': None,
    #     'time_fld_format': '',
    #     'sql':"select %s from info_ad where id > %s limit 2;"
    # }


    ]






