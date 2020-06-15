#coding=utf-8

'''
k线持久化到sqlite
'''

from kline import KLine
from point import Point
import sqlite3

CREATE_TABLE_SQL = '''CREATE TABLE `point` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(50),
  `code` VARCHAR(10),
  `dayBegin` REAL,
  `lastdayEnd` REAL,
  `now` REAL,
  `dayMax` REAL,
  `dayMin` REAL,
  `time` DATETIME
)
'''

class KLineSqlite(KLine):

    def __init__(self, code, dbname = 'kline.db'):
        super().__init__(code)
        self.dbname = dbname
        self.conn = None
        try:
            self.initDB()
        except Exception as ex:
            if 'table `point` already exists' not in str(ex):
                raise ex

    def getConnection(self):
        if self.conn == None:
            self.conn = sqlite3.connect(self.dbname)
        return self.conn

    def close(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None

    def initDB(self):
        conn = self.getConnection()
        c = conn.cursor()
        c.execute(CREATE_TABLE_SQL)
        conn.commit()
        self.close()

    def onOnePointEvent(self, point):
        point.print()
        conn = self.getConnection()
        c = conn.cursor()
        sql = "INSERT INTO point(name, code, dayBegin, lastdayEnd, now, dayMax, dayMin, time)  \
                  VALUES('%s', '%s', %f, %f, %f, %f, %f, '%s')" % (
                      point.name, point.code, point.dayBegin, point.lastdayEnd, point.now, point.dayMax, point.dayMin, str(point.time)
                  ) 
        c.execute(sql)
        conn.commit()

    def loadByTimeRange(self, startTime, endTime):
        sql = "select * from point where code='%s' and time >= '%s' and time <= '%s'" % (self.code, startTime, endTime)
        conn = self.getConnection()
        c = conn.cursor()
        cursor = c.execute(sql)
        rows = []
        for row in cursor:
            p = Point()
            p.name = row[1]
            p.code = row[2]
            p.dayBegin = row[3]
            p.lastdayEnd = row[4]
            p.now = row[5]
            p.dayMax = row[6]
            p.dayMin = row[7]
            p.time = row[8]
            rows.append(p)
        conn.close()
        return rows


klineSqlite = KLineSqlite('sz159919')
pointList = klineSqlite.loadByTimeRange('2020-06-12 09:30:00', '2020-06-12 14:38:00')
'''
from agileutil.table_writer import TableWriter
header = ['name', 'time', 'price']
rows = [ [p.name, p.time, p.now] for p in pointList ]
tbWriter = TableWriter(header, rows)
tbWriter.dump()
'''

'''
import numpy as np
from matplotlib import pyplot as plt
import time

plt.title("sz159919 ETF300") 
plt.xlabel("time") 
plt.ylabel("price")
x = []
y = []
for p in pointList:
    x.append(p.time)
    y.append(p.now)
plt.plot(x, y)
plt.show()
'''