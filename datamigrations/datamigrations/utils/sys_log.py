#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os.path
import logging
import logging.handlers


class SysLog:
    """
    记录日志
    """

    def __init__(self, logFileName, instanceName):
        # 构造函数
        self.logFileName = logFileName
        self.instanceName = instanceName

    def writeLog(self, logtype, log):
         # 写日志
        filePath = os.path.dirname(self.logFileName)
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        logger = logging.getLogger(self.instanceName)
        logger.setLevel(logging.INFO)

        if len(logger.handlers) == 0:
            handler = logging.handlers.RotatingFileHandler(self.logFileName, maxBytes=1048576, backupCount=10)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)

            logger.addHandler(handler)

        if logtype == "info":
            logger.info(log)
        elif logtype == "warn":
            logger.warn(log)
        elif logtype == "error":
            logger.error(log)
        elif logtype == "debug":
            logger.debug(log)
        elif logtype == "critical":
            logger.critical(log)

        logging.shutdown()
