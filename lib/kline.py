#coding=utf-8

import gevent
from gevent import monkey
monkey.patch_all()
from point import Point
import time


class KLine:
    def __init__(self, code):
        self.code = code
        self.pointList = []

    def show(self):
        while 1:
            (1)
            p = Point.getNow(self.code)
            self.pointList.append(p)

    def collect(self, times=3110400000):
        i = 0
        while i < times:
            i = i + 1
            p = Point.getNow(self.code)
            self.onOnePointEvent(p)
            gevent.sleep(1)

    def onOnePointEvent(self, point):
        pass


'''
kline = KLine('sz159919')
kline.collect(3)
pointList = kline.pointList
from agileutil.table_writer import TableWriter
header = ['name', 'time', 'price']
rows = [ [p.name, p.time, p.now] for p in pointList ]
tbWriter = TableWriter(header, rows)
tbWriter.dump()
'''
