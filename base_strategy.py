#coding=utf-8

import time

class BaseStrategy:

    logger = None

    def __init__(self):
        pass

    @classmethod
    def logError(cls, string):
        if cls.logger != None:
            cls.logger.error("[strategy] " + string)

    @classmethod
    def logInfo(cls, string):
        if cls.logger != None:
            cls.logger.info("[strategy] " + string)

    @classmethod
    def logWarning(cls, string):
        if cls.logger != None:
            cls.logger.warning("[strategy] " + string)

    @classmethod
    def getBeginEndDate(cls, days=10):
        now = time.time()
        endDate = time.strftime('%Y%m%d', time.localtime(now))
        begin = now - (days * 24 * 3600)
        beginDate = time.strftime("%Y%m%d", time.localtime(begin))
        return str(beginDate), str(endDate)