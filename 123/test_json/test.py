import os
import sys_config

configFile = os.path.split(os.path.realpath(__file__))[0] + "/test.conf"
print configFile

conf = sys_config.SysConfig(configFile)
name = conf.getConfig("info", "name")
age = conf.getConfig("info", "age")
classes = conf.getConfig("info", "classes")

action = []
actions = {
    "name":name,
    "age":age,
    "classes":classes
}

action.append(actions)
print action
