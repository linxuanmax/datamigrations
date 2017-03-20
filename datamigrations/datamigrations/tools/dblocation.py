# coding=utf-8

import json
import os
import datetime
import time


def load_pos(task_name, task_type, main_fld_type, time_fld_format, pos):
    # 第一次开始任务配置位置存储文件
    track_file = os.path.split(os.path.realpath(__file__))[0] + '/track/' + "%s" % (task_name + '.json')   # 文件位置固定
    if os.path.exists(track_file):
        load_f = open(track_file, 'r')
        files = json.load(load_f)
        pos['curpos'] = files['curpos']
        pos['curpos_stime'] = files['curpos_stime']
        pos['curpos_etime'] = files['curpos_etime']
        load_f.close()
        return pos
    else:
        d = datetime.datetime.strptime('2010-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        e = datetime.datetime.strptime('1980-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        if main_fld_type[0] == 'number':
            pos['curpos'] = 0
        elif main_fld_type[0] == 'string':
            pos['curpos'] = ''
        elif main_fld_type[0] == 'time':
            pos['curpos'] = e.strftime(main_fld_type[1])
        if task_type == 2:
            pos['curpos_stime'] = d.strftime(time_fld_format)
            pos['curpos_etime'] = d.strftime(time_fld_format)
        f = open(track_file, 'w')
        f.write(json.dumps(pos))
        f.close()
        return pos


def save_pos(task_name, pos):
    # 保存数据位置
    track_file = os.path.split(os.path.realpath(__file__))[0] + '/track/' + "%s" % (task_name + '.json')
    f = open(track_file, 'w')
    f.write(json.dumps(pos))
    f.close()


def del_pos(task_name):
    # 删除任务
    track_file = os.path.split(os.path.realpath(__file__))[0] + '/track/' + "%s" % (task_name + '.json')
    if track_file:
        print "MISSION OVER：%s" % task_name
        os.remove(track_file)


def add_location(main_fld_type, time_fld_format, days_range, hours_range, pos):
    # 当处理时间增量的任务时，确定时间位置
    time_curpos_stime = datetime.datetime.strptime(pos['curpos_etime'].encode('utf-8'), time_fld_format)
    time_now = datetime.datetime.now()
    time_now_sub = time_now + datetime.timedelta(days=days_range)
    try:
        time_curpos_stime += datetime.timedelta(hours=hours_range)
        if time_curpos_stime < time_now_sub:
            pos['curpos_stime'] = pos['curpos_etime']
            pos['curpos_etime'] = time_curpos_stime.strftime(time_fld_format)
            if main_fld_type[0] == 'number':
                pos['curpos'] = 0
            elif main_fld_type[0] == 'string':
                pos['curpos'] = ' '
            elif main_fld_type[0] == 'time':
                d = datetime.datetime.strptime('1980-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                pos['curpos'] = d.strftime(main_fld_type[1])
        else:
            time.sleep(5)
    finally:
        return pos

