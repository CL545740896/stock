#coding=utf-8

import requests
import time

class Point:

    sinaURL = 'http://hq.sinajs.cn'

    def __init__(self):
        #股票代码
        self.code = None
        #股票名称
        self.name = None
        #今日开盘价
        self.dayBegin = None
        #昨日收盘价
        self.lastdayEnd = None
        #当前价格
        self.now = None
        #今日最高价
        self.dayMax = None
        #今日最低价
        self.dayMin = None
        #成交的股票数, 由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百
        #成交金额，单位w元
        #当前时间
        self.time = None

    @classmethod
    def getNow(cls, code):
        url = cls.sinaURL + '/list=' + code
        r = requests.get(url)
        fields = r.text.replace('var hq_str_' + code + '=', '').replace("\"", '').split(',')
        p = Point()
        p.code, p.name, p.dayBegin, p.lastdayEnd, p.now, p.dayMax, p.dayMin, p.time = code, fields[0], float(fields[1]), float(fields[2]), float(fields[3]), float(fields[4]), float(fields[5]), ' '.join([ fields[-3], fields[-2] ])
        return p

    def dump(self):
        m = {
            'code' : self.code,
            'name' : self.name,
            'dayBegin' : self.dayBegin,
            'lastdayEnd' : self.lastdayEnd,
            'now' : self.now,
            'dayMax' : self.dayMax,
            'dayMin' : self.dayMin,
            'time' : self.time,
        }
        for k, v in m.items(): 
            print(k + ':' + str(v) + "(%s)" % type(v)  )

    @classmethod
    def isStcokTime(cls):
        '''
        判断当前是否为A股交易时间
        '''
        curStamp = time.time()
        t = time.localtime(curStamp)
        if t.tm_wday not in [0, 1, 2, 3, 4]: return False
        beginTime = int(time.mktime(time.strptime("%s-%s-%s 00:00:00" % (t.tm_year, t.tm_mon, t.tm_mday), "%Y-%m-%d %H:%M:%S")))
        time_9_30 = beginTime + 9 * 3600 + 1800
        time_11_30 = beginTime + 11 * 3600 + 1800
        time_13_00 = beginTime + 13 * 3600
        time_15_00 = beginTime + 15 * 3600
        if curStamp >= time_9_30 and curStamp <= time_11_30 or curStamp >= time_13_00 and curStamp <= time_15_00: return True
        return False