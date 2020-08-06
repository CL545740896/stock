#coding=utf-8
'''
k线持久化到文件
'''

from kline import KLine


class KLineFile(KLine):
    def __init__(self, code):
        super().__init__(code)

    def onOnePointEvent(self, point):
        f = open('/tmp/' + self.code, 'a+')
        line = "%s|%s\n" % (point.time, point.now)
        f.write(line)
        f.close()
